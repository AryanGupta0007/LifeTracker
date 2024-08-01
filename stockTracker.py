import yfinance as yf
import time
ticker_symbol = 'PCJEWELLER.NS'

# Get the data of the stock
while True:
    apple_stock = yf.Ticker(ticker_symbol)

    historical_prices = apple_stock.history(period='1d', interval='1m')

    # Get the latest price and time
    latest_price = historical_prices['Close'].iloc[-1]

    latest_time = historical_prices.index[-1].strftime('%H:%M:%S')
    print(latest_price, latest_time)
    price = apple_stock.info

    print(price['bid'])
    print(price['ask'])

