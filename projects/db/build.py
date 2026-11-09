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
"""Builds the Babson Investment Club database from projects/db/data/*.csv.
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
    # Building the Database

    This notebook builds `projects/db/database.duckdb` from the CSV files in `projects/db/data/`, made by `make_data.py`. It rebuilds the file from nothing every time it runs.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Tables

    Six tables, matching the ERD in `README.md`:

    - `members` and `portfolios`: a member owns zero or more portfolios.
    - `assets`, `asset_tickers` and `closing_prices`: an asset is kept as one identity even if its ticker changes, and has at most one closing price per day.
    - `trades`: one buy or sell of one asset by one portfolio on one day.

    A trade's `(asset_id, trade_date)` is a **foreign key into `closing_prices`**, which holds the rule "a trade happens on a day its asset has a closing price." The rule "a portfolio never sells more units than it holds" cannot be held by a constraint, because it has to add up earlier rows; section 6 checks it with a query instead.
    """)
    return


@app.cell
def _(duckdb, mo):
    _file = mo.notebook_dir() / "database.duckdb"
    _data = mo.notebook_dir() / "data"
    _file.unlink(missing_ok=True)

    with duckdb.connect(_file) as _con:
        _con.execute("""
            CREATE TABLE members (
                member_id     INTEGER PRIMARY KEY,
                first_name    VARCHAR NOT NULL,
                last_name     VARCHAR NOT NULL,
                school_email  VARCHAR NOT NULL UNIQUE,
                class_year    INTEGER NOT NULL,
                join_date     DATE NOT NULL
            )
        """)
        _con.execute("""
            CREATE TABLE portfolios (
                portfolio_id  INTEGER PRIMARY KEY,
                member_id     INTEGER NOT NULL REFERENCES members(member_id),
                name          VARCHAR NOT NULL,
                created_date  DATE NOT NULL,
                strategy      VARCHAR
            )
        """)
        _con.execute("""
            CREATE TABLE assets (
                asset_id  INTEGER PRIMARY KEY,
                name      VARCHAR NOT NULL,
                type      VARCHAR NOT NULL CHECK (type IN ('stock', 'ETF', 'crypto')),
                sector    VARCHAR
            )
        """)
        _con.execute("""
            CREATE TABLE asset_tickers (
                asset_id        INTEGER NOT NULL REFERENCES assets(asset_id),
                effective_date  DATE NOT NULL,
                ticker          VARCHAR NOT NULL,
                PRIMARY KEY (asset_id, effective_date)
            )
        """)
        _con.execute("""
            CREATE TABLE closing_prices (
                asset_id     INTEGER NOT NULL REFERENCES assets(asset_id),
                price_date   DATE NOT NULL,
                close_price  DOUBLE NOT NULL CHECK (close_price > 0),
                PRIMARY KEY (asset_id, price_date)
            )
        """)
        _con.execute("""
            CREATE TABLE trades (
                trade_id      INTEGER PRIMARY KEY,
                portfolio_id  INTEGER NOT NULL REFERENCES portfolios(portfolio_id),
                asset_id      INTEGER NOT NULL,
                trade_date    DATE NOT NULL,
                side          VARCHAR NOT NULL CHECK (side IN ('buy', 'sell')),
                quantity      DOUBLE NOT NULL CHECK (quantity > 0),
                price         DOUBLE NOT NULL CHECK (price > 0),
                fee           DOUBLE NOT NULL CHECK (fee >= 0),
                UNIQUE (portfolio_id, asset_id, trade_date),
                FOREIGN KEY (asset_id, trade_date) REFERENCES closing_prices(asset_id, price_date)
            )
        """)

        # load order matters: a table referenced by a foreign key loads first
        _con.execute(f"INSERT INTO members SELECT * FROM read_csv('{_data}/members.csv')")
        _con.execute(f"INSERT INTO assets SELECT * FROM read_csv('{_data}/assets.csv')")
        _con.execute(f"INSERT INTO asset_tickers SELECT * FROM read_csv('{_data}/asset_tickers.csv')")
        _con.execute(f"INSERT INTO closing_prices SELECT * FROM read_csv('{_data}/closing_prices.csv')")
        _con.execute(f"INSERT INTO portfolios SELECT * FROM read_csv('{_data}/portfolios.csv')")
        _con.execute(f"INSERT INTO trades SELECT * FROM read_csv('{_data}/trades.csv')")

        _con.execute("""
            CREATE VIEW portfolio_holdings AS
                SELECT
                    portfolio_id,
                    asset_id,
                    sum(CASE WHEN side = 'buy' THEN quantity ELSE -quantity END) AS units_held
                FROM trades
                GROUP BY portfolio_id, asset_id
                HAVING sum(CASE WHEN side = 'buy' THEN quantity ELSE -quantity END) > 0
        """)

    database = _file
    database.name
    return (database,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Every other cell reads through `ask`, which opens the file read-only, runs one query, and closes it again.
    """)
    return


@app.cell
def _(database, duckdb):
    def ask(sql):
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. The Data

    `make_data.py` writes the six CSV files with a fixed random seed, so it writes the same data every time. It breaks one rule on purpose, in exactly two trades: a portfolio sells more units of an asset than it holds at that point. Those two trades are `trade_id` 243 and 244, printed by the script when it runs. It also leaves one member, Priya, with no portfolio, and one asset, Exxon Mobil (`asset_id` 7), never traded, so the questions about rows with nothing attached have an answer.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. A Look at the Data

    Bitcoin's closing price over the year. A real crypto asset moves this much, day to day, so the shape looks right.
    """)
    return


