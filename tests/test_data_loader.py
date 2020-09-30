"""Tests for src.data_loader"""
import datetime
import sys
import pytest

sys.path.append("..")

from src.data_loader import StockPriceLoader


TICKERS = ["NVDA", "INTC", "AMAT", "MKSI", "SNPS", "SOXX", "8035.T", "BESI.AS"]
START_DATE = datetime.datetime(2019, 7, 17)


@pytest.fixture
def load_stock_prices():
    """Load input for testing"""
    return StockPriceLoader(
        input_data_source="./example_inputs/example_purchase_info.csv"
    )


def test_repr(load_stock_prices):
    """Test __repr__"""
    assert str(load_stock_prices) == f"Tickers: {TICKERS}\n Start Date: {START_DATE}"


def test_load_positions(load_stock_prices):
    """Test tickers and start date loaded correctly"""
    assert load_stock_prices.tickers == TICKERS
    assert load_stock_prices.start_date == START_DATE


def test_get_stock_prices(load_stock_prices):
    """Test stock prices loaded correctly"""
    assert load_stock_prices.daily_stock_prices.isnull().sum().sum() == 0
    assert (
        load_stock_prices.daily_stock_prices.index.min() == load_stock_prices.start_date
    )


def test_bad_input(input_data_source="./example_inputs/missing_data.csv"):
    """Test raise ValueError if missing data"""
    with pytest.raises(ValueError):
        StockPriceLoader(input_data_source)


def test_too_many_tickers(input_data_source="./example_inputs/too_many_tickers.csv"):
    """Test raise ValueError if too many tickers"""
    with pytest.raises(ValueError):
        StockPriceLoader(input_data_source)
