"""Test portfolio_value.py classes and functions"""

from ppt.portfolio_value import Portfolio

from .conftest import EXAMPLE_INPUT_DATA


class TestStocks:
    """Test Stocks class"""

    pass


class TestCash:
    """Test Cash class"""

    pass


class TestPortfolio:
    """Test portfolio class"""

    def test_portfolio(self):
        assert Portfolio(
            input_data_source="/".join([EXAMPLE_INPUT_DATA, "purchase_info.csv"])
        )
