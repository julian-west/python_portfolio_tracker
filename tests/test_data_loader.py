"""Tests for src.data_loader"""
import datetime
import pytest

from src.data_loader import StockPriceLoader


TICKERS = ["NVDA", "INTC", "AMAT", "MKSI", "SNPS", "SOXX"]
START_DATE = datetime.datetime(2019, 7, 17)


def test_repr(prices):
    """Test __repr__"""
    assert str(prices) == f"Tickers: {TICKERS}\nStart Date: {START_DATE}"


def test_load_positions(prices):
    """Test tickers and start date loaded correctly"""
    assert prices.tickers == TICKERS
    assert prices.start_date == START_DATE


def test_get_stock_prices(prices):
    """Test stock prices loaded correctly"""
    assert prices.daily_stock_prices.isnull().sum().sum() == 0
    assert prices.daily_stock_prices.index.min() == prices.start_date


def test_bad_input(input_data_source="./tests/example_inputs/missing_data.csv"):
    """Test raise ValueError if missing data"""
    with pytest.raises(ValueError):
        StockPriceLoader(input_data_source)


def test_too_many_tickers(
    input_data_source="./tests/example_inputs/too_many_tickers.csv",
):
    """Test raise ValueError if too many tickers"""
    with pytest.raises(ValueError):
        StockPriceLoader(input_data_source)
