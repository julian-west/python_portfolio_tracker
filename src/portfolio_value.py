"""Calculate Portfolio Daily Value"""
import pandas as pd

from src.data_loader import PositionLoader
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
        self.metadata = self._get_stock_metadata()
        self.daily_shares_owned = self._get_daily_number_of_shares_owned()
        self.daily_value_usd = self._get_daily_value_usd()

    def _get_stock_purchase_info(self, ticker):
        """Filter all positions for single stock"""
        return self.positions[self.positions["yahoo_ticker"] == ticker]

    def _get_daily_stock_price(self, ticker):
        """Get the daily stock price for the given stock"""
        return self.daily_stock_prices[ticker]

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


class CalculateCashBalance(PositionLoader):
    """Calculate daily cash position"""

    def __init__(
        self,
        input_data_source: str = "../data/raw/purchase_info.csv",
    ):
        super().__init__(input_data_source)
        self.starting_cash_balance = self.get_starting_balance()
        self.cash_flows = self._calc_daily_cash_balance()
        self.daily_cash_balance = self.cash_flows["pf_cash_balance"]

    def get_starting_balance(self):
        """Get starting cash balance"""
        assert self.positions.iloc[0]["action"] == "CASH IN", self.positions.iloc[0][
            "action"
        ]
        return self.positions.iloc[0]["total_usd"]

    def _calc_daily_cash_balance(self):
        def _calc_cash_changes(self, flags):

            filtered_positions = self.positions[
                self.positions["action"].isin(flags)
            ].set_index("date")
            return (
                filtered_positions.groupby(filtered_positions.index)["total_usd"]
                .sum()
                .reindex(self.datetime_index)
                .fillna(0)
                .values
            )

        def _calc_portfolio_cash_change(row):
            return (
                row["inflows"]
                + row["pf_cash_increase"]
                - row["outflows"]
                - row["pf_cash_decrease"]
            )

        cashflows_df = pd.DataFrame(self.datetime_index)
        cashflows_df["inflows"] = _calc_cash_changes(self, flags=["CASH IN"])
        cashflows_df["outflows"] = _calc_cash_changes(self, flags=["CASH OUT"])
        cashflows_df["pf_cash_increase"] = _calc_cash_changes(self, flags=["SELL"])
        cashflows_df["pf_cash_decrease"] = _calc_cash_changes(self, flags=["BUY"])
        cashflows_df["cash_balance_change"] = cashflows_df.apply(
            _calc_portfolio_cash_change, axis=1
        )
        cashflows_df["pf_cash_balance"] = cashflows_df["cash_balance_change"].cumsum()
        cashflows_df["external_cashflows"] = (
            cashflows_df["inflows"] - cashflows_df["outflows"]
        ).cumsum()

        return cashflows_df.set_index(0).rename_axis("date", axis=0)


class Portfolio(StockPriceLoader):
    """Portfolio stats and info

    Inherits attributes from `StockPriceLoader` and `CalculateStockValue`

    Args:
        input_data_source (str): location of csv with purchase info

    Attributes:
        stock_objects (Dict): dictionary with stock specific information (see
            CalculateStockValue for all attributes)
        combined_daily_value (pd.DataFrame): single dataframe with a column for
            each ticker showing the total value of the position in the stock for
            any given day
        combined_daily_shares (pd.DataFrame): single dataframe with a column for
            each ticker showing the total number of shares owned for each stock
            on any given day

    """

    def __init__(self, input_data_source: str = "../data/raw/purchase_info.csv"):
        super().__init__(input_data_source)

        self.stock_objects = self._create_stock_objects()
        self.cash = CalculateCashBalance(input_data_source=self.input_data_source)
        self.combined_daily_value = self._combine_stock_properties(
            stock_property="daily_value_usd"
        )
        self.combined_daily_shares = self._combine_stock_properties(
            stock_property="daily_shares_owned"
        )
        self.daily_portfolio_value = self._calc_daily_portfolio_value()

    def _create_stock_objects(self):

        stock_objs_dict = {}
        for ticker in self.tickers:
            stock_objs_dict[ticker] = CalculateStockValue(
                ticker, self.input_data_source
            )

        return stock_objs_dict

    def _combine_stock_properties(self, stock_property: str):
        """Combine individual stock properties into single dataframe"""
        combined_df = pd.DataFrame(self.datetime_index)
        for ticker, stock_obj in self.stock_objects.items():
            combined_df[ticker] = getattr(stock_obj, stock_property).values

        if stock_property == "daily_value_usd":
            combined_df["cash_balance"] = self.cash.cash_flows["pf_cash_balance"].values

        return combined_df.set_index(0).rename_axis("date", axis=0)

    def _calc_daily_portfolio_value(self):
        return self.combined_daily_value.sum(axis=1)
