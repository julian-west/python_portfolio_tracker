"""Load Stock Prices"""
import datetime
from typing import List
import pandas as pd
import pandas_datareader as web
import ffn

TODAY = datetime.datetime.now().date()


class PositionLoader:
    """Load positions input data"""

    def __init__(self, input_data_source: str = "../data/raw/purchase_info.csv"):
        self.input_data_source = input_data_source
        self.positions = self._load_positions()
        self.tickers = self._get_tickers()
        self.start_date = self._get_start_date()
        self.datetime_index = self._generate_datetime_index()
        self.stock_metadata = self._extract_metadata()

    def _load_positions(self):
        """Load positions from input_data_source"""
        positions = pd.read_csv(self.input_data_source, parse_dates=["date"])

        if positions.isnull().sum().sum() != 0:
            raise ValueError(
                "There is missing data in the input csv. Please fix these "
                "errors, save and try again."
            )

        return positions

    def _get_tickers(self):
        """Get list of all unique tickers present in the input data"""
        return list(
            self.positions[self.positions["yahoo_ticker"] != "cash"][
                "yahoo_ticker"
            ].unique()
        )

    def _get_start_date(self):
        """Get earliest date from input data"""
        return self.positions["date"].min()

    def _generate_datetime_index(self):
        """Create a datetime index starting from earliest stock purchase date"""
        return pd.date_range(
            self.positions["date"].min(),
            end=TODAY,
            freq="D",
        )

    def _extract_metadata(self):
        """Extract metadata for each stock"""

        metadata = {}
        for ticker in self.tickers:
            stock_row = self.positions[self.positions["yahoo_ticker"] == ticker].iloc[0]
            metadata[ticker] = {
                "company": stock_row["company"],
                "currency": stock_row["currency"],
            }

        return metadata


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
        self.daily_stock_prices_local_currency = self._get_stock_prices_local_currency()
        self.daily_stock_prices_usd = self._get_stock_prices_usd()

    def __repr__(self):
        return f"Tickers: {self.tickers}\nStart Date: {str(self.start_date)}"

    def _get_stock_prices_local_currency(self):
        """Load stock prices (in local currency) from list of tickers"""

        if len(self.tickers) > 15:
            raise ValueError(
                f"There are {len(self.tickers)} tickers in the input data "
                ". The maximum number of stocks for this program is 15"
            )
        stock_prices_local = ffn.get(
            self.tickers, start=self.start_date, clean_tickers=False
        )
        stock_prices_local = stock_prices_local.reindex(
            self.datetime_index, method="ffill"
        )
        return stock_prices_local

    def _get_stock_prices_usd(self):
        """Convert local prices to USD"""

        # load daily exchange rates
        xrates = CurrencyLoader(self.datetime_index, self.positions)

        currencies_df = pd.DataFrame(self.datetime_index).set_index(0)
        for ticker in self.tickers:
            cur = self.stock_metadata[ticker]["currency"]
            currencies_df[ticker] = xrates.xrates[cur]

        stock_prices_usd = self.daily_stock_prices_local_currency * currencies_df

        return stock_prices_usd


class BenchMarkLoader:
    """Load benchmark indicators"""

    def __init__(self, portfolio_object: object, benchmark_tickers: List):
        self.start_date = portfolio_object.start_date
        self.datetime_index = portfolio_object.datetime_index
        self.benchmarks = benchmark_tickers
        self.benchmark_stock_prices = self.get_benchmark_prices()

    def __repr__(self):
        return f"Benchmarks: {self.benchmarks}"

    def get_benchmark_prices(self):
        """Load benchmark daily prices and infill weekend prices"""

        bm_prices = ffn.get(self.benchmarks, start=self.start_date, clean_tickers=False)
        bm_prices = bm_prices.reindex(self.datetime_index, method="ffill")
        return bm_prices


class CurrencyLoader:
    """Load currency timeseries"""

    # yahoo finance currency codes
    CURRENCIES = {
        "JPY": "JPYUSD=X",
        "EUR": "EURUSD=X",
        "GBP": "GBPUSD=X",
        "USD": "USD=X",
    }

    def __init__(self, datetime_index, positions):
        self.datetime_index = datetime_index
        self.positions = positions
        self.currencies = self._get_currencies()
        self.xrates = self._get_xrates()

    def _get_currencies(self):
        """Get list of currencies present in portfolio"""
        return list(self.positions["currency"].unique())

    def _get_xrates(self):
        """Get daily exchange rates from yahoo finance"""
        try:
            currency_codes = list(map(lambda x: self.CURRENCIES[x], self.currencies))
        except KeyError:
            print(
                "Invalid or unsupported currency."
                f"Currently supported currencies are: {self.CURRENCIES.keys()}"
            )

        xrates = web.DataReader(
            currency_codes,
            "yahoo",
            start=self.datetime_index[0].date(),
        )["Adj Close"]

        xrates = xrates.reindex(self.datetime_index).ffill().bfill()
        xrates.columns = self.currencies
        return xrates
