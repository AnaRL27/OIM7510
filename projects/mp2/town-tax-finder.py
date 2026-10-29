# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "requests",
# ]
# ///

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
def _(csv, os, requests):
    data_folder = "projects/mp2/data"
    os.makedirs(data_folder, exist_ok=True)


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

        with open(f"{data_folder}/towns_{county}.csv", "w", newline="") as _file:
            _writer = csv.DictWriter(_file, fieldnames=towns[0].keys())
            _writer.writeheader()
            for _town in towns:
                _writer.writerow(_town)

        return towns


    def get_town_history(dor_code, year):
        response = requests.get(f"https://oim.zhili.dev/ma/towns/{dor_code}/history")
        data = response.json()

        with open(f"{data_folder}/history_{dor_code}.csv", "w", newline="") as _file:
            _writer = csv.DictWriter(_file, fieldnames=data["years"][0].keys())
            _writer.writeheader()
            for _year_record in data["years"]:
                _writer.writerow(_year_record)

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
    return sorted_results, towns


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


@app.cell
def _(get_town_history, sorted_results, towns):
    print(f"{'Town':<15}{'2026 Value':>12}{'2025 Value':>12}{'2026 Bill':>12}{'2025 Bill':>12}")
    value_lower_count = 0
    bill_lower_count = 0
    skipped_2025 = 0
    for _r in sorted_results:
        for _town in towns:
            if _town["name"] == _r["town"]:
                _dor_code = _town["dor_code"]
        _history_2025 = get_town_history(_dor_code, 2025)
        if _history_2025 is None:
            skipped_2025 = skipped_2025 + 1
        else:
            _value_2025 = _history_2025["average_single_family_value_dollars"]
            _bill_2025 = _history_2025["average_single_family_bill_dollars"]
            print(f"{_r['town']:<15}{_r['average_value']:>12,}{_value_2025:>12,}{_r['average_bill']:>12,}{_bill_2025:>12,}")
            if _value_2025 < _r["average_value"]:
                value_lower_count = value_lower_count + 1
            if _bill_2025 < _r["average_bill"]:
                bill_lower_count = bill_lower_count + 1

    print(
        f"Out of {len(sorted_results)} towns, {value_lower_count} had a lower average home value in 2025 "
        f"and {bill_lower_count} had a lower average bill in 2025, compared with 2026."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The prediction was mostly right since 10/12 towns had a lower home value and 11/12 had a lower tax value.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Going Further
    """)
    return


@app.cell
def _(
    budget_dollars,
    fiscal_year,
    get_town_history,
    get_towns,
    sorted_results,
    tax_limit_dollars,
):
    norfolk_towns = get_towns("Norfolk")

    norfolk_results = []
    for _town in norfolk_towns:
        _history = get_town_history(_town["dor_code"], fiscal_year)
        if _history is not None:
            _average_value = _history["average_single_family_value_dollars"]
            _average_bill = _history["average_single_family_bill_dollars"]
            if _average_value <= budget_dollars and _average_bill <= tax_limit_dollars:
                norfolk_results.append({
                    "town": _town["name"],
                    "average_value": _average_value,
                    "tax_rate": _history["residential_rate_per_thousand"],
                    "average_bill": _average_bill,
                })

    norfolk_sorted = sorted(norfolk_results, key=lambda r: r["average_bill"])

    print(f"{'Town':<15}{'Average Value':>15}{'Tax Rate':>12}{'Average Bill':>15}")
    for _r in norfolk_sorted:
        print(f"{_r['town']:<15}{_r['average_value']:>15,}{_r['tax_rate']:>12}{_r['average_bill']:>15,}")

    print(
        f"\nOut of {len(norfolk_towns)} towns in Norfolk County, {len(norfolk_sorted)} have an average home "
        f"under ${budget_dollars:,} and an average tax bill under ${tax_limit_dollars:,}, "
        f"compared with {len(sorted_results)} towns in Middlesex County."
    )
    return (norfolk_sorted,)


@app.cell
def _(
    budget_dollars,
    fiscal_year,
    get_town_history,
    get_towns,
    norfolk_sorted,
    sorted_results,
    tax_limit_dollars,
):
    worcester_towns = get_towns("Worcester")

    worcester_results = []
    for _town in worcester_towns:
        _history = get_town_history(_town["dor_code"], fiscal_year)
        if _history is not None:
            _average_value = _history["average_single_family_value_dollars"]
            _average_bill = _history["average_single_family_bill_dollars"]
            if _average_value <= budget_dollars and _average_bill <= tax_limit_dollars:
                worcester_results.append({
                    "town": _town["name"],
                    "average_value": _average_value,
                    "tax_rate": _history["residential_rate_per_thousand"],
                    "average_bill": _average_bill,
                })

    worcester_sorted = sorted(worcester_results, key=lambda r: r["average_bill"])

    print(f"{'Town':<15}{'Average Value':>15}{'Tax Rate':>12}{'Average Bill':>15}")
    for _r in worcester_sorted:
        print(f"{_r['town']:<15}{_r['average_value']:>15,}{_r['tax_rate']:>12}{_r['average_bill']:>15,}")

    print(
        f"\nOut of {len(worcester_towns)} towns in Worcester County, {len(worcester_sorted)} have an average home "
        f"under ${budget_dollars:,} and an average tax bill under ${tax_limit_dollars:,}, "
        f"compared with {len(sorted_results)} towns in Middlesex County and {len(norfolk_sorted)} towns in Norfolk County."
    )
    return (worcester_sorted,)


@app.cell
def _(
    budget_dollars,
    fiscal_year,
    get_town_history,
    get_towns,
    norfolk_sorted,
    sorted_results,
    tax_limit_dollars,
    worcester_sorted,
):
    plymouth_towns = get_towns("Plymouth")

    plymouth_results = []
    for _town in plymouth_towns:
        _history = get_town_history(_town["dor_code"], fiscal_year)
        if _history is not None:
            _average_value = _history["average_single_family_value_dollars"]
            _average_bill = _history["average_single_family_bill_dollars"]
            if _average_value <= budget_dollars and _average_bill <= tax_limit_dollars:
                plymouth_results.append({
                    "town": _town["name"],
                    "average_value": _average_value,
                    "tax_rate": _history["residential_rate_per_thousand"],
                    "average_bill": _average_bill,
                })

    plymouth_sorted = sorted(plymouth_results, key=lambda r: r["average_bill"])

    print(f"{'Town':<15}{'Average Value':>15}{'Tax Rate':>12}{'Average Bill':>15}")
    for _r in plymouth_sorted:
        print(f"{_r['town']:<15}{_r['average_value']:>15,}{_r['tax_rate']:>12}{_r['average_bill']:>15,}")

    print(
        f"\nOut of {len(plymouth_towns)} towns in Plymouth County, {len(plymouth_sorted)} have an average home "
        f"under ${budget_dollars:,} and an average tax bill under ${tax_limit_dollars:,}, "
        f"compared with {len(sorted_results)} towns in Middlesex County, {len(norfolk_sorted)} towns in Norfolk County, "
        f"and {len(worcester_sorted)} towns in Worcester County."
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Middlesex County offers the fewest affordable options for this couple, with only 12 of 54 towns (22%) meeting the $700,000 home value and $8,000 tax bill limits, while Norfolk is similarly tight at 7 of 28 towns (25%), but Plymouth (16 of 27 towns, 59%) and especially Worcester (46 of 60 towns, 77%) offer far more towns that fit the budget.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 10. Time Spent
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    I am a beginner and have never used python before so every step takes a long time for me. I spent around 6+ hours mostly in the first section where I needed to understand what was being asked and how to frame the approach step by step. I also need to work more efficiently with AI.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell
def _():
    import csv
    import os

    import marimo as mo
    import requests

    return csv, mo, os, requests


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


if __name__ == "__main__":
    app.run()
