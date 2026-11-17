# /// script
# requires-python = ">=3.12,<3.15"
# dependencies = [
#     "marimo[sql]",
#     "duckdb",
#     "polars",
#     "pyarrow",
#     "altair",
# ]
# ///
"""Asks projects/db/database.duckdb the Babson Investment Club's business questions.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import duckdb
    import polars as pl

    return (duckdb,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Asking the Database Questions

    This notebook asks `projects/db/database.duckdb`, built by `build.py`, the club's business questions. It reads the database through its own `ask` function, the same shape as `build.py`'s.
    """)
    return


@app.cell
def _(duckdb, mo):
    database = mo.notebook_dir() / "database.duckdb"

    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **`as_of` date: November 8, 2026.** This is the same date `make_data.py` used to generate a year of data, so every "last 30 days", "last 90 days" and "last month" below is counted back from it, not from today's real date, which falls after the data ends.
    """)
    return


@app.cell
def _():
    from datetime import date

    as_of = date(2026, 11, 8)
    return (as_of,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *(The prediction below for "Reading It Back" was committed, on its own, as `db: prediction` before any of the queries in this notebook ran. After that commit, Part A's `make_data.py` turned out to have a bug — it decided each trade's buy or sell in the random order it was generated, not in calendar order, so a sell could land on an earlier date than the buy meant to cover it. That bug is now fixed and the data regenerated; see "Working With the Agent" below. It did not touch the prediction's reasoning or its answer.)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Portfolio Activity, Last 30 Days

    For each portfolio over the last 30 days: the number of trades, the money spent on buys with fees added, and the money received from sells with fees taken off.
    """)
    return


@app.cell
def _(as_of, ask):
    q1 = ask(f"""
        SELECT
            portfolio_id,
            count(*) AS n_trades,
            round(sum(CASE WHEN side = 'buy' THEN quantity * price + fee ELSE 0 END), 2) AS buy_spend,
            round(sum(CASE WHEN side = 'sell' THEN quantity * price - fee ELSE 0 END), 2) AS sell_proceeds
        FROM trades
        WHERE trade_date BETWEEN DATE '{as_of}' - INTERVAL 29 DAY AND DATE '{as_of}'
        GROUP BY portfolio_id
        ORDER BY portfolio_id
    """)
    q1
    return (q1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Thirteen of the club's fifteen portfolios traded in the last 30 days; portfolio 12 spent the most on buys, $241,705.10, and portfolio 14 took in the most from sells, $163,734.98.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Members, Portfolios and Total Bought

    One row for each member, members with no portfolio included: their number of portfolios and the total value they bought across them.
    """)
    return


@app.cell
def _(ask):
    q2 = ask("""
        SELECT
            m.member_id,
            m.first_name,
            m.last_name,
            count(DISTINCT po.portfolio_id) AS n_portfolios,
            round(COALESCE(sum(CASE WHEN t.side = 'buy' THEN t.quantity * t.price ELSE 0 END), 0), 2) AS total_bought
        FROM members m
        LEFT JOIN portfolios po ON po.member_id = m.member_id
        LEFT JOIN trades t ON t.portfolio_id = po.portfolio_id
        GROUP BY m.member_id, m.first_name, m.last_name
        ORDER BY m.member_id
    """)
    q2
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Priya Chen owns no portfolios and bought nothing; every other member owns one or two, and Ella Novak bought the most across her two, $650,409.21.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. What Each Portfolio Holds

    What each portfolio holds on `as_of`: for each asset, the units bought minus the units sold, keeping only those above zero. This uses the `portfolio_holdings` view.
    """)
    return


