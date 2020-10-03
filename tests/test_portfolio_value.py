"""Test portfolio_value.py classes and functions"""

from ppt.portfolio_value import CalculateStockValue
from ppt.portfolio_value import Portfolio

from .conftest import EXAMPLE_INPUT_DATA_SOURCE, TICKERS


class TestCalculateStockValue:
    """Test CalculateStockValue class"""

    def test__get_stock_metadata(self, nvda_stock_value):
        """Test output of stock metadata"""
        assert nvda_stock_value.metadata["company"] == "Nvidia"
        assert nvda_stock_value.metadata["yahoo_ticker"] == "NVDA"
        assert nvda_stock_value.metadata["currency"] == "USD"


class TestPortfolio:
    """Test portfolio class"""

    def test_portfolio(self):
        assert Portfolio(input_data_source=EXAMPLE_INPUT_DATA_SOURCE)
