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

// TODO

### Data Input Format

//TODO

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
