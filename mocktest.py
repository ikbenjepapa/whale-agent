import requests

def get_oi_and_price():
    # Fetch Open Interest
    url_oi = "https://fapi.binance.com/futures/data/openInterestHist"
    params_oi = {
        "symbol": "BTCUSDT",
        "period": "5m",
        "limit": 10
    }

    response_oi = requests.get(url_oi, params=params_oi)
    if response_oi.status_code == 200:
        data_oi = response_oi.json()
    else:
        print(f"Error fetching OI: {response_oi.status_code}")
        return

    # Fetch BTC Price
    url_price = "https://api.binance.com/api/v3/ticker/price"
    params_price = {"symbol": "BTCUSDT"}
    response_price = requests.get(url_price, params=params_price)
    if response_price.status_code == 200:
        btc_price = float(response_price.json()["price"])
    else:
        print(f"Error fetching BTC price: {response_price.status_code}")
        return

    # Process and Print Results
    for entry in data_oi:
        timestamp = entry['timestamp']
        btc_oi = float(entry['sumOpenInterest'])
        oi_usd = btc_oi * btc_price  # Calculate OI in USD
        print(f"Timestamp: {timestamp}, OI (BTC): {btc_oi}, OI (USD): {oi_usd:.2f}")

get_oi_and_price()
