# Python Portfolio Tracker

Currently a work in progress...🏗️

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.org/julian-west/python_portfolio_tracker.svg?branch=master)](https://travis-ci.org/julian-west/python_portfolio_tracker)
[![codecov](https://codecov.io/gh/julian-west/python_portfolio_tracker/branch/master/graph/badge.svg)](https://codecov.io/gh/julian-west/python_portfolio_tracker)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/ambv/black)

Track the performance of your portfolio using Python!

## Key Features

- download stock prices and calculate the daily value of your stock positions from a simple input csv of buy/sell positions
- conduct in-depth analysis of your overall portfolio performance and individual stocks e.g. mean-variance, correlations, max drawdown, position weightings, profit contributions etc.

## Problems this repo solves

Online broker accounts tend to give generalised statistics about portfolio (or individual stock) performance. It can be difficult to easily download any source data to do your own in depth analysis on the performance of any individual positions and the overall risk return profile of the portfolio. Furthermore, if you have accounts with multiple brokers it is very difficult and time consuming to complete an analysis of all your positions.

Using a simple list of buy/sell positions in a csv file as input, this repo aims to allow the user to efficiently collect daily stock price data, calculate the value of their portfolio over time and complete custom in depth analysis of positions (e.g mean-variance, correlations, etc.).a

## How to use

1. Fork this repo, clone to local computer and create a virtual environment

```bash
# could alternatively use virtualenv
conda create --name python-portfolio-tracker --file requirements.txt

```

2. Upload your input data containing the list of buy/sell actions in your portfolio (using the correct format specified in the [Data Input Format](#dif) below). The default location for the input data is: `data/raw/purchase_info.csv`, however, you can upload it anywhere and just reference the location (`input_data_source`) in the load data functions.

<a id='dif'></a>

### Data Input Format

The required data input for this analysis is a `csv` file containing rows for each purchase (or disposal) of a stock in your portfolio. An example is given in the `../data/raw/purchase_info.csv` in this repository.

The required columns are:

- `date`: the date of your transaction
- `action`: BUY or SELL
- `company`: the name of the company (this is not sensitive to any further analysis and can be anything of your choosing)
- `yahoo_ticker`: the ticker of the stock on finance.yahoo.com (note this might be different from the actual stock market ticker)
- `currency`: the currency the stock price is denominated in
- `num_shares`: the number of shares involved in the transaction
- `stock_price_usd`: the stock price you bought the stock at on that day
- `trading_costs_usd`: the trading costs incurred
- `total_usd`: the total cost of the transaction
- `total_shares_held`: the total number of shares held after the transaction

Example input format:

|    | date       | action   | company           | yahoo_ticker   | currency   |   num_shares |   stock_price_usd |   trading_costs_usd |   total_usd |   total_shares_held |
|---:|:-----------|:---------|:------------------|:---------------|:-----------|-------------:|------------------:|--------------------:|------------:|--------------------:|
|  0 | 17/07/2019 | BUY      | Nvidia            | NVDA           | USD        |           39 |          166.67   |                4.95 |     6505.08 |                  39 |
|  1 | 17/07/2019 | BUY      | Intel             | INTC           | USD        |          180 |           49.91   |                4.95 |     8988.75 |                 180 |
|  2 | 17/07/2019 | BUY      | Applied Materials | AMAT           | USD        |          268 |           45.9151 |                4.95 |    12310.2  |                 268 |
|  3 | 17/07/2019 | BUY      | MKS Instruments   | MKSI           | USD        |          120 |           76.7449 |                4.95 |     9214.34 |                 120 |
|  4 | 17/07/2019 | BUY      | Synopsys          | SNPS           | USD        |           68 |          136.808  |                4.95 |     9307.92 |                  68 |
|  5 | 17/07/2019 | BUY      | SOXX ETF          | SOXX           | USD        |           75 |          204.261  |                4.95 |    15324.5  |                  75 |
|  6 | 26/11/2019 | SELL     | Nvidia            | NVDA           | USD        |            5 |          217      |                4.95 |     1089.95 |                  34 |
|  7 | 25/03/2020 | BUY      | Nvidia            | NVDA           | USD        |           10 |          205.75   |                4.95 |     2062.45 |                  44 |

## Current limitations

- Only available for USD denominated stocks (I may put in a currency converter in the future)
- Data processing and analysis is completed in memory which may not scale we to portfolios with many different positions
- Stock price data is loaded from `yahooFinance` (using the `ffn` library), the veracity of this data source may not be 100% and it can also take a long time to load data

## Running Tests

PyTest is used for running tests in this project. If running on Linux or Mac and you have `Make` installed you can run tests using the `make test` command from the Makefile.

Alternatively, tests can be run using `pytest` directly using the following command:

```bash
pytest --cov-config=.coveragerc --cov=src
```

## Further work

- User input through webapp rather than csv/Jupyter Notebooks
- Account for dividend payments
