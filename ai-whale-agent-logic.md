# Whale Agent Overlook

## Purpose
The **WhaleAgent** monitors changes in Open Interest (OI) for cryptocurrency markets (e.g., Bitcoin and Ethereum) to detect significant movements caused by "whales" — large traders who may influence the market. It uses historical data, APIs, and AI to analyze patterns and recommend actions.

![](whale.jpg)

## Key Components

### Initialization (`__init__`)
- **Configuration & Setup:**
  - Loads AI models and parameters, including overrides if specified.
  - Fetches API keys for OpenAI and Anthropic for AI-related operations.
  - Sets up directories for data and audio storage.

- **History Loading:**
  - Attempts to load historical OI data from a CSV file. If none exists, it creates a new file.
  - Cleans up old data (only keeps the last 24 hours of OI records).

### Whale Detection Logic
The agent identifies "whale activity" when the current change in OI is significantly above the historical rolling average.

- **Rolling Average & Threshold:**
  - Computes the rolling average of absolute percentage changes.
  - Multiplies this average by a threshold (`WHALE_THRESHOLD_MULTIPLIER`) to detect unusual spikes.

### AI Integration
- Uses a predefined **WHALE_ANALYSIS_PROMPT** to format data for analysis by an AI model.
- AI suggests whether to "BUY," "SELL," or "DO NOTHING," with a confidence level.

### Announcements
- Provides voice announcements for detected whale activities using OpenAI's voice generation API.
- Only announces whale events audibly; general updates are logged.

---

## Main Workflow

### Monitoring Cycle (`run_monitoring_cycle`)
1. **Fetch Current Data:**
   - Calls an API to get the latest OI data for Bitcoin, Ethereum, and total markets.
  
2. **Calculate Changes:**
   - Compares the current OI to the historical OI from a configured interval (`CHECK_INTERVAL_MINUTES`) to calculate percentage changes.

3. **Detect Whale Activity:**
   - Checks if the percentage change exceeds the whale detection threshold.

4. **AI Analysis:**
   - If whale activity is detected, analyzes the data using AI to provide actionable insights.

5. **Announcements:**
   - Logs or audibly announces results depending on whether whale activity is detected.

### Save New Data (`_save_oi_data`)
- Appends new OI data with calculated percentage changes to the history file and updates the rolling dataset.

### Detect Historical Changes (`_get_historical_oi`)
- Retrieves OI data from a specific time in the past for change calculations.

---

## Key Functions and Their Roles

| **Function**                  | **Purpose**                                                                                          |
|-------------------------------|------------------------------------------------------------------------------------------------------|
| `load_history`                | Loads or initializes historical OI data, cleans up old records, and saves the dataset.              |
| `_save_oi_data`               | Appends new OI data, calculates percentage changes, and saves the updated history.                  |
| `_get_current_oi`             | Fetches the latest OI data from the API.                                                            |
| `_get_historical_oi`          | Retrieves historical OI data for comparison with current values.                                    |
| `_calculate_changes`          | Computes percentage changes in OI over a given interval.                                            |
| `_detect_whale_activity`      | Identifies significant OI changes above the rolling average, using a multiplier threshold.          |
| `_analyze_opportunity`        | Uses AI to analyze market data and recommend actions.                                               |
| `_announce`                   | Logs or announces messages; uses voice announcements for whale activities.                         |
| `_format_announcement`        | Formats changes and AI recommendations into a speech-friendly message.                             |
| `run_monitoring_cycle`        | Executes a full monitoring cycle: fetch data, calculate changes, detect whales, and analyze/announce. |

---

## Core Logic Flow
1. **Load Historical Data:**
   - Start with recent OI history to enable change detection.

2. **Fetch Current Data:**
   - Use the API to get the latest OI values.

3. **Calculate Percentage Changes:**
   - Compare the current OI with historical values to compute percentage changes.

4. **Detect Whale Activity:**
   - Check if the change exceeds the threshold (rolling average * multiplier).

5. **AI Analysis (if Whale Activity):**
   - Send OI data and changes to an AI model for actionable insights.

6. **Announce Results:**
   - Log or audibly announce findings, including AI recommendations.

---

## Whale Detection Formula
- **Rolling Average Threshold:**
  ```
  Threshold = Rolling Average * WHALE_THRESHOLD_MULTIPLIER
  ```

- **Is Whale?**
  ```
  Whale Activity = Current Change (abs) > Threshold
  ```

---

## How to Understand Its Actions

- **Whale Activity Detection:**
  - Look at percentage changes in OI. Large deviations might indicate market manipulation or significant trades.

- **AI Recommendations:**
  - The AI suggests "BUY," "SELL," or "NOTHING" based on detected patterns and market data.

- **Confidence:**
  - AI outputs a confidence level, indicating the strength of its recommendation.

- **Announcements:**
  - General updates are logged.
  - Whale activities are audibly announced, possibly with AI analysis.

---

## For Debugging or Extending
- **Start Small:** 
  - Focus on individual functions, like `load_history` or `_detect_whale_activity`.
  
- **Run Tests:**
  - Simulate different scenarios by providing sample OI data and observing the behavior.

- **Log Outputs:**
  - Ensure all calculations and detections are logged for verification.

---

Let me know which part you'd like to dive deeper into, and I can provide more detailed explanations!
