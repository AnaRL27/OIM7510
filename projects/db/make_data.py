"""Writes fake data for the Babson Investment Club database.

Run with: uv run python projects/db/make_data.py
Writes one CSV file per table into projects/db/data/.
"""

import csv
import os
import random
from datetime import date, timedelta

random.seed(42)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

AS_OF = date(2026, 11, 8)
START = date(2025, 11, 8)


def write_csv(filename, header, rows):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            writer.writerow(row)
    print(f"wrote {len(rows)} rows to {filename}")


def all_days(start, end):
    days = []
    d = start
    while d <= end:
        days.append(d)
        d = d + timedelta(days=1)
    return days


def random_date(start, end):
    span = (end - start).days
    offset = random.randint(0, span)
    return start + timedelta(days=offset)


# ---------------------------------------------------------------------------
# Members
# ---------------------------------------------------------------------------

first_names = [
    "Ana", "Ben", "Carla", "Diego", "Ella", "Felix", "Grace", "Hassan",
    "Iris", "Jamal", "Kira", "Leo", "Maya", "Noah", "Priya",
]
last_names = [
    "Rivera", "Chen", "Okafor", "Silva", "Novak", "Adams", "Patel",
    "Lund", "Garcia", "Hughes", "Kim", "Moreau", "Singh",
]

members = []
for i in range(15):
    member_id = i + 1
    first = first_names[i]
    last = last_names[i % len(last_names)]
    class_year = random.choice([2026, 2027, 2028, 2029])
    join_date = random_date(START - timedelta(days=700), START)
    email = f"{first.lower()}.{last.lower()}@babson.edu"
    members.append([member_id, first, last, email, class_year, join_date])

write_csv(
    "members.csv",
    ["member_id", "first_name", "last_name", "school_email", "class_year", "join_date"],
    members,
)

# ---------------------------------------------------------------------------
# Portfolios
# ---------------------------------------------------------------------------

strategies = ["Growth", "Value", "Index Tracking", "Income", ""]
portfolio_names = ["Growth Fund", "Tech Bets", "Dividend Picks", "Core Holdings", "Side Book"]

portfolios = []
portfolio_id = 1
for member in members:
    member_id, _, _, _, _, join_date = member
    # member 15 (last one) gets zero portfolios on purpose
    if member_id == 15:
        continue
    num_portfolios = random.choice([1, 1, 1, 2])
    for _ in range(num_portfolios):
        name = random.choice(portfolio_names)
        created_date = random_date(join_date, AS_OF - timedelta(days=30))
        strategy = random.choice(strategies)
        portfolios.append([portfolio_id, member_id, name, created_date, strategy])
        portfolio_id += 1

write_csv(
    "portfolios.csv",
    ["portfolio_id", "member_id", "name", "created_date", "strategy"],
    portfolios,
)

# ---------------------------------------------------------------------------
# Assets
# ---------------------------------------------------------------------------

# asset_id, name, type, sector (sector blank for crypto)
assets = [
    [1, "Apple Inc", "stock", "Technology"],
    [2, "Microsoft Corp", "stock", "Technology"],
    [3, "Amazon.com Inc", "stock", "Consumer Discretionary"],
    [4, "Alphabet Inc", "stock", "Technology"],
    [5, "Tesla Inc", "stock", "Consumer Discretionary"],
    [6, "JPMorgan Chase", "stock", "Financials"],
    [7, "Exxon Mobil", "stock", "Energy"],
    [8, "SPDR S&P 500 ETF", "ETF", "Diversified"],
    [9, "Invesco QQQ ETF", "ETF", "Diversified"],
    [10, "Bitcoin", "crypto", ""],
    [11, "Ethereum", "crypto", ""],
    [12, "Northstar Media", "stock", "Communication Services"],
]

write_csv("assets.csv", ["asset_id", "name", "type", "sector"], assets)

# Exxon Mobil (asset_id 7) is never traded, on purpose.
NEVER_TRADED_ASSET_ID = 7

# ---------------------------------------------------------------------------
# Asset tickers (one row per ticker an asset has used)
# ---------------------------------------------------------------------------

current_tickers = {
    1: "AAPL", 2: "MSFT", 3: "AMZN", 4: "GOOGL", 5: "TSLA", 6: "JPM",
    7: "XOM", 8: "SPY", 9: "QQQ", 10: "BTC", 11: "ETH", 12: "NOVA",
}

asset_tickers = []
for asset_id, ticker in current_tickers.items():
    if asset_id == 12:
        # Northstar Media changes its ticker partway through the year.
        asset_tickers.append([asset_id, START, "NSTR"])
        asset_tickers.append([asset_id, date(2026, 4, 1), "NOVA"])
    else:
        asset_tickers.append([asset_id, START, ticker])

write_csv("asset_tickers.csv", ["asset_id", "effective_date", "ticker"], asset_tickers)

