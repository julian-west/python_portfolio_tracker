"""Project wide fixtures and constant variables"""
import datetime

import pytest

from ppt.data_loader import (
    BenchmarkLoader,
    CurrencyLoader,
    PositionLoader,
    StockPriceLoader,
)

EXAMPLE_INPUT_DATA = "./tests/example_inputs/"
TEST_DATAFRAMES = "".join([EXAMPLE_INPUT_DATA, "test_dataframes/"])

EXAMPLE_TICKER = "NVDA"
EXAMPLE_BENCHMARK = "^GSPC"
TICKERS = ["8035.T", "BESI.AS", "INTC", "AMAT", "MKSI", "SNPS", "SOXX", "NVDA"]
START_DATE = datetime.datetime(2019, 7, 17)
CURRENCIES = ["USD", "JPY", "EUR"]


@pytest.fixture
def positions():
    """Load Positions"""
    return PositionLoader(
        input_data_source="".join([EXAMPLE_INPUT_DATA, "purchase_info.csv"])
    )


@pytest.fixture
def stock_prices():
    """Load input for testing"""
    return StockPriceLoader(
        input_data_source="".join([EXAMPLE_INPUT_DATA, "purchase_info.csv"])
    )


@pytest.fixture
def benchmarks():
    """Load benchmarks for testing"""
    return BenchmarkLoader(
        input_data_source="".join(
            [EXAMPLE_INPUT_DATA, "purchase_info.csv"],
        ),
        benchmark_tickers=EXAMPLE_BENCHMARK,
    )


@pytest.fixture
def currency():
    """Load currencies for testing"""
    return CurrencyLoader(
        input_data_source="".join([EXAMPLE_INPUT_DATA, "purchase_info.csv"])
    )
