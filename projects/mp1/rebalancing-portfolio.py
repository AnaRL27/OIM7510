# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of project, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Target users could include day traders, retail investors,investment fund managers and generally anyone who invests in the stock market. The ability to balance a portfolio allows these users to allocate resources according to a set of goals/ investment criteria.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Step 1:  Find the market value of each holding by multipying price times number of shares
    Step 2: Add up all of those values to know what the value of your holdings is
    Step 3: Add 5,000 in cash to the total value of your holdings to get the total portfolio value
    Step 4: Multiply portfolio value times the target weights to get the target value of each holding
    Step 5: Find out how many sahres you need to own in order to have the target portfolio by dividing the market value by the price
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Question 1: The loop carries the cash balance of $5,000 and it updates based the stocks peformance
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Question 2: Sum of holdings should be equal to portfolio minus your cash. Your weights should always equal 100 and cash is greater than or equal to 0
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your project from the Mini Project 1 page. If you chose your own project, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    holdings = [
        ("AAPL", 100, 173.93),
        ("MSFT", 50, 319.53),
        ("GOOG", 80, 131.36),
        ("AMZN", 200, 129.33),
        ("NVDA", 20, 410.17),
        ("TSLA", 150, 255.70),
    ]
    cash = 5000.00
    target_weights = {"AAPL": 0.20, "MSFT": 0.20, "GOOG": 0.15,
                      "AMZN": 0.15, "NVDA": 0.15, "TSLA": 0.15}
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _():
    holdings = [
        ("AAPL", 100, 173.93),
        ("MSFT", 50, 319.53),
        ("GOOG", 80, 131.36),
        ("AMZN", 200, 129.33),
        ("NVDA", 20, 410.17),
        ("TSLA", 150, 255.70),
    ]
    return (holdings,)


@app.cell
def _():
    cash = 5000.00
    return (cash,)


@app.cell
def _():
    target_weights = {"AAPL": 0.20, "MSFT": 0.20, "GOOG": 0.15,
                      "AMZN": 0.15, "NVDA": 0.15, "TSLA": 0.15}
    return (target_weights,)


@app.cell
def _(cash, holdings):
    holdings_value = 0
    for _ticker, _shares, _price in holdings:
        holdings_value = holdings_value + _shares * _price

    portfolio_value = holdings_value + cash
    portfolio_value
    return (portfolio_value,)


@app.cell
def _(holdings, portfolio_value, target_weights):
    target_shares = []
    shares_to_trade = []
    for _ticker, _shares, _price in holdings:
        _target_value = portfolio_value * target_weights[_ticker]
        _shares_target = int(_target_value // _price)
        target_shares.append(_shares_target)
        shares_to_trade.append(_shares_target - _shares)

    target_shares, shares_to_trade
    return shares_to_trade, target_shares


@app.cell
def _(cash, holdings, shares_to_trade):
    cash_spent = 0
    for _i in range(len(holdings)):
        _ticker, _shares, _price = holdings[_i]
        cash_spent = cash_spent + shares_to_trade[_i] * _price
    cash_left = cash - cash_spent
    cash_left
    return (cash_left,)


@app.cell
def _(holdings, portfolio_value, target_shares, target_weights):
    value_after = []
    weight_after = []
    gap_points = []
    for _i in range(len(holdings)):
        _ticker, _shares, _price = holdings[_i]
        _value = target_shares[_i] * _price
        value_after.append(_value)
        _weight = _value / portfolio_value
        weight_after.append(_weight)
        gap_points.append(abs(_weight - target_weights[_ticker]) * 100)

    value_after, weight_after, gap_points
    return gap_points, value_after, weight_after


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(
    cash_left,
    gap_points,
    holdings,
    shares_to_trade,
    target_shares,
    value_after,
    weight_after,
):
    print(f"{'Ticker':<8}{'Shares Now':>12}{'Shares Target':>15}{'Shares to Trade':>18}{'Value After':>15}{'Weight After':>15}{'Gap (pts)':>12}")
    for _i in range(len(holdings)):
        _ticker, _shares, _price = holdings[_i]
        print(f"{_ticker:<8}{_shares:>12}{target_shares[_i]:>15}{shares_to_trade[_i]:>18}{value_after[_i]:>15,.2f}{weight_after[_i]*100:>14.2f}%{gap_points[_i]:>11.2f}")

    print(f"\nCash left after trades: ${cash_left:,.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    Sum of holdings should be equal to portfolio minus your cash (holdings = 116,302, Portfolio = 121,302 and Cash = 5,000. Therefore 121,302 -5,000 = 116,302). Your weights should always equal 100 and cash is greater than or equal to 0.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Initially, the code the agent created did not work because I had not defined holdings, cash and target weights separately. Once I did, the code worked and I checked the final result of 121,302 by following the five steps defined in Section 2 and doing it in excel. Additionally, I also had to ask the agent to complete the final steps of dividing target value with price and also made sure it was correct in excel.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell
def _():
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For Going Further, I installed yahoo finance in UV and then worked with my agent to make sure the holdings in section 3 could be updated in real time based on yahoo finance vs manual inputs.
    """)
    return


@app.cell
def _():
    return


@app.cell
def _():
    import yfinance as yf

    return (yf,)


@app.cell
def _(holdings, yf):
    holdings_live = []
    for _ticker, _shares, _price in holdings:
        _live_price = yf.Ticker(_ticker).fast_info["lastPrice"]
        holdings_live.append((_ticker, _shares, _live_price))

    holdings_live
    return


if __name__ == "__main__":
    app.run()
