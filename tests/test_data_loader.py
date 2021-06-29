"""Tests for ppt.data_loader"""

import numpy as np
import pandas as pd

from .conftest import CURRENCIES, START_DATE, TEST_DATAFRAMES, TICKERS


def load_and_assert_testing_df(object, attribute, test_df, precision=3):
    """Load a test dataframe and assert index and values are equal

    Args:
        object (obj): object to test
        attribute (str): string name of attribute to test
        test_df (str): filename of test dataframe to load
        precision (int): number of decimal places the dataframes should be equal

    """

    test_df = pd.read_csv(
        "".join(
            [
                TEST_DATAFRAMES,
                test_df,
            ]
        ),
        index_col=[0],
        parse_dates=[0],
    )

    rows = len(test_df)
    attribute_value = getattr(object, attribute)

    np.testing.assert_array_equal(
        test_df.index.values,
        attribute_value.head(rows).index.values,
    )

    np.testing.assert_array_almost_equal(
        test_df.values,
        attribute_value.head(rows).values,
        decimal=3,
    )


class TestPositionLoader:
    """Test the PositionLoader class"""

    def test_tickers(self, positions):
        """Assert the correct tickers are present"""
        assert sorted(positions.tickers) == sorted(TICKERS)

    def test_start_date(self, positions):
        """Assert the correct start_date"""
        assert positions.start_date == START_DATE

    def test_stock_metadata(self, positions):
        """Assert correct metadata format"""
        assert sorted(positions.stock_metadata.keys()) == sorted(positions.tickers)
        assert positions.stock_metadata["INTC"] == {
            "company": "Intel",
            "currency": "USD",
        }


class TestStockPriceLoader:
    """Test the StockPriceLoader Class"""

    def test_daily_stock_prices_local_currency(self, stock_prices):
        """Assert correct stock price loading"""
        load_and_assert_testing_df(
            stock_prices,
            "daily_stock_prices_local_currency",
            "StockPriceLoader_daily_stock_prices_local_currency.csv",
        )

    def test_daily_stock_prices_usd(self, stock_prices):
        """Assert correct USD conversion"""
        load_and_assert_testing_df(
            stock_prices,
            "daily_stock_prices_usd",
            "StockPriceLoader_daily_stock_prices_usd.csv",
        )


class TestBenchmarkLoader:
    """Test benchmark loader"""

    def test_benchmark_stock_prices(self, benchmarks):
        load_and_assert_testing_df(
            benchmarks,
            "benchmark_stock_prices",
            "BenchMarkLoader_benchmark_stock_prices.csv",
        )


class TestCurrencyLoader:
    """Test currency loader"""

    def test_currencies(self, currency):
        """Test currencies extracted correctly"""
        assert sorted(CURRENCIES) == sorted(currency.currencies)

    def test_xrates(self, currency):
        """Test currency xrates load correctly"""
        load_and_assert_testing_df(currency, "xrates", "CurrencyLoader_xrates.csv")
