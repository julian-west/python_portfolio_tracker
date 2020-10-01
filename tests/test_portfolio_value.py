"""Test portfolio_value.py classes and functions"""

from src.portfolio_value import CalculateStockValue

TICKER = "NVDA"


def test__get_stock_metadata(nvda_stock_value):
    """Test output of stock metadata"""
    assert nvda_stock_value.metadata["company"] == "Nvidia"
    assert nvda_stock_value.metadata["yahoo_ticker"] == "NVDA"
    assert nvda_stock_value.metadata["currency"] == "USD"

