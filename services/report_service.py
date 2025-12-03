import os
import sys
import pandas as pd

# --- Make sure Python can see the project root (expense_tracker) ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from services import db_service

def load_expenses_df() -> pd.DataFrame:
    """
    Load all expenses from the database into a pandas DataFrame.
    Columns: id, category, amount, date, description
    """
    rows = db_service.get_all_expenses()
    df = pd.DataFrame(rows, columns=["id", "category", "amount", "date", "description"])

    if df.empty:
        return df

    # Ensure correct types
    df["amount"] = df["amount"].astype(float)
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
    return df

def category_summary() -> pd.DataFrame:
    """
    Return a DataFrame with total amount spent per category.
    Columns: category, total_amount
    """
    df = load_expenses_df()
    if df.empty:
        return pd.DataFrame(columns=["category", "total_amount"])

    grouped = (
        df.groupby("category", as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "total_amount"})
    )
    return grouped

def monthly_summary() -> pd.DataFrame:
    """
    Return a DataFrame with total amount spent per (year, month).
    Columns: year, month, total_amount
    """
    df = load_expenses_df()
    if df.empty:
        return pd.DataFrame(columns=["year", "month", "total_amount"])

    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month

    grouped = (
        df.groupby(["year", "month"], as_index=False)["amount"]
        .sum()
        .rename(columns={"amount": "total_amount"})
    )
    return grouped

def budget_status(year: int, month: int) -> dict:
    """
    Compute budget vs actual for a given year and month.
    """
    df = load_expenses_df()
    if df.empty:
        spent = 0.0
    else:
        # Filter expenses for the given month/year
        df["year"] = df["date"].dt.year
        df["month"] = df["date"].dt.month

        mask = (df["year"] == year) & (df["month"] == month)
        spent = float(df.loc[mask, "amount"].sum())

    # Get budget from db_service
    budget = db_service.get_budget(month, year)  # note order (month, year) in db_service
    if budget is None:
        budget = 0.0

    # Compute remaining and percentage
    remaining = budget - spent
    if budget > 0:
        percent_used = (spent / budget) * 100
    else:
        percent_used = 0.0

    # Determine status
    if budget == 0:
        status = "NO_BUDGET_SET"
    elif percent_used >= 100:
        status = "OVER_100"
    elif percent_used >= 80:
        status = "WARNING_80"
    else:
        status = "OK"

    return {
        "year": year,
        "month": month,
        "spent": round(spent, 2),
        "budget": round(budget, 2),
        "remaining": round(remaining, 2),
        "percent_used": round(percent_used, 2),
        "status": status,
    }

def export_category_summary(filepath: str = None) -> str:
    """
    Export category summary to CSV.
    Returns the path to the created file.
    """
    if filepath is None:
        reports_dir = os.path.join(PROJECT_ROOT, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        filepath = os.path.join(reports_dir, "category_summary.csv")

    summary_df = category_summary()
    summary_df.to_csv(filepath, index=False)
    return filepath


def export_monthly_summary(filepath: str = None) -> str:
    """
    Export monthly summary to CSV.
    Returns the path to the created file.
    """
    if filepath is None:
        reports_dir = os.path.join(PROJECT_ROOT, "reports")
        os.makedirs(reports_dir, exist_ok=True)
        filepath = os.path.join(reports_dir, "monthly_summary.csv")

    summary_df = monthly_summary()
    summary_df.to_csv(filepath, index=False)
    return filepath

if __name__ == "__main__":
    # Simple manual tests
    print("Loading expenses into DataFrame...")
    df = load_expenses_df()
    print(df)

    print("\nCategory summary:")
    print(category_summary())

    print("\nMonthly summary:")
    print(monthly_summary())

    print("\nBudget status for 12/2025:")
    print(budget_status(2025, 12))

    print("\nExporting CSV reports...")
    cat_path = export_category_summary()
    mon_path = export_monthly_summary()
    print("Category summary saved to:", cat_path)
    print("Monthly summary saved to:", mon_path)
