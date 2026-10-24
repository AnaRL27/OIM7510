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


@app.cell
def _():
    county = "Middlesex"
    budget_dollars = 700000
    tax_limit_dollars = 8000
    fiscal_year = 2026
    return budget_dollars, county, fiscal_year, tax_limit_dollars


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work
    """)
    return


@app.cell
def _(requests):
    def get_towns(county):
        towns = []
        page_number = 1
        response = requests.get(
            "https://oim.zhili.dev/ma/towns",
            params={"county": county, "per_page": 100, "page": page_number},
        )
        data = response.json()
        for _item in data["items"]:
            towns.append(_item)
        total_pages = data["pagination"]["pages"]

        for page_number in range(2, total_pages + 1):
            response = requests.get(
                "https://oim.zhili.dev/ma/towns",
                params={"county": county, "per_page": 100, "page": page_number},
            )
            data = response.json()
            for _item in data["items"]:
                towns.append(_item)
        return towns


    def get_town_history(dor_code, year):
        response = requests.get(f"https://oim.zhili.dev/ma/towns/{dor_code}/history")
        data = response.json()
        for _year_record in data["years"]:
            if _year_record["fiscal_year"] == year:
                return _year_record
        return None

    return get_town_history, get_towns


@app.cell
def _(
    budget_dollars,
    county,
    fiscal_year,
    get_town_history,
    get_towns,
    tax_limit_dollars,
):
    towns = get_towns(county)

    results = []
    skipped_towns = 0
    for _town in towns:
        _history = get_town_history(_town["dor_code"], fiscal_year)
        if _history is None:
            skipped_towns = skipped_towns + 1
        else:
            _average_value = _history["average_single_family_value_dollars"]
            _tax_rate = _history["residential_rate_per_thousand"]
            _average_bill = _history["average_single_family_bill_dollars"]
            if _average_value <= budget_dollars and _average_bill <= tax_limit_dollars:
                results.append({
                    "town": _town["name"],
                    "average_value": _average_value,
                    "tax_rate": _tax_rate,
                    "average_bill": _average_bill,
                })

    sorted_results = sorted(results, key=lambda r: r["average_bill"])
    return (sorted_results,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer
    """)
    return


@app.cell
def _(sorted_results):
    print(f"{'Town':<15}{'Average Value':>15}{'Tax Rate':>12}{'Average Bill':>15}")
    for _r in sorted_results:
        print(f"{_r['town']:<15}{_r['average_value']:>15,}{_r['tax_rate']:>12}{_r['average_bill']:>15,}")
    return


@app.cell
def _(budget_dollars, county, sorted_results, tax_limit_dollars):
    cheapest = sorted_results[0]
    print(
        f"In {county} County, {len(sorted_results)} towns have an average home "
        f"under ${budget_dollars:,} and an average tax bill under ${tax_limit_dollars:,}, "
        f"with {cheapest['town']} the cheapest at ${cheapest['average_bill']:,} a year "
        f"on a ${cheapest['average_value']:,} average home."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I know these numbers are right
    """)
    return


@app.cell
def _(sorted_results):
    print(f"{'Town':<15}{'Average Value':>15}{'Tax Rate':>10}{'Calculated Bill':>18}{'Reported Bill':>16}{'Difference':>13}")
    for _r in sorted_results:
        _calculated_bill = _r["average_value"] * _r["tax_rate"] / 1000
        _difference = _r["average_bill"] - _calculated_bill
        print(f"{_r['town']:<15}{_r['average_value']:>15,}{_r['tax_rate']:>10}{_calculated_bill:>18,.0f}{_r['average_bill']:>16,}{_difference:>13,.0f}")
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
    The only section where I changed the agent's output was section 6 when we were checking the results. The output of the formula I wanted to use to verify was: The average home value times the tax rate divided by 1,000 should come out close to the average bill. Tax rates are quoted per $1,000 of value. However, when the code resulted in just the columns calulcated bill and reported bill and then the difference, I asked the agent to also include the average value and tax rate we had previously calulated. This way we can use as a summary/ verification of our results.
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
    Function 1: Get towns - In: county name Out: list of towns. I asked about params (adds options to the web address so API knows what you are referring to).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Function 2: Get town history. In: dor code, 2026, Out: record for that year. I asked about lambda (tiny, unnamed function used once)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Change/ Prediction: One change in input to function 1 is fiscal year to 2025, predicting both house and tax value are lower than for 2026.
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
    import requests

    return mo, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


if __name__ == "__main__":
    app.run()
