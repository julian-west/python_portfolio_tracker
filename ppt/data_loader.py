"""Load Stock Prices"""
import datetime
from typing import List
import pandas as pd
import pandas_datareader as web
import ffn

TODAY = datetime.datetime.now().date()


class PositionLoader:
    """Load positions input data

    Args:
        input_data_source (str): the location of the input csv. Default value
            is '../data/raw/purchase_info.csv'

    Attributes:
        input_data_source (str): location of specified data source
        positions (pd.DataFrame): dataframe of loaded csv datasource
        tickers (list): list of unique tickers in the input data source
        start_date (Timestamp): date of first purchase/cash injection
        datetime_index (pd.DateTimeIndex): a continuous datetime index starting
            at 'start_date' running up until today's date.
        stock_metadata (Dict): a dictionary containing some metadata for each
            stock. e.g. {'MSFT': {'company': 'Microsoft','currency':'USD'}}

    """

    def __init__(self, input_data_source: str = "../data/raw/purchase_info.csv"):
        self.input_data_source = input_data_source
        self.positions = self._load_positions()
        self.tickers = self._get_tickers()
        self.start_date = self._get_start_date()
        self.datetime_index = self._generate_datetime_index()
        self.stock_metadata = self._extract_metadata()

    def _load_positions(self):
        """Load positions from input_data_source

        //TODO Data input validation
        """
        return pd.read_csv(self.input_data_source, parse_dates=["date"])

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
            of ticker symbols. Default is 'data/raw/purchase_info.csv'

    Attributes:
        daily_stock_prices_local_currency (pd.DataFrame): daily adjusted closing
            stock prices in their local currency from yahoo finance for all
            tickers present in the input csv
        daily_stock_prices_usd (pd.DataFrame): daily closing stock prices
            converted to USD

    """

    def __init__(self, input_data_source: str = "../data/raw/purchase_info.csv"):
        super().__init__(input_data_source)
        self.daily_stock_prices_local_currency = self._get_stock_prices_local_currency()
        self.daily_stock_prices_usd = self._get_stock_prices_usd()

    def __repr__(self):
        return f"Tickers: {sorted(self.tickers)}\nStart Date: {str(self.start_date)}"

    def _get_stock_prices_local_currency(self):
        """Load stock prices (in local currency) from list of tickers"""

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
        xrates = CurrencyLoader(self.input_data_source)

        currencies_df = pd.DataFrame(self.datetime_index).set_index(0)
        for ticker in self.tickers:
            cur = self.stock_metadata[ticker]["currency"]
            currencies_df[ticker] = xrates.xrates[cur]

        stock_prices_usd = self.daily_stock_prices_local_currency * currencies_df

        return stock_prices_usd


class BenchmarkLoader(PositionLoader):
    """Load benchmark indicators

    Note currently only supports USD benchmarks

    Args:
        benchmark_tickers (List): str or list of tickers to load as benchmarks
        input_data_source (str): location of input datasource

    Attributes:
        benchmarks (List): list of benchmarks
        benchmark_stock_prices (pd.DataFrame): dataframe with list of daily
            stock prices for the benchmarks

    """

    def __init__(
        self,
        benchmark_tickers: List,
        input_data_source: str = "../data/raw/purchase_info.csv",
    ):
        super().__init__(input_data_source)
        self.benchmarks = benchmark_tickers
        self.benchmark_stock_prices = self.get_benchmark_prices()

    def __repr__(self):
        return f"Benchmarks: {self.benchmarks}"

    def get_benchmark_prices(self):
        """Load benchmark daily prices and infill weekend prices"""

        bm_prices = ffn.get(self.benchmarks, start=self.start_date, clean_tickers=False)
        bm_prices = bm_prices.reindex(self.datetime_index, method="ffill")
        return bm_prices


class CurrencyLoader(PositionLoader):
    """Load currency timeseries

    Args:
        input_data_source: location of input data source

    Attributes:
        CURRENCIES (Dict): constant. Dictionary with supported currencies and
            there corresponding yahoo finance code
        currencies (list): list of currencies present in the portfolio
        xrates (pd.DataFrame): dataframe containing the daily exchange rates for
            each unique currency in the input csv
    """

    # yahoo finance currency codes
    CURRENCIES = {
        "JPY": "JPYUSD=X",
        "EUR": "EURUSD=X",
        "GBP": "GBPUSD=X",
        "USD": "USD=X",
    }

    def __init__(self, input_data_source: str = "../data/raw/purchase_info.csv"):
        super().__init__(input_data_source)
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
