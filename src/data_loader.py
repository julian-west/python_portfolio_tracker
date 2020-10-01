"""Load Stock Prices"""
import datetime
import pandas as pd
import ffn

TODAY = datetime.datetime.now().date()


class PositionLoader:
    """Load positions input data"""

    def __init__(self, input_data_source: str = "../data/raw/purchase_info.csv"):
        self.input_data_source = input_data_source
        self.positions = self._load_positions()
        self.datetime_index = self._generate_datetime_index()

    def _load_positions(self):
        """Load positions from input_data_source"""
        positions = pd.read_csv(self.input_data_source, parse_dates=["date"])

        if positions.isnull().sum().sum() != 0:
            raise ValueError(
                "There is missing data in the input csv. Please fix these "
                "errors, save and try again."
            )

        self.tickers = list(
            positions[positions["yahoo_ticker"] != "cash"]["yahoo_ticker"].unique()
        )
        self.start_date = positions["date"].min()

        return positions

    def _generate_datetime_index(self):
        """Create a datetime index starting from earliest stock purchase date"""
        return pd.date_range(
            self.positions["date"].min(),
            end=TODAY,
            freq="D",
        )


class StockPriceLoader(PositionLoader):
    """
    Load stock prices from tickers specified in input_data_source

    Args:
        input_data_source (str): location of input csv file containing a list
            of ticker symbols

    Attributes:
        input_data_source (str): location of specified data source
        positions (pd.DataFrame): dataframe of loaded csv datasource
        tickers (list): list of tickers in the input data source
        start_date (pd.datetime): earlist purchase date in the portfolio
        daily_stock_prices (pd.DataFrame): dataframe containing the daily
            closing stock prices for all tickers in self.tickers starting from
            self.start_date to today's date

    """

    def __init__(self, input_data_source: str = "../data/raw/purchase_info.csv"):
        super().__init__(input_data_source)
        self.daily_stock_prices = self.get_stock_prices()

    def __repr__(self):
        return f"Tickers: {self.tickers}\nStart Date: {str(self.start_date)}"

    def get_stock_prices(self):
        """Load stock prices from list of tickers"""

        if len(self.tickers) > 15:
            raise ValueError(
                f"There are {len(self.tickers)} tickers in the input data "
                "source. The maximum number of stocks for this program is 15"
            )
        return ffn.get(self.tickers, start=self.start_date, clean_tickers=False)
