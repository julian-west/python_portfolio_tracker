"""Tests for ppt.data_loader"""
import datetime
import pytest

from ppt.data_loader import StockPriceLoader

from .conftest import TICKERS, START_DATE


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
