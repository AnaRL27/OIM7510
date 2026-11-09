# Database Project — Babson Investment Club

## 1. The Scenario

**B · Babson Investment Club.** The club runs paper portfolios for its members to learn with. Today its records are a shared spreadsheet and screenshots from a broker. This database gives it a clear history of every trade, what each portfolio holds, and what it is worth.

## 2. The ERD

```mermaid
erDiagram
    MEMBERS ||--o{ PORTFOLIOS : owns
    PORTFOLIOS ||--o{ TRADES : makes
    ASSETS ||--o{ TRADES : "is traded in"
    ASSETS ||--o{ CLOSING_PRICES : has
    ASSETS ||--o{ ASSET_TICKERS : "is known as"

    MEMBERS {
        int    member_id PK
        string first_name
        string last_name
        string school_email
        int    class_year
        date   join_date
    }
    PORTFOLIOS {
        int    portfolio_id PK
        int    member_id FK
        string name
        date   created_date
        string strategy
    }
    ASSETS {
        int    asset_id PK
        string name
        string type
        string sector
    }
    ASSET_TICKERS {
        int    asset_id PK, FK
        date   effective_date PK
        string ticker
    }
    CLOSING_PRICES {
        int    asset_id PK, FK
        date   price_date PK
        float  close_price
    }
    TRADES {
        int    trade_id PK
        int    portfolio_id FK
        int    asset_id FK
        date   trade_date
        string side
        int    quantity
        float  price
        float  fee
    }
```

## 3. What One Row Means

- One row of `members` is one person who belongs to the club.
- One row of `portfolios` is one paper portfolio owned by one member.
- One row of `assets` is one stock, ETF or crypto the club follows, kept as one identity even if its ticker changes.
- One row of `asset_tickers` is the ticker an asset used starting on one date.
- One row of `closing_prices` is one asset's closing price on one trading day.
- One row of `trades` is one buy or sell of one asset by one portfolio on one day.

## 4. Design Choices

*(filled in after the build — see below)*
