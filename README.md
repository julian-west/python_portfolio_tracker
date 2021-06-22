# Python Portfolio Tracker (ppt)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.org/julian-west/python_portfolio_tracker.svg?branch=master)](https://travis-ci.org/julian-west/python_portfolio_tracker)
[![codecov](https://codecov.io/gh/julian-west/python_portfolio_tracker/branch/master/graph/badge.svg)](https://codecov.io/gh/julian-west/python_portfolio_tracker)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-black.svg)](https://github.com/ambv/black)

Track the performance of your portfolio using Python!

---
**Currently under construction... :construction::building_construction:**

Progress:

- Data loading
    - [x] Load positions from input csv containing BUY/SELL actions
    - [x] Load stock prices for positions in input csv
    - [x] Add support for :us:, :gb:, :eu: and :jp: stocks
    - [x] Convert foriegn stocks to USD to calculate total portfolio value in USD
    - [ ] Load dividend payments for each stock
    - [ ] Robust data input validation

- Portfolio Analysis
    - [ ] Calculate time-weighted portfolio performance
    - [ ] Calculate total return for each holding
    - [ ] Calculate overall portfolio performance metrics
    - [ ] Calculate individual stock performance metrics

---

## Key Features

- simple input format: list of buy and sell positions in csv format 
- automatically calculate the daily value of your portfolio, your stock positions and cash balance from the input list of buy/sell actions
- adjust for regular cash injections (e.g. monthly contributions to the portfolio)
- compatible for US, EU, JP and GB listed stocks
- quickly conduct an in-depth analysis of your overall portfolio performance or individual stocks using inbuilt functions (e.g. mean-variance, correlations, max drawdown, position weightings, profit contributions etc.) or use the base raw data for your own further analysis

## Problems this library aims to solves

Online brokerage accounts only provide high level 'one-size-fits-all' metrics on your portfolio performance and (generally) do not give you access to the underlying raw data.

This makes it difficult to run custom analyses on your positions and understand the true performance of the portfolio, your overall stock/cash positions and any potential risks (correlations) between individual stock positions. This is especially a problem if you have multiple brokeage accounts.

Furthermore, most other Python libraries do not account for regular cash injections (e.g. monthly contributions to the portfolio). This makes it hard to evaluate the true performance of your portfolio.

Using a simple list of buy/sell positions in a csv file as input, this repo aims to allow the user to efficiently collect daily stock price data, calculate the value of their portfolio over time and use the raw data to complete custom in depth analysis of positions (e.g mean-variance, correlations, etc.).

## QuickStart

1. Fork this repo, clone to local computer and create a virtual environment

    ```bash
    # could alternatively use virtualenv
    conda create --name python-portfolio-tracker --file requirements.txt

    ```

2. Upload your input data containing the list of buy/sell actions in your portfolio (using the correct format specified in the [Data Input Format](#dif) below). The default location for the input data is: `data/raw/purchase_info.csv`, however, you can upload it anywhere and just reference the location (`input_data_source`) in the load data functions.

3. Load stock price data and calculate daily running portfolio and stock position values

    ```python
    from ppt.portfolio_value import Portfolio

    # load portfolio data from input csv located in 'data/raw/purchase_info.csv
    pf = Portfolio()

    # get daily portfolio value
    pf.portfolio_value_usd

    ```

4. Use the raw stock price and portfolio value data contained in the `Portfolio` object to analyse your stock portfolio (in built library functions to analyse the portfolio are to come in the future...)

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

### Key Input Requirements

- cash inflows and outflows (new cash injected into the portfolio and cash removed from the portfolio) should be recorded using `CASH IN` and `CASH OUT` labels in the `action` column
- the first entry of the input csv should be a `CASH IN` action which denotes the starting cash balance (before any stocks were bought)  

Example input format:

|    | date       | action   | company                     | yahoo_ticker   | currency   |   num_shares |   stock_price_usd |   trading_costs_usd |   total_usd |   total_shares_held |
|---:|:-----------|:---------|:----------------------------|:---------------|:-----------|-------------:|------------------:|--------------------:|------------:|--------------------:|
|  0 | 17/07/2019 | CASH IN  | cash                        | cash           | USD        |            0 |       100000      |                0    |   100000    |                   0 |
|  1 | 17/07/2019 | BUY      | Intel                       | INTC           | USD        |          180 |           49.91   |                4.95 |     8988.75 |                 180 |
|  2 | 17/07/2019 | BUY      | Applied Materials           | AMAT           | USD        |          268 |           45.9151 |                4.95 |    12310.2  |                 268 |
|  3 | 17/07/2019 | BUY      | MKS Instruments             | MKSI           | USD        |          120 |           76.7449 |                4.95 |     9214.34 |                 120 |
|  4 | 17/07/2019 | BUY      | Synopsys                    | SNPS           | USD        |           68 |          136.808  |                4.95 |     9307.92 |                  68 |
|  5 | 17/07/2019 | BUY      | SOXX ETF                    | SOXX           | USD        |           75 |          204.261  |                4.95 |    15324.5  |                  75 |
|  6 | 18/07/2019 | BUY      | Nvidia                      | NVDA           | USD        |           39 |          166.67   |                4.95 |     6505.08 |                  39 |
|  7 | 24/07/2019 | BUY      | Tokyo Electron              | 8035.T         | JPY        |          100 |          168.413  |              126.31 |    16967.7  |                 100 |
|  8 | 24/07/2019 | BUY      | BE Semiconductor Industries | BESI.AS        | EUR        |          420 |           29.9253 |              100    |    12668.6  |                 420 |
|  9 | 26/11/2019 | SELL     | Nvidia                      | NVDA           | USD        |            5 |          217      |                4.95 |     1089.95 |                  34 |
| 10 | 25/12/2019 | CASH IN  | cash                        | cash           | USD        |            0 |        10000      |                0    |    10000    |                   0 |
| 11 | 25/03/2020 | BUY      | Nvidia                      | NVDA           | USD        |           10 |          205.75   |                4.95 |     2062.45 |                  44 |
| 12 | 25/05/2020 | CASH OUT | cash                        | cash           | USD        |            0 |         5000      |                0    |     5000    |                   0 |

## Current limitations

- Only available for stocks which have stock price information available on yahoo finance
- Data processing and analysis is completed in memory which may not scale we to portfolios with many different positions
- Stock price data is loaded from `yahooFinance` (using the `ffn` library), the veracity of this data source may not be 100%
- The library currently does not track dividend payments

## Further work

- release as a PyPI library
- User input through webapp rather than csv/Jupyter Notebooks
- Account for dividend payments
- Link to a dashboard to visualise the analysis

---

## Running Tests

PyTest is used for running tests in this project. If running on Linux or Mac and you have `Make` installed you can run tests using the `make test` command from the Makefile.

Alternatively, tests can be run using `pytest` directly using the following command from the home working directory:

```bash
pytest --cov-config=.coveragerc --cov=ppt
```
