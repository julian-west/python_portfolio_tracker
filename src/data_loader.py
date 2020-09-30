"""Load Stock Prices"""
import pandas as pd


class StockPriceLoader:
    """
    Load stock prices from tickers specified in input_data_source
    
    Args:
        input_data_source (str): location of input csv file containing a list
            of ticker symbols
    
    Attributes:
        __repr__ (pd.DataFrame): dataframe containing stock prices
    
    
    """

    def __init__(self, input_data_source: str = "../data/raw/positions.csv"):
        self.input_data_source = input_data_source
        self.positions = self.load_positions()

    def __repr__(self):
        return str(self.positions)

    def load_positions(self):
        return pd.read_csv(self.input_data_source, parse_dates=["date"])

