"""Calculate Portfolio Daily Value"""
import pandas as pd

from ppt.data_loader import BenchmarkLoader, PositionLoader, StockPriceLoader


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
    """Calculate daily cash position

    Args:
        input_data_source: location of input data

    Attributes:
        starting_cash_balance (int): original cash injected into portfolio
        cash_flows (pd.DataFrame): dataframe containing cash flow information
        daily_cash_balance (pd.Series): daily cash balance

    """

    def __init__(
        self,
        input_data_source: str = "../data/raw/purchase_info.csv",
    ):
        super().__init__(input_data_source)
        self.starting_cash_balance = self._get_starting_balance()
        self.cash_flows = self._calc_cash_flows()
        self.daily_cash_balance = self.cash_flows["pf_cash_balance"]
        self.external_cashflows = self.cash_flows["external_cashflows"]

    def _get_starting_balance(self):
        """Get starting cash balance"""
        assert self.positions.iloc[0]["action"] == "CASH IN", self.positions.iloc[0][
            "action"
        ]
        return self.positions.iloc[0]["total_usd"]

    def _calc_cash_flows(self):
        """Calculate portfolio cashflows"""

        def _calc_cash_changes(self, flags):
            """Calculate changes in cash position from buying/selling"""
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
            """Calculate change in portfolio cash"""
            return (
                row["inflows"]
                + row["pf_cash_increase"]
                - row["outflows"]
                - row["pf_cash_decrease"]
            )

        cashflows_df = pd.DataFrame(self.datetime_index).set_index(0)

        for col, flag in zip(
            ["inflows", "outflows", "pf_cash_increase", "pf_cash_decrease"],
            ["CASH IN", "CASH OUT", "SELL", "BUY"],
        ):
            cashflows_df[col] = _calc_cash_changes(self, flags=[flag])

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

    Args:
        input_data_source (str): location of csv with purchase info

    Attributes:
        stocks (object): Stock prices and daily stock values. See `Stocks` class
        cash (object): Cash balance. See `Cash` class
        portfolio_value_usd (pd.Series): daily total portfolio value
        benchmark (object): Benchmark stock prices

    """

    def __init__(self, input_data_source: str = "../data/raw/purchase_info.csv"):
        super().__init__(input_data_source)

        self.stocks = Stocks(self.daily_stock_prices_usd, input_data_source)
        self.cash = Cash(input_data_source=input_data_source)
        self.portfolio_value_usd = self._get_daily_portfolio_value_usd()
        self.profit = self._get_running_profit()
        self.benchmark = None

    def __repr__(self):
        # //TODO - make an informative repr
        return str(self.stock_metadata)

    def _get_daily_portfolio_value_usd(self):
        """Calculate the daily value of the portfolio in USD"""
        return pd.concat(
            [self.stocks.daily_stocks_value_usd, self.cash.daily_cash_balance], axis=1
        ).sum(axis=1)

    def _get_running_profit(self):
        """Calculate profit"""
        return self.portfolio_value_usd - self.cash.external_cashflows

    def add_benchmark(self, benchmark_tickers):
        """Add a benchmark"""
        self.benchmark = BenchmarkLoader(benchmark_tickers, self.input_data_source)
