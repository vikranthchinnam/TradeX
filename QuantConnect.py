from AlgorithmImports import *
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import coint
import yfinance as yf
import itertools

class CointegrationAnalysisAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2023, 1, 1)
        self.SetCash(100000)
        

        self.tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
        self.finance_stocks = ['JPM', 'BAC', 'WFC', 'GS', 'C']
        self.tech_pairs = list(itertools.combinations(self.tech_stocks, 2))
        self.finance_pairs = list(itertools.combinations(self.finance_stocks, 2))

        for stock in self.tech_stocks:
            self.AddEquity(stock, Resolution.Daily)
        for stock in self.finance_stocks:
            self.AddEquity(stock, Resolution.Daily)

        self.effector_effector_p_values = pd.DataFrame(index=self.tech_stocks, columns=self.tech_stocks)
        self.effected_effected_p_values = pd.DataFrame(index=self.finance_stocks, columns=self.finance_stocks)
        self.effector_effected_p_values = pd.DataFrame(index=self.tech_stocks, columns=self.finance_stocks)



        # Schedule the ComputeAndDebugCointegration to run every 30 days
        self.Schedule.On(self.DateRules.EveryDay(), self.TimeRules.At(0, 0), self.ComputeAndDebugCointegration)
    def compute_cointegration(self, pair):
        try:
            history1 = self.History([pair[0]], 120, Resolution.Daily)  # Last 120 days
            history2 = self.History([pair[1]], 120, Resolution.Daily)
            if history1.empty or history2.empty:
                return None
            stock1 = history1['close'].dropna()
            stock2 = history2['close'].dropna()
            _, p_value, _ = coint(stock1, stock2)
            return p_value
        except Exception as e:
            self.Debug(f"Error computing cointegration for pair {pair}: {e}")
            return None
    def ComputeAndDebugCointegration(self):
        # Ensure we only execute every 30 days
        if (self.Time - self.StartDate).days % 30 == 0:
            # For for effector effector
            for pair in self.tech_pairs:
                p_value = self.compute_cointegration(pair)
                
                self.effector_effector_p_values.loc[pair[0], pair[1]] = p_value
                self.effector_effector_p_values.loc[pair[1], pair[0]] = p_value
            # For for affected to affected
            for pair in self.finance_pairs:
                p_value = self.compute_cointegration(pair)
                self.effected_effected_p_values.loc[pair[0], pair[1]] = p_value
                self.effected_effected_p_values.loc[pair[1], pair[0]] = p_value

            for effector in self.tech_stocks:
                for effected in self.finance_stocks:
                    p_value = self.compute_cointegration((effector, effected))
                    self.effector_effected_p_values.loc[effector, effected] = p_value
            
            self.Debug(f"Effector Effector\n {self.effector_effector_p_values.head()} \n")
            self.Debug(f"Effected Effected\n {self.effected_effected_p_values.head()} \n")
            self.Debug(f"Effector Effected\n {self.effector_effected_p_values.head()} \n")



    def OnData(self, data):
        pass