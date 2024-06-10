from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import MACD
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.tickers = ["T", "VZ"]

    @property
    def interval(self):
        return "1day"  # Daily data is sufficient for MACD-based strategies

    @property
    def assets(self):
        return self.tickers

    @property
    def data(self):
        # No additional data sources are needed for this strategy
        return []

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            # Retrieve MACD for the ticker
            macd_data = MACD(ticker, data["ohlcv"], fast=12, slow=26)
            if macd_data is not None:
                # MACD line (macd), signal line (signal)
                macd_line, signal_line = macd_data["MACD"], macd_data["signal"]
                if len(macd_line) > 0 and len(signal_line) > 0:
                    # Entry signal: MACD crosses above the signal line
                    if macd_line[-1] > signal_line[-1] and macd_line[-2] < signal_line[-2]:
                        allocation_dict[ticker] = 0.5  # Allocate 50% of the portfolio to this stock
                    # Exit signal: MACD crosses below the signal line
                    elif macd_line[-1] < signal_line[-1] and macd_line[-2] > signal_line[-2]:
                        allocation_dict[ticker] = 0  # Exit the position
                    else:
                        # No significant action, maintain the current position
                        # Assuming a cash position is handled elsewhere or by default
                        continue
                else:
                    log(f"No MACD data available for {ticker}, skipping.")
            else:
                log(f"MACD calculation failed for {ticker}.")
                continue

        if not allocation_dict:
            log("No allocations made.")
            return TargetAllocation({})  # In case there are no signals, return an empty allocation

        return TargetAllocation(allocation_dict)