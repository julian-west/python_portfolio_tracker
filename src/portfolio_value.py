"""Calculate Portfolio Daily Value"""

import datetime
import pandas as pd

from src.data_loader import StockPriceLoader


class CalculateStockValue(StockPriceLoader):
    """Calculate individual stock value

    Args:
        ticker (str): ticker of the stock to analyse

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
            self.stock_purchase_info["date"].min(),
            end=datetime.datetime.now().date(),
            freq="D",
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
