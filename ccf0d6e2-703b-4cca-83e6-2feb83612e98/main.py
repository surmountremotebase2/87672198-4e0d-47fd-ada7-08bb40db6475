from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA, EMA
from surmount.logging import log
from surmount.data import InstitutionalOwnership, InsiderTrading

class TradingStrategy(Strategy):
    def __init__(self):
        # List of tickers for Nvidia, Tesla, and Apple
        self.tickers = ["NVDA", "TSLA", "AAPL"]
        
        # Combining data for both institutional ownership and insider trading as part of the strategy criteria
        self.data_list = [InstitutionalOwnership(i) for i in self.tickers]
        self.data_list += [InsiderTrading(i) for i in self.tickers]

    @property
    def interval(self):
        # Daily data interval
        return "1day"

    @property
    def assets(self):
        # Defines the assets that the strategy will analyze and potentially trade
        return self.tickers

    @property
    def data(self):
        # Specifies the additional data that will be used to inform the trading decisions
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            long_term_trend = EMA(ticker, data["ohlcv"], 200)  # Long term trend with 200-day EMA
            short_term_trend = SMA(ticket, data["ohlcv"], 50) # Short-term trend with 50-day SMA
            
            # Verify if both lists have enough data to compute the strategies
            if not long_term_trend or not short_term_trend:
                log(f"Insufficient data for {ticker}")
                allocation_dict[ticker] = 0  # Avoid trading if data is insufficient
                continue

            # Trading decision based on trend: go long if the short-term trend is above the long-term trend
            if short_term_trend[-1] > long_term_trend[-1]:
                allocation_dict[ticker] = 1 / len(self.tickers)
            else:
                allocation_dict[ticker] = 0  # Do not allocate if short-term trend is below the long-term trend

        # Return the calculated target allocation for each ticker
        return TargetAllocation(allocation_dict)