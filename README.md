# Personal Expense Tracker & Budget Analyzer

## Goals
- Let the user add daily expense transactions.
- Store all expenses in a local SQLite database.
- Allow viewing all transactions or filtering by date/category.
- Allow setting a monthly budget (e.g., for November 2025).
- Show how much of the budget has been used.
- Generate a simple monthly summary (total spent, by category).
- Export reports to CSV (later).

## Data we need to store

### Expenses
- id (auto-generated)
- category (e.g., Food, Rent, Transport)
- amount
- date (YYYY-MM-DD)
- description (optional)

### Budgets
- id (auto-generated)
- month (1–12)
- year (e.g., 2025)
- amount (budget for that month)
