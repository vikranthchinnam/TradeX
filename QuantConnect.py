from AlgorithmImports import *
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint

class CointegrationAnalysisAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2022, 1, 1)
        self.SetCash(100000)

        # Define stock symbols
        self.tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB']  # Note: Replaced 'META' with 'FB' for compatibility
        self.finance_stocks = ['JPM', 'BAC', 'WFC', 'GS', 'C']

        # Add the equity assets
        self.symbols = {}
        for ticker in self.tech_stocks + self.finance_stocks:
            self.symbols[ticker] = self.AddEquity(ticker, Resolution.Daily).Symbol

        self.lookback = 252  # Lookback period for historical data

        # Schedule the analysis to run at the start of the algorithm
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.AfterMarketOpen(next(iter(self.symbols.values())), 10), self.RunAnalysis)

    def OnData(self, data):
        # This function is required, but we don't need to do anything here for this example
        pass

    def RunAnalysis(self):
        # This is a placeholder for the analysis function
        # Due to the complexity of fetching and analyzing multiple pairs, consider breaking down the tasks
        # and possibly using a custom data structure to store historical data for analysis

        # Example: Fetch historical data for a single pair
        history1 = self.History(self.symbols['AAPL'], self.lookback, Resolution.Daily).close.unstack(level=0)
        history2 = self.History(self.symbols['MSFT'], self.lookback, Resolution.Daily).close.unstack(level=0)

        # Ensure we have enough data points
        if len(history1) < self.lookback or len(history2) < self.lookback:
            self.Debug("Not enough data points for analysis")
            return

        # Perform cointegration test for a single pair as an example
        _, p_value, _ = coint(history1, history2)
        self.Debug(f"Cointegration test p-value for AAPL and MSFT: {p_value}")

        # Expand this section to loop through all pairs and perform analysis as per your requirements

    def OnEndOfAlgorithm(self):
        # This function is required, but we don't need to do anything here for this example
        pass
