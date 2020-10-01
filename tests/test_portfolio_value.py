"""Test portfolio_value.py classes and functions"""

from src.portfolio_value import CalculateStockValue
from src.portfolio_value import calc_portfolio_value

TICKER = "NVDA"


class TestCalculateStockValue:
    """Test CalculateStockValue class"""

    def test__get_stock_metadata(self, nvda_stock_value):
        """Test output of stock metadata"""
        assert nvda_stock_value.metadata["company"] == "Nvidia"
        assert nvda_stock_value.metadata["yahoo_ticker"] == "NVDA"
        assert nvda_stock_value.metadata["currency"] == "USD"


def test_calc_portfolio_value():
    """Test calc_portfolio_value"""
    assert calc_portfolio_value(
        input_data_source="./tests/example_inputs/example_purchase_info.csv"
    )
