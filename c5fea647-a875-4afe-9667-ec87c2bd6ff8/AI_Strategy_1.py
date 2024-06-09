from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset, CompanyInfo, PerformanceMetric

class TradingStrategy(Strategy):
    def __init__(self):
        # List to hold tickers of interest, initially empty
        self.tickers = []
        # Assuming a function or a way to get Spanish companies from diverse sectors
        self.spanish_companies = self.get_spanish_companies_from_diverse_sectors()

    @property
    def interval(self):
        # A long-term outlook might be better captured with monthly data
        return "1month"

    @property
    def assets(self):
        # Tickers are derived from the Spanish companies identified
        return self.tickers

    @property
    def data(self):
        # Assuming PerformanceMetric is a class that encapsulates performance data for companies
        return [PerformanceMetric(ticker) for ticker in self.tickers]

    def get_spanish_companies_from_diverse_sectors(self):
        # Placeholder for a method to get a list of Spanish companies across different sectors
        # This method should update self.tickers with the company symbols
        pass

    def evaluate_performance(self, data):
        # Placeholder for evaluating performance, returning a score for sorting
        return data['performance_metric']  # Hypothetical metric

    def run(self, data):
        # Initialize all allocations to zero
        allocation_dict = {ticker: 0 for ticker in self.tickers}
        performance_scores = []

        # Evaluate and score the performance of each company
        for ticker in self.tickers:
            performance_data = data[ticker]
            score = self.evaluate_performance(performance_data)
            performance_scores.append((ticker, score))

        # Sort companies based on performance scores in descending order (higher is better)
        sorted_companies = sorted(performance_scores, key=lambda x: x[1], reverse=True)

        # Allocate investments to top N companies, N can be decided based on how diversified you want to be
        N = 5
        for ticker, score in sorted_companies[:N]:
            allocation_dict[ticker] = 1.0 / N  # Evenly distribute among top N

        return TargetAlbumlocation(allocation_dict)