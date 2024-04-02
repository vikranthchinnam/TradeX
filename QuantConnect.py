from AlgorithmImports import *
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint
import yfinance as yf
import itertools

class CointegrationAnalysisAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2022, 1, 1)
        self.SetCash(100000)

        self.tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
        self.finance_stocks = ['JPM', 'BAC', 'WFC', 'GS', 'C']

        # Create a list of all possible pairs within each group
        self.tech_pairs = list(itertools.combinations(self.tech_stocks, 2))
        self.finance_pairs = list(itertools.combinations(self.finance_stocks, 2))

        # Function to compute cointegration test and extract p-value
        def compute_cointegration(pair):
            try:
                stock1 = yf.download(pair[0], start='2020-01-01', end='2022-01-01')['Adj Close'].dropna()
                stock2 = yf.download(pair[1], start='2020-01-01', end='2022-01-01')['Adj Close'].dropna()
                _, p_value, _ = coint(stock1, stock2)
                return p_value
            except Exception as e:
                print(f"Error computing cointegration for pair {pair}: {e}")
                return None


        # Compute p-values for effector and effector stocks
        self.effector_effector_p_values = pd.DataFrame(index=self.tech_stocks, columns=self.tech_stocks)
        for pair in self.tech_pairs:
            p_value = compute_cointegration(pair)
            self.effector_effector_p_values.loc[pair[0], pair[1]] = p_value
            self.effector_effector_p_values.loc[pair[1], pair[0]] = p_value

        # Compute p-values for effected and effected stocks
        self.effected_effected_p_values = pd.DataFrame(index=self.finance_stocks, columns=self.finance_stocks)
        for pair in self.finance_pairs:
            p_value = compute_cointegration(pair)
            self.effected_effected_p_values.loc[pair[0], pair[1]] = p_value
            self.effected_effected_p_values.loc[pair[1], pair[0]] = p_value

        # Compute p-values for effector and effected stocks
        self.effector_effected_p_values = pd.DataFrame(index=self.tech_stocks, columns=self.finance_stocks)
        for effector in self.tech_stocks:
            for effected in self.finance_stocks:
                p_value = compute_cointegration((effector, effected))
                self.effector_effected_p_values.loc[effector, effected] = p_value

        print()
        print("P-values between tech stocks (effector-effector)")
        print(self.effector_effector_p_values)
        print("\n")

        print("P-values between finance stocks (effected-effected)")
        print(self.effected_effected_p_values)
        print("\n")

        print("P-values between tech and finance stocks (effector-effected)")
        print(self.effector_effected_p_values)

    def OnData(self, data):
        # This function is required, but we don't need to do anything here for this example
        pass
