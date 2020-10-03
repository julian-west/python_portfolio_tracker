"""Project wide fixtures and constant variables"""
import datetime
import pytest
from ppt.data_loader import StockPriceLoader

EXAMPLE_INPUT_DATA_SOURCE = "./tests/example_inputs/example_purchase_info.csv"
EXAMPLE_TICKER = "NVDA"
TICKERS = ["INTC", "AMAT", "MKSI", "SNPS", "SOXX", "NVDA"]
START_DATE = datetime.datetime(2019, 7, 17)


@pytest.fixture
def prices():
    """Load input for testing"""
    return StockPriceLoader(input_data_source=EXAMPLE_INPUT_DATA_SOURCE)