@app.cell
def _(ask):
    _prices = ask("""
        SELECT price_date, close_price
        FROM closing_prices
        WHERE asset_id = 10
        ORDER BY price_date
    """)
    _prices.plot.line(x="price_date", y="close_price")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Row Counts
    """)
    return


@app.cell
def _(ask):
    ask("""
        SELECT
            (SELECT count(*) FROM members) AS members,
            (SELECT count(*) FROM portfolios) AS portfolios,
            (SELECT count(*) FROM assets) AS assets,
            (SELECT count(*) FROM asset_tickers) AS asset_tickers,
            (SELECT count(*) FROM closing_prices) AS closing_prices,
            (SELECT count(*) FROM trades) AS trades
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. A Row It Refuses

    Inserting a trade with a quantity of zero breaks the rule that a quantity has to be more than zero.
    """)
    return


@app.cell
def _(database, duckdb):
    try:
        with duckdb.connect(database) as _con:
            _con.execute("""
                INSERT INTO trades VALUES (9001, 1, 1, '2026-01-05', 'buy', 0, 180.0, 0.0)
            """)
        refused = "accepted"
    except duckdb.ConstraintException as _error:
        refused = str(_error).splitlines()[0]
    refused
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Answers You Already Knew

    Three checks whose answers are known from how `make_data.py` built the data.
    """)
    return


@app.cell
def _(ask):
    # expected: Priya has no portfolio, so members - portfolio owners = 1
    ask("""
        SELECT count(*) AS members_without_a_portfolio
        FROM members
        WHERE member_id NOT IN (SELECT member_id FROM portfolios)
    """)
    return


@app.cell
def _(ask):
    # expected: Exxon Mobil (asset_id 7) was never traded
    ask("""
        SELECT count(*) AS trades_of_exxon
        FROM trades
        WHERE asset_id = 7
    """)
    return


@app.cell
def _(ask):
    # expected: the two trades that oversell are trade_id 252 and 253
    ask("""
        SELECT t.trade_id, t.portfolio_id, t.asset_id, t.trade_date, t.quantity
        FROM trades t
        WHERE t.trade_id IN (252, 253)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. A View

    `portfolio_holdings` is the question the club asks every week: what every portfolio currently holds. It is saved in the cell that builds the database, so anybody can ask for it by name and always get the current rows.
    """)
    return


@app.cell
def _(ask):
    ask("SELECT * FROM portfolio_holdings ORDER BY portfolio_id, asset_id")
    return


if __name__ == "__main__":
    app.run()
