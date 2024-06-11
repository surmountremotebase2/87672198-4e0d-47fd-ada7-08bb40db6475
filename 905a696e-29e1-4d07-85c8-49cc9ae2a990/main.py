from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA  # Using Exponential Moving Average for better responsiveness
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # List of sports apparel companies we are interested in
        self.tickers = ["NKE", "UAA", "ADDYY"]

    @property
    def interval(self):
        # Choosing '1day' interval for daily analysis
        return "1day"

    @property
    def assets(self):
        # Targeted assets for the strategy
        return self.tickers

    @property
    def data(self):
        # No additional data required for this simple strategy
        return []

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            # Fetch the closing prices and calculate the EMA for each ticker
            closing_prices = [i[ticker]["close"] for i in data["ohlcv"]]
            # Using an arbitrary value of 21 days for the EMA
            ema_values = EMA(ticker, data["ohlcv"], 21)

            if len(ema_values) == 0:
                # Handle the case where EMA couldn't be calculated (e.g., not enough data)
                log(f"EMA for {ticker} could not be calculated due to insufficient data.")
                allocation_dict[ticker] = 0
                continue

            # Compare the latest closing price to the latest EMA value
            if closing_prices[-1] > ema_values[-1]:
                # If the stock price is above the EMA, allocate a higher portion of the portfolio to this stock
                allocation_dict[ticker] = 0.8 / len(self.tickers)  # Example allocation approach
            else:
                # Otherwise, reduce the allocation or avoid the stock
                allocation_dict[ticker] = 0.2 / len(self.tickers)  # Minimal investment in underperformers

        # The allocation_dict now contains the strategy's decisions for each ticker
        return TargetFreight(allocation_dict)