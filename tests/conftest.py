"""Project wide fixtures"""

import pytest
from src.data_loader import StockPriceLoader
from src.portfolio_value import CalculateStockValue

INPUT_DATA_SOURCE = "./tests/example_inputs/example_purchase_info.csv"
EXAMPLE_TICKER = "NVDA"


@pytest.fixture
def prices():
    """Load input for testing"""
    return StockPriceLoader(input_data_source=INPUT_DATA_SOURCE)


@pytest.fixture
def nvda_stock_value():
    """Load stock value class for an example ticker"""
    return CalculateStockValue(
        ticker=EXAMPLE_TICKER, input_data_source=INPUT_DATA_SOURCE
    )
