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

    return duckdb, pl


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
    ## 3. Reading It Back

    **The question:** *For every trade in the last 90 days, the closing price on the trade date, and how far the trade price was from it, as a percent of the closing price.* This joins `trades`, `closing_prices`, `portfolios` and `assets` — four tables.

    **My prediction, before running anything.** In `build.py`, `trades` declares `FOREIGN KEY (asset_id, trade_date) REFERENCES closing_prices(asset_id, price_date)`, and `(asset_id, price_date)` is `closing_prices`' primary key. A foreign key into a primary key matches at most one row on the other side, so joining `trades` to `closing_prices` on `(asset_id, trade_date) = (asset_id, price_date)` cannot add rows (no closing price repeats for a day) or drop rows (every trade has one, by the constraint). Joining `portfolios` and `assets` in as well cannot change the count either, since every trade already has exactly one portfolio and one asset.

    So **I predict the four-table join, before any grouping, produces exactly as many rows as there are trades in the 90 days ending on `as_of`** — not more, not fewer. I have not yet counted that number or run the join; the next section does both, after this prediction is committed.
    """)
    return


if __name__ == "__main__":
    app.run()
