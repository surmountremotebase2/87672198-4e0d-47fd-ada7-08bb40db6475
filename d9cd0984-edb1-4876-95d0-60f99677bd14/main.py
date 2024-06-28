from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        # Green energy tickers - Example tickers, update this list based on your specific green energy focus
        self.tickers = ["ICLN", "TAN", "QCLN", "FAN"]
        # Short and long SMAs periods
        self.short_sma_period = 10
        self.long_sma_period = 30

    @property
    def interval(self):
        # Daily interval for this strategy
        return "1day"

    @property
    def assets(self):
        # The assets this strategy will handle
        return self.tickers

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            # Calculate the two SMAs for each asset
            short_sma = SMA(ticker, data["ohlcv"], self.short_sma_period)
            long_sma = SMA(ticker, data["ohlcv"], self.long_sma_period)

            if len(short_sma) > 0 and len(long_sma) > 0:  # Ensure we have SMA data
                # Buy signal: Short-term SMA crosses above long-term SMA
                if short_sma[-1] > long_sma[-1] and short_sma[-2] <= long_sma[-2]:
                    log(f"Buy signal for {ticker}")
                    allocation_dict[ticker] = 1.0 / len(self.tickers)  # Equally divide allocation among tickers

                # Sell signal: Short-term SMA crosses below long-term SMA
                elif short_sma[-1] < long_sma[-1] and short_sma[-2] >= long_sma[-2]:
                    log(f"Sell signal for {ticker}")
                    allocation_dict[ticker] = 0  # Exit position
                
                else: # Hold current position if no crossover signal
                    allocation_dict[ticker] = 0.5 / len(self.tickers)  # This is arbitrary, adjust based on strategy needs
            else:
                # Default to no allocation if insufficient data
                allocation_dict[ticker] = 0

        return TargetAllocation(allocation_dict)