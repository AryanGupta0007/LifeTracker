import yfinance as yf
import time


class ShareData:
    def __init__(self, stock):
        try:
            self.stock = yf.Ticker(stock)
        except Exception as e:
            print(f"Error {e}")
            time.sleep(10)

    def get_historical_data(self, interval=None, period=None):
        try:
            if interval and period:
                stock_history = self.stock.history(period=period, interval=interval)
            elif interval:
                stock_history = self.stock.history(interval=interval)
            elif period:
                stock_history = self.stock.history(period=period)
            else:
                stock_history = self.stock.history()
            return stock_history
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            time.sleep(10)

    def get_bid_and_ask_price(self):
        try:
            stock_info = self.stock.info
            bid_price = stock_info.get('bid', stock_info.get('currentPrice', None))
            ask_price = stock_info.get('ask', stock_info.get('currentPrice', None))
            if bid_price is None or ask_price is None:
                raise ValueError("Bid or Ask price not found.")
            return bid_price, ask_price
        except Exception as e:
            print(f"Error fetching bid and ask price: {e}")
            time.sleep(10)

    def get_market_price(self):
        try:
            bid, ask = self.get_bid_and_ask_price()
            if bid is None or ask is None:
                raise ValueError("Bid or Ask price not available for market price calculation.")
            market_price = (bid + ask) / 2
            return market_price
        except Exception as e:
            print(f"Error calculating market price: {e}")
            time.sleep(10)

    def get_stock_info(self):
        try:
            stock_info = self.stock.info
            return stock_info
        except Exception as e:
            print(f"Error fetching stock info: {e}")
            time.sleep(10)
