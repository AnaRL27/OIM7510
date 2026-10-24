import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question
    The people who would use this are planning on buying a home in Middlesex of around $700,000 who want to keep their property tax bill under $8,000. What do their options look like (short list of towns) to determine feasibility and whether it makes sense to pivot.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI
    Part A:
    	1. List every town in the county (will check pagination to confirm I collected all of them)
    	2. Fiscal year 2026 history for each town. Figures needed for each town's history: average home value, residential tax rate and average bill.
    	3. Is the town’s average home value within their budget? And Is the town’s average bill within their tax limit?
    	4. Average bill lowest to highest
    	5. Table containing every town in Middlesex where the price and property tax meet their budget. Columns: town, average home value, residential tax rate, average bill.

    Part B:
    	1. get_towns(county) → in: county name, out: list of town records & get_town_history(dor_code, year) → in: dor_code + fiscal year, out: that town's history record
    	2. /ma/towns & /ma/towns/{dor_code}/history
    	3. Pagination: comparing total and pages
        4. The average home value times the tax rate divided by 1,000 should come out close to the average bill. Tax rates are quoted per $1,000 of value.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I know these numbers are right
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Reading It Back
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Going Further
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Time Spent
    """)
    return


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


if __name__ == "__main__":
    app.run()
