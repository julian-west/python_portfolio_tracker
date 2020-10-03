"""Calculate Portfolio Daily Value"""
import pandas as pd

from ppt.data_loader import PositionLoader
from ppt.data_loader import StockPriceLoader


class Stocks(PositionLoader):
    """Calculate daily value of stocks

    Args:
        stock_prices_usd (pd.DataFrame): dataframe with the USD converted daily
            stock price of each ticker in the input csv
        input_data_source (str): location of input csv
    Attributes:
        daily_shares_owned (pd.Series): pd.Series with the number of shares
            owned on each date during the datetime_index
        daily_value_usd (pd.Series): pd.Series with the USD value of the
            portfolio on any given date in the datetime_index
    """

    def __init__(
        self,
        stock_prices_usd,
        input_data_source="../data/raw/purchase_info.csv",
    ):
        super().__init__(input_data_source)

        self.daily_shares_owned = self._get_daily_shares_owned()
        self.daily_stocks_value_usd = self._get_daily_stocks_value_usd(stock_prices_usd)

    def _get_daily_shares_owned(self):
        stock_positions = self.positions[self.positions["yahoo_ticker"] != "cash"]
        daily_shares_owned = (
            stock_positions.pivot(
                index="date", columns="yahoo_ticker", values="total_shares_held"
            )
            .ffill()
            .fillna(0)
            .reindex(self.datetime_index)
            .ffill()
        )

        return daily_shares_owned[self.tickers]

    def _get_daily_stocks_value_usd(self, stock_prices_usd):
        """Get the daily value for each stock in usd"""
        return self.daily_shares_owned * stock_prices_usd


class Cash(PositionLoader):
    """Calculate daily cash position"""

    def __init__(
        self,
        input_data_source: str = "../data/raw/purchase_info.csv",
    ):
        super().__init__(input_data_source)
        self.starting_cash_balance = self._get_starting_balance()
        self.cash_flows = self._calc_daily_cash_balance()
        self.daily_cash_balance = self.cash_flows["pf_cash_balance"]

    def _get_starting_balance(self):
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

        cashflows_df = pd.DataFrame(self.datetime_index).set_index(0)
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

        return cashflows_df.rename_axis("date", axis=0)


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

        self.stocks = Stocks(self.daily_stock_prices_usd, input_data_source)
        self.cash = Cash(input_data_source=input_data_source)
        self.portfolio_value_usd = self._get_daily_portfolio_value_usd()

    def __repr__(self):
        # //TODO - make an informative repr
        return str(self.stock_metadata)

    def _get_daily_portfolio_value_usd(self):
        """Calculate the daily value of the portfolio in USD"""
        return pd.concat(
            [self.stocks.daily_stocks_value_usd, self.cash.daily_cash_balance], axis=1
        ).sum(axis=1)