@app.cell
def _(ask):
    q3 = ask("""
        SELECT ph.portfolio_id, po.name, a.name AS asset_name, ph.units_held
        FROM portfolio_holdings ph
        JOIN portfolios po ON po.portfolio_id = ph.portfolio_id
        JOIN assets a ON a.asset_id = ph.asset_id
        ORDER BY ph.portfolio_id, a.name
    """)
    q3
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    All 15 portfolios hold at least one asset today, across 124 portfolio-asset positions in total.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Trade Price Against the Closing Price, Last 90 Days

    For every trade in the last 90 days, the closing price on the trade date, and how far the trade price was from it, as a percent of the closing price.
    """)
    return


@app.cell
def _(as_of, ask):
    q4 = ask(f"""
        SELECT
            t.trade_id,
            po.name AS portfolio_name,
            a.name AS asset_name,
            t.trade_date,
            t.price AS trade_price,
            cp.close_price,
            round(abs(t.price - cp.close_price) / cp.close_price * 100, 3) AS pct_off
        FROM trades t
        JOIN closing_prices cp ON cp.asset_id = t.asset_id AND cp.price_date = t.trade_date
        JOIN portfolios po ON po.portfolio_id = t.portfolio_id
        JOIN assets a ON a.asset_id = t.asset_id
        WHERE t.trade_date BETWEEN DATE '{as_of}' - INTERVAL 89 DAY AND DATE '{as_of}'
        ORDER BY pct_off DESC
    """)
    q4
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    134 trades fall in the last 90 days, and on average a trade's price was 0.445% away from that day's closing price — close to free, since `make_data.py` only adds up to 1% of noise around the close.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Assets Never Traded

    The assets the club follows that no portfolio has ever traded.
    """)
    return


@app.cell
def _(ask):
    q5 = ask("""
        SELECT asset_id, name, type, sector
        FROM assets
        WHERE asset_id NOT IN (SELECT DISTINCT asset_id FROM trades)
    """)
    q5
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Exxon Mobil is the only asset the club follows that no portfolio has ever traded.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. The Asset That Changed Its Ticker

    The asset that changed its ticker: its value traded over the year, under both tickers together.
    """)
    return


@app.cell
def _(ask):
    q6 = ask("""
        SELECT a.asset_id, a.name, count(*) AS n_trades, round(sum(t.quantity * t.price), 2) AS value_traded
        FROM trades t
        JOIN assets a ON a.asset_id = t.asset_id
        WHERE t.asset_id IN (SELECT asset_id FROM asset_tickers GROUP BY asset_id HAVING count(*) > 1)
        GROUP BY a.asset_id, a.name
    """)
    q6
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Northstar Media, known as `NSTR` until 2026-04-01 and `NOVA` after, traded 22 times across the year for a combined $24,526.99 — the `trades` table keeps one `asset_id` for it the whole time, so the two tickers add up without extra work.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Trades That Break the Holdings Rule *(checks a rule)*

    Every trade checked against the rule that a portfolio never sells more units of an asset than it holds at the time, and a list of any that break it.
    """)
    return


@app.cell
def _(ask):
    q7 = ask("""
        WITH running AS (
            SELECT
                trade_id, portfolio_id, asset_id, trade_date, side, quantity,
                sum(CASE WHEN side = 'buy' THEN quantity ELSE -quantity END)
                    OVER (
                        PARTITION BY portfolio_id, asset_id
                        ORDER BY trade_date, trade_id
                        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                    ) AS units_held_after
            FROM trades
        )
        SELECT trade_id, portfolio_id, asset_id, trade_date, quantity, units_held_after
        FROM running
        WHERE units_held_after < 0
        ORDER BY trade_id
    """)
    q7
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Trade 237 (portfolio 14, asset 10) and trade 238 (portfolio 15, asset 5) both leave negative units held, and are the only two — exactly the rows `make_data.py` broke the rule in on purpose.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Sector Concentration (my own question)

    For each portfolio's current holdings, using the `portfolio_holdings` view, the number of distinct sectors held — which portfolios are least diversified?
    """)
    return


@app.cell
def _(ask):
    q8 = ask("""
        SELECT po.portfolio_id, po.name, count(DISTINCT a.sector) AS n_sectors
        FROM portfolio_holdings ph
        JOIN portfolios po ON po.portfolio_id = ph.portfolio_id
        JOIN assets a ON a.asset_id = ph.asset_id
        GROUP BY po.portfolio_id, po.name
        ORDER BY n_sectors ASC, po.portfolio_id
    """)
    q8
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Portfolio 3, "Dividend Picks", is the least diversified, holding assets from only 3 distinct sectors; most portfolios spread across 4 or 5.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## How I Know These Numbers Are Right

    Two of the answers above, checked a second way.

    **Question 2's total bought.** Question 2 sums `quantity * price` for buys through a join from `members`, grouped per member. Summed directly from `trades` with no join at all, buys total the same $3,547,575.01 — the join neither drops nor duplicates any buy trade.
    """)
    return


