# Whale Agent AI

Whale Agent AI is a Python-based tool designed to monitor and analyze Bitcoin (BTC) futures open interest (OI) data. It detects significant market activity ("whale activity") and provides actionable insights using OpenAI's GPT-4 model.

---

## Features

- **Real-Time Open Interest Monitoring**
  - Fetches BTC futures OI data from Binance every 5 minutes.
  - Calculates percentage changes to detect significant activity.

- **Whale Detection**
  - Identifies "whale activity" based on customizable thresholds.
  - Highlights significant OI changes to help spot market trends.

- **AI-Powered Analysis**
  - Uses OpenAI's GPT-4 to provide actionable insights (e.g., BUY, SELL, or NOTHING).
  - Includes confidence levels and reasoning for each recommendation.

- **Historical Data Logging**
  - Maintains an `oi_history.csv` file to store historical OI data.
  - Enables trend analysis over time.

---

## Installation

### Prerequisites
- Python 3.7+
- Binance API access (public endpoints are used).
- OpenAI API key for GPT-4.

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd whale-agent
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your environment variables:
   - Create a `.env` file in the project root:
     ```plaintext
     OPENAI_API_KEY=your_openai_api_key
     ```

---

## Usage

1. Run the script:
   ```bash
   python whale-ai-agent.py
   ```

2. Monitor the output:
   - The agent will fetch OI data every 5 minutes.
   - Significant changes in OI will trigger whale activity detection and AI analysis.

3. Review the AI's recommendations:
   - Example Output:
     ```plaintext
     🐋 WhaleAgent started. Monitoring OI changes...
     🔍 Avg Change: 5.00%, Threshold: 5.50%, BTC Change: 6.67%
     🐋 Whale Activity Detected: True
     🤖 AI Analysis:
     BUY
     The increase in BTC Open Interest (OI) indicates a growing interest in the market, which could potentially drive the price up.
     Confidence: 75%
     ```

---

## Configuration

### Modify Detection Sensitivity
- Adjust `self.whale_threshold_multiplier` in the `__init__` method to change sensitivity:
  ```python
  self.whale_threshold_multiplier = 1.25  # Default is 1.1 for high sensitivity
  ```

### Customize Monitoring Interval
- Modify `self.check_interval` (in minutes) in the `__init__` method:
  ```python
  self.check_interval = 5  # Default is 5 minutes
  ```

---

## File Structure

```plaintext
whale-agent/
├── whale-ai-agent.py      # Main script
├── mocktest.py            # For testing purposes
├── requirements.txt       # Dependencies
├── .gitignore             # Ignored files
├── .env                   # API keys (not tracked by Git)
├── oi_history.csv         # Historical data
└── README.md              # Project documentation
```

---

## Example Prompts for AI
The AI model analyzes whale activity using the following structured prompt:

```plaintext
You must respond in exactly 3 lines:
Line 1: BUY, SELL, or NOTHING
Line 2: Reason for your suggestion
Line 3: Confidence: X%

BTC OI changed by {btc_change}%:
Current OI: {total_change}%.
```

---

## Limitations

1. **Data Reliability:** Relies on Binance API for accurate OI data.
2. **Model Dependency:** Requires an active OpenAI API key and sufficient credits.
3. **Market Context:** AI analysis is based solely on OI changes without additional market data.

---

## Contributions

Contributions are welcome! Feel free to open an issue or submit a pull request.

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## Acknowledgments

- **Binance**: For providing the OI data API.
- **OpenAI**: For the GPT-4 API integration.