# ---------------------------------------------------------------------------
# Closing prices
# ---------------------------------------------------------------------------

start_prices = {
    1: 180.0, 2: 330.0, 3: 140.0, 4: 135.0, 5: 240.0, 6: 150.0,
    7: 105.0, 8: 440.0, 9: 370.0, 10: 35000.0, 11: 2000.0, 12: 48.0,
}

crypto_ids = [10, 11]

closing_prices = []
asset_price_dates = {}
asset_price_lookup = {}

for asset_id, start_price in start_prices.items():
    price = start_price
    price_dates = []
    if asset_id in crypto_ids:
        days = all_days(START, AS_OF)
    else:
        days = []
        for d in all_days(START, AS_OF):
            if d.weekday() < 5:
                days.append(d)
    for d in days:
        change = random.uniform(-0.02, 0.02)
        price = max(price * (1 + change), 0.01)
        rounded_price = round(price, 2)
        closing_prices.append([asset_id, d, rounded_price])
        price_dates.append(d)
        asset_price_lookup[(asset_id, d)] = rounded_price
    asset_price_dates[asset_id] = price_dates

write_csv("closing_prices.csv", ["asset_id", "price_date", "close_price"], closing_prices)

# ---------------------------------------------------------------------------
# Trades
# ---------------------------------------------------------------------------

tradeable_asset_ids = []
for asset_id in current_tickers:
    if asset_id != NEVER_TRADED_ASSET_ID:
        tradeable_asset_ids.append(asset_id)

holdings = {}  # (portfolio_id, asset_id) -> quantity held
used_combos = set()  # (portfolio_id, asset_id, date)
trades = []
trade_id = 1

for portfolio in portfolios:
    portfolio_id, member_id, _, created_date, _ = portfolio
    num_trades = random.randint(12, 20)
    attempts = 0
    made = 0
    while made < num_trades and attempts < num_trades * 5:
        attempts += 1
        asset_id = random.choice(tradeable_asset_ids)
        price_dates = asset_price_dates[asset_id]
        valid_dates = []
        for d in price_dates:
            if d >= created_date:
                valid_dates.append(d)
        if not valid_dates:
            continue
        trade_date = random.choice(valid_dates)
        combo = (portfolio_id, asset_id, trade_date)
        if combo in used_combos:
            continue

        held = holdings.get((portfolio_id, asset_id), 0)
        if held == 0:
            side = "buy"
        else:
            side = random.choice(["buy", "buy", "sell"])

        # crypto trades in fractional units; stocks and ETFs trade in whole shares
        if asset_id in crypto_ids:
            if side == "buy":
                quantity = round(random.uniform(0.01, 5.0), 4)
            else:
                quantity = round(random.uniform(0.01, held), 4)
        else:
            if side == "buy":
                quantity = random.randint(1, 50)
            else:
                quantity = random.randint(1, held)

        close_price = asset_price_lookup[(asset_id, trade_date)]
        noise = random.uniform(-0.01, 0.01)
        price = round(close_price * (1 + noise), 2)
        fee = 0.0
        if random.random() < 0.3:
            fee = round(random.uniform(1.0, 10.0), 2)

        trades.append([trade_id, portfolio_id, asset_id, trade_date, side, quantity, price, fee])
        used_combos.add(combo)

        if side == "buy":
            holdings[(portfolio_id, asset_id)] = held + quantity
        else:
            holdings[(portfolio_id, asset_id)] = held - quantity

        trade_id += 1
        made += 1

# Force exactly two trades that oversell: a portfolio sells more units
# of an asset than it holds. This breaks the rule "a portfolio never
# sells more units of an asset than it holds at the time" on purpose,
# so question 7 can find them.
broken_rule_trades = []
candidates = []
for key, qty in holdings.items():
    candidates.append((key, qty))
random.shuffle(candidates)

forced = 0
for (portfolio_id, asset_id), qty in candidates:
    if forced == 2:
        break
    price_dates = asset_price_dates[asset_id]
    trade_date = price_dates[-1]
    combo = (portfolio_id, asset_id, trade_date)
    if combo in used_combos:
        continue
    if asset_id in crypto_ids:
        oversell_quantity = round(qty + random.uniform(1.0, 5.0), 4)
    else:
        oversell_quantity = qty + random.randint(10, 50)
    close_price = asset_price_lookup[(asset_id, trade_date)]
    trades.append([trade_id, portfolio_id, asset_id, trade_date, "sell", oversell_quantity, close_price, 0.0])
    broken_rule_trades.append(trade_id)
    used_combos.add(combo)
    trade_id += 1
    forced += 1

write_csv(
    "trades.csv",
    ["trade_id", "portfolio_id", "asset_id", "trade_date", "side", "quantity", "price", "fee"],
    trades,
)

print(f"trade_ids that oversell on purpose (break the holdings rule): {broken_rule_trades}")
