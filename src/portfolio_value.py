"""Calculate Portfolio Daily Value"""
from typing import Dict
from datetime import datetime
import pandas as pd

from src.data_loader import StockPriceLoader


class CalculateStockValue(StockPriceLoader):
    """Calculate individual stock value

    Args:
        ticker (str): ticker of the stock to analyse

    Attributes:
        stock_purchase_info (pd.DataFrame): dataframe with purchase info,
            filtered for specified ticker
        daily_stock_price (pd.Series): pd.Series containing stock price for the
            specified ticker
        datetime_index (pd.DatetimeIndex): index with list of dates at a daily
            frequency starting from the first stock price dates to today
        metadata (Dict): dictionary with stock company name, ticker and currency
        daily_shares_owned (pd.Series): pd.Series with the number of shares
            owned on each date during the datetime_index
        daily_value_usd (pd.Series): pd.Series with the USD value of the
            portfolio on any given date in the datetime_index
    """

    def __init__(
        self, ticker: str, input_data_source: str = "../data/raw/purchase_info.csv"
    ):
        super().__init__(input_data_source)

        self.stock_purchase_info = self._get_stock_purchase_info(ticker)
        self.daily_stock_price = self._get_daily_stock_price(ticker)
        self.datetime_index = self._generate_datetime_index()
        self.metadata = self._get_stock_metadata()
        self.daily_shares_owned = self._get_daily_number_of_shares_owned()
        self.daily_value_usd = self._get_daily_value_usd()

    def _get_stock_purchase_info(self, ticker):
        """Filter all positions for single stock"""
        return self.positions[self.positions["yahoo_ticker"] == ticker]

    def _get_daily_stock_price(self, ticker):
        """Get the daily stock price for the given stock"""
        return self.daily_stock_prices[ticker]

    def _generate_datetime_index(self):
        """Create a datetime index starting from earliest stock purchase date"""
        return pd.date_range(
            self.stock_purchase_info["date"].min(), end=datetime.now().date(), freq="D",
        )

    def _get_stock_metadata(self):
        """Get company, ticker and currency metadata for the stock"""
        return (
            self.stock_purchase_info[["company", "yahoo_ticker", "currency"]]
            .iloc[0]
            .to_dict()
        )

    def _get_daily_number_of_shares_owned(self):
        """Get timeseries with the number of shares held each day"""
        num_shares_held = self.stock_purchase_info.set_index("date")[
            "total_shares_held"
        ]
        return num_shares_held.reindex(self.datetime_index).ffill().fillna(0)

    def _get_daily_value_usd(self):
        """Get usd daily_value"""
        return self.daily_stock_price.mul(self.daily_shares_owned).ffill()

    def _get_daily_value_currency(self):
        """Function to convert non-usd stock prices to usd"""
        raise NotImplemented


def calc_portfolio_value(input_data_source: str = "../data/raw/purchase_info.csv"):
    """Calculate the portfolio value

    Args:
        input_data_source (str): location of csv with purchase info

    Returns:
        stock_prices.daily_stock_prices (pd.DataFrame): raw stock prices for
            each ticker in the input file
        stocks (Dict): dictionary containing `CalculateStockValue` objects for
            each ticker in the input file. These can be used to access stats
            and data for individual stocks
        combined_daily_value (pd.DataFrame): single dataframe which has a column
            for each ticker and its daily value
        combined_daily_shares_owned (pd.DataFrame): single dataframe which has a
            column for each ticker and its daily number of shares

    """

    def combine_stock_properties(
        stock_objs: Dict, start_date: pd.Timestamp, stock_property: str
    ):
        """Combine individual stock properties into single dataframe"""
        combined_df = pd.DataFrame(
            index=pd.date_range(start=start_date, end=datetime.now().date(), freq="D")
        )

        for ticker, stock_obj in stock_objs.items():
            combined_df[ticker] = getattr(stock_obj, stock_property)

        return combined_df

    stock_prices = StockPriceLoader(input_data_source)
    stocks = {}
    for ticker in stock_prices.tickers:
        stocks[ticker] = CalculateStockValue(ticker, input_data_source)

    combined_daily_value = combine_stock_properties(
        stock_objs=stocks,
        start_date=stock_prices.start_date,
        stock_property="daily_value_usd",
    )

    combined_daily_shares_owned = combine_stock_properties(
        stock_objs=stocks,
        start_date=stock_prices.start_date,
        stock_property="daily_shares_owned",
    )

    return (
        stock_prices.daily_stock_prices,
        stocks,
        combined_daily_value,
        combined_daily_shares_owned,
    )
