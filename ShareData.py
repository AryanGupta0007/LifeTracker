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
            if interval:
                stock_history = self.stock.history(interval=interval)
            if period:
                stock_history = self.stock.history(period=period)
            if interval and period:
                stock_history = self.stock.history(period=period, interval=interval)
            return stock_history

        except Exception as e:
            print(f"Error2 {e}")
            time.sleep(10)

    def get_bid_and_ask_price(self):
        # print(self.stock.info)
        try:
            if 'bid' in self.stock.info:
                bid_price = self.stock.info['bid']
                ask_price = self.stock.info['ask']
            else:
                bid_price = self.stock.info['currentPrice']
                ask_price = self.stock.info['currentPrice']

            return bid_price, ask_price
        except Exception as e:
            print(f"Error3 {e}")
            time.sleep(10)

    def get_market_price(self):
        try:
            bid, ask = self.get_bid_and_ask_price()
            market_price = (bid + ask) / 2
            return market_price
        except Exception as e:
            print(f"Error4 {e}")
            time.sleep(10)

    def get_stock_info(self):
        try:
            stock_info = self.stock.info
            return stock_info
        except Exception as e:
            print(f"Error5 {e}")
            time.sleep(10)
