import os
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv
import openai
import requests  # Added for Binance API requests
import time

class WhaleAgent:
    """Simplified Whale Agent using OpenAI only."""

    def __init__(self):
        """Initialize WhaleAgent."""
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("🚨 OPENAI_API_KEY not found in environment variables!")
        openai.api_key = self.api_key

        self.data_file = "oi_history.csv"
        self.history = self._load_history()
        self.check_interval = 5  # Check interval in minutes
        self.whale_threshold_multiplier = 1.1  # Reduced for more sensitivity

    def _load_history(self):
        """Load or initialize historical data."""
        if os.path.exists(self.data_file):
            df = pd.read_csv(self.data_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            return df
        else:
            return pd.DataFrame(columns=['timestamp', 'btc_oi', 'total_oi'])

    def _save_history(self):
        """Save history to file."""
        self.history.to_csv(self.data_file, index=False)

    def _get_current_oi(self):
        """Fetch current OI data from Binance API."""
        try:
            url = "https://fapi.binance.com/futures/data/openInterestHist"
            params = {
                "symbol": "BTCUSDT",  # Bitcoin futures
                "period": "5m",       # Data interval (e.g., 5 minutes)
                "limit": 1              # Fetch the latest data point
            }
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data:
                    latest = data[-1]  # Get the latest OI data point
                    return {
                        "btc_oi": float(latest["sumOpenInterest"]),
                        # Use the same key for total OI if USD data is unavailable
                        "total_oi": float(latest.get("sumOpenInterestUsd", latest["sumOpenInterest"]))
                    }
            raise ValueError("❌ Failed to fetch OI data from Binance API")
        except Exception as e:
            print(f"❌ Error in _get_current_oi: {e}")
            return None

    def _calculate_changes(self, current_oi):
        """Calculate percentage changes in OI."""
        if self.history.empty:
            return None

        last_oi = self.history.iloc[-1]
        btc_change = (current_oi['btc_oi'] - last_oi['btc_oi']) / last_oi['btc_oi'] * 100
        total_change = (current_oi['total_oi'] - last_oi['total_oi']) / last_oi['total_oi'] * 100

        return {'btc_change': btc_change, 'total_change': total_change}

    def _detect_whale_activity(self, changes):
        """Detect whale activity based on changes."""
        avg_change = self.history['btc_oi'].pct_change().mean() * 100 if not self.history.empty else 0
        avg_change = 0 if pd.isna(avg_change) else avg_change  # Handle NaN
        threshold = avg_change * self.whale_threshold_multiplier
        print(f"🔍 Avg Change: {avg_change:.2f}%, Threshold: {threshold:.2f}%, BTC Change: {changes['btc_change']:.2f}%")
        return abs(changes['btc_change']) > threshold

    def _analyze_opportunity(self, changes):
        """Use OpenAI to analyze market data and provide insights."""
        prompt = f"""
        You must respond in exactly 3 lines:
        Line 1: BUY, SELL, or NOTHING
        Line 2: Reason for your suggestion
        Line 3: Confidence: X%

        BTC OI changed by {changes['btc_change']:.2f}%:
        Current OI: {changes['total_change']:.2f}%.
        """
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",  # Use the supported GPT-4 model
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0
            )
            return response['choices'][0]['message']['content'].strip()
        except openai.error.OpenAIError as e:
            print(f"❌ OpenAI API Error: {e}")
            return "NOTHING\nUnable to analyze due to API error\nConfidence: 0%"

    def run_cycle(self):
        """Run a single monitoring cycle."""
        current_oi = self._get_current_oi()
        if current_oi is None:
            print("⚠️ Skipping cycle due to OI fetch error.")
            return

        timestamp = datetime.now()

        # Ensure history has the correct structure
        if self.history.empty:
            self.history = pd.DataFrame(columns=['timestamp', 'btc_oi', 'total_oi'])

        changes = self._calculate_changes(current_oi)
        if not changes:
            print("🚀 Initial data point added.")
            self.history = pd.concat(
                [self.history, pd.DataFrame([{
                    'timestamp': timestamp, 'btc_oi': current_oi['btc_oi'], 'total_oi': current_oi['total_oi']
                }])],
                ignore_index=True
            )
            self._save_history()
            return

        whale_detected = self._detect_whale_activity(changes)
        print(f"🐋 Whale Activity Detected: {whale_detected}")

        if whale_detected:
            analysis = self._analyze_opportunity(changes)
            print(f"🤖 AI Analysis:\n{analysis}")

        # Add current OI to history
        self.history = pd.concat(
            [self.history, pd.DataFrame([{
                'timestamp': timestamp, 'btc_oi': current_oi['btc_oi'], 'total_oi': current_oi['total_oi']
            }])],
            ignore_index=True
        )
        self._save_history()

if __name__ == "__main__":
    agent = WhaleAgent()
    print("🐋 WhaleAgent started. Monitoring OI changes...")
    while True:
        agent.run_cycle()
        time.sleep(60 * agent.check_interval)