@app.cell
def _(ask):
    ask("SELECT round(sum(quantity * price), 2) AS total_bought_direct FROM trades WHERE side = 'buy'")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Question 3's holdings.** The `portfolio_holdings` view says 15 distinct portfolios hold something today. Counting the club's portfolios directly gives the same 15 — every portfolio holds at least one asset, which matches what section 2 above already showed (every portfolio bought something).
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            (SELECT count(DISTINCT portfolio_id) FROM portfolio_holdings) AS portfolios_with_holdings,
            (SELECT count(*) FROM portfolios) AS portfolios_total
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Working With the Agent

    While building question 7 above, the agent reported that `make_data.py` had a bug. The script assigned buy/sell sides and tracked each portfolio's running holdings in the random order it generated trades, rather than in `trade_date` order. That allowed a sell to fall on an earlier date than the buy that was supposed to cover it. According to the agent, about 29 trades violated the holdings rule, not the 2 the script was designed to seed on purpose.

    I did not accept this claim as-is. Before asking the agent to change anything, I verified it myself and counted the trades where holdings went negative. The result was 29, which confirmed the agent's finding. I then had the agent implement a fix: the script now sorts each portfolio's selected trades by date before assigning buy/sell and how many shares each trade involves. That fix is its own commit, `db: fix oversell generation to use chronological trade order`, and question 7's cell above is where I re-checked it: it now finds exactly the 2 trades (237, 238) the script seeds on purpose.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reading It Back

    **The question:** *For every trade in the last 90 days, the closing price on the trade date, and how far the trade price was from it, as a percent of the closing price* (question 4 above). This joins `trades`, `closing_prices`, `portfolios` and `assets` — four tables.

    **My prediction, committed before running anything (`db: prediction`).** In `build.py`, `trades` declares `FOREIGN KEY (asset_id, trade_date) REFERENCES closing_prices(asset_id, price_date)`, and `(asset_id, price_date)` is `closing_prices`' primary key. A foreign key into a primary key matches at most one row on the other side, so joining `trades` to `closing_prices` on `(asset_id, trade_date) = (asset_id, price_date)` cannot add rows (no closing price repeats for a day) or drop rows (every trade has one, by the constraint). Joining `portfolios` and `assets` in as well cannot change the count either, since every trade already has exactly one portfolio and one asset. **I predicted the four-table join, before any grouping, would produce exactly as many rows as there are trades in the 90 days ending on `as_of`** — not more, not fewer.
    """)
    return


@app.cell
def _(as_of, ask):
    ask(f"""
        SELECT
            (SELECT count(*) FROM trades
                JOIN closing_prices cp ON cp.asset_id = trades.asset_id AND cp.price_date = trades.trade_date
                JOIN portfolios po ON po.portfolio_id = trades.portfolio_id
                JOIN assets a ON a.asset_id = trades.asset_id
                WHERE trades.trade_date BETWEEN DATE '{as_of}' - INTERVAL 89 DAY AND DATE '{as_of}') AS join_rows,
            (SELECT count(*) FROM trades
                WHERE trade_date BETWEEN DATE '{as_of}' - INTERVAL 89 DAY AND DATE '{as_of}') AS trades_in_window
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **The joins alone produced 134 rows, and there are 134 trades in that 90-day window — the prediction matched.** The reasoning held: the foreign key into `closing_prices`' primary key let each trade match exactly one closing price, and `portfolios`/`assets` each matched exactly one row per trade, so the four-table join is one row for one trade, no more and no fewer.

    **One row of question 4's result means:** one trade, naming the portfolio that made it and the asset it traded, with the price that trade was actually executed at next to that asset's official closing price on that same day, and how far apart the two prices were, as a percent of the closing price.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Going Further

    One of question 1's results — the number of trades each portfolio made in the last 30 days — as a bar chart, one bar per portfolio.
    """)
    return


@app.cell
def _(q1):
    q1.plot.bar(x="portfolio_id", y="n_trades")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Two portfolios, 11 and 12, traded noticeably more often than the rest in the last 30 days; most portfolios made only 1 to 4 trades in that window.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Time Spent

    Total of 8+ hours since i am a beginner
    """)
    return


if __name__ == "__main__":
    app.run()
