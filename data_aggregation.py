import yfinance as yf
import pandas as pd
import numpy as np
import itertools

tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']
finance_stocks = ['JPM', 'BAC', 'WFC', 'GS', 'C']

# Create a list of all possible pairs within each group
tech_pairs = list(itertools.combinations(tech_stocks, 2))
finance_pairs = list(itertools.combinations(finance_stocks, 2))

# returns correlation coefficient (between -1 and 1)
def compute_coefficient(pair):
    stock1 = yf.download(pair[0], start="2020-01-01", end="2022-01-01")['Adj Close']
    stock2 = yf.download(pair[1], start="2020-01-01", end="2022-01-01")['Adj Close']

    stock1_returns = stock1.pct_change() * 100 
    stock2_returns = stock2.pct_change() * 100 

    stock1_returns = stock1_returns.dropna()
    stock2_returns = stock2_returns.dropna()

    c = np.corrcoef(stock1, stock2)
    return c[0, 1]

# Compute correlation coefficient for effector and effector stocks
effector_effector_p_values = pd.DataFrame(index=tech_stocks, columns=tech_stocks)
for pair in tech_pairs:
    p_value = compute_coefficient(pair)
    effector_effector_p_values.loc[pair[0], pair[1]] = p_value
    effector_effector_p_values.loc[pair[1], pair[0]] = p_value

# Compute correlation coefficient for effected and effected stocks
effected_effected_p_values = pd.DataFrame(index=finance_stocks, columns=finance_stocks)
for pair in finance_pairs:
    p_value = compute_coefficient(pair)
    effected_effected_p_values.loc[pair[0], pair[1]] = p_value
    effected_effected_p_values.loc[pair[1], pair[0]] = p_value

# Compute correlation coefficient for effector and effected stocks
effector_effected_p_values = pd.DataFrame(index=tech_stocks, columns=finance_stocks)
for effector in tech_stocks:
    for effected in finance_stocks:
        p_value = compute_coefficient((effector, effected))
        effector_effected_p_values.loc[effector, effected] = p_value

print()
print("Correlation coefficient between tech stocks (effector-effector)")
print(effector_effector_p_values)
print("\n")

print("Correlation coefficient between finance stocks (effected-effected)")
print(effected_effected_p_values)
print("\n")

print("Correlation coefficient between tech and finance stocks (effector-effected)")
print(effector_effected_p_values)
