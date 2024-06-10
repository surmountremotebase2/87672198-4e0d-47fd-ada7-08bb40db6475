from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset, InsiderTrading
from surmount.technical_indicators import EMA, RSI
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Selecting a list of fashion industry tickers
        self.tickers = ["LVMUY", "KORS", "TIF", "NKE", "ADDYY"]
        # Adding insider trading data for analysis
        self.data_list = [InsiderTrading(i) for i in self.tickers]
        # Including some technical indicator data
        self.ema_data = {ticker: EMA(ticker, [], 20) for ticker in self.tickers}  # 20-day EMA as an example
        self.rsi_data = {ticker: RSI(ticker, [], 14) for ticker in self.tickers}  # 14-day RSI as an example

    @property
    def interval(self):
        # Daily frequency for data points
        return "1day"

    @property
    def assets(self):
        # List of assets to trade
        return self.tickers

    @property
    def data(self):
        # Data required for running the strategy
        return self.data_list

    def run(self, data):
        allocation_dict = dict()
        for ticker in self.tickers:
            allocation_dict[ticker] = 0  # Initialize allocation for each ticker

            # Check for recent insider sales
            insider_trades = data[InsiderTrading(ticker)]
            recent_sales = sum(1 for trade in insider_trades if trade['transactionType'].lower() == 'sale')

            # Determine if trending up using EMA and RSI for condition
            trending_up = self.ema_data[ticker][-1] > self.ema_data[ticker][-2] and self.rsi_data[ticker][-1] < 70

            # If insider sales are low and the stock is trending up, allocate accordingly
            if recent_sales < 3 and trending_up:
                allocation_dict[ticker] = 1 / len(self.tickers)  # Equally weighted allocation for simplicity

        return TargetAllocation(allocation_dict)