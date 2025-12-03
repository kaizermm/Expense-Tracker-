import os
import sys

# --- Make sure Python can see the project root (expense_tracker) ---

# CURRENT_DIR = .../expense_tracker/services
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

# PROJECT_ROOT = .../expense_tracker
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

# Add project root to sys.path if not already there
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Now these imports will work, because 'database' and 'models'
# are folders under PROJECT_ROOT (expense_tracker)
from database.db_connection import get_connection
from models.expense import Expense
from models.budget import Budget

def add_expense(expense):
    """Insert expense into the expenses table"""
    conn = get_connection()
    cursor = conn.cursor()

    #Now using 4 columns and 4 placeholders
    cursor.execute(
        """
        INSERT INTO expenses (category, amount, date, description)
        VALUES (?, ?, ?, ?);
        """,
        expense.to_tuple()   # this must return (category, amount, date, description)
    )

    conn.commit()
    conn.close()

def get_all_expenses():
    """Fetch expenses from the database."""
    conn = get_connection()
    cursor = conn.cursor()

    # Also selecting description now
    cursor.execute(
        """
        SELECT id, category, amount, date, description
        FROM expenses
        ORDER BY date;
        """
    )

    rows = cursor.fetchall()
    conn.close()
    return rows


def get_expense_by_id(expense_id: int):
    """
    Fetch a single expense by ID.
    Returns a tuple or None if not found.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, category, amount, date, description FROM expenses WHERE id = ?",
        (expense_id,),
    )
    row = cursor.fetchone()

    conn.close()
    return row


def update_expense(expense_id: int, expense: Expense) -> bool:
    """
    Update an existing expense.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE expenses
        SET category = ?, amount = ?, date = ?, description = ?
        WHERE id = ?
        """,
        (expense.category, expense.amount, expense.date, expense.description, expense_id),
    )

    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated

def delete_expense(expense_id: int) -> bool:
    """
    Delete an expense by ID.
    Returns True if a row was deleted, False otherwise.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted

def set_budget(budget: Budget) -> None:
    """
    Insert or update the budget for a given month/year.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO budgets (month, year, amount)
        VALUES (?, ?, ?)
        """,
        (budget.month, budget.year, budget.budget_amount),
    )

    conn.commit()
    conn.close()

def get_budget(month: int, year: int):
    """
    Get the budget amount for a given month/year.
    Returns the amount as float, or None if not set.
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT amount FROM budgets WHERE month = ? AND year = ?",
        (month, year),
    )
    row = cursor.fetchone()

    conn.close()
    if row is None:
        return None
    return float(row[0])


if __name__ == "__main__":
    from models.expense import Expense
    from models.budget import Budget
    from database.db_connection import create_tables  # if you exposed this

    # Ensure tables exist
    try:
        create_tables()
    except Exception:
        # If you don't want to import create_tables here, you can ignore this
        pass

    # 1. Add an expense
    exp = Expense(category="Test", amount=12.5, date="2025-12-02", description="Day 3 test")
    exp_id = add_expense(exp)
    print("Inserted expense ID:", exp_id)

    # 2. Fetch all expenses
    print("All expenses:")
    for row in get_all_expenses():
        print(row)

    # 3. Update the expense
    exp_updated = Expense(category="Test-Updated", amount=20.0, date="2025-12-03", description="Updated")
    updated = update_expense(exp_id, exp_updated)
    print("Updated?", updated)

    # 4. Delete the expense
    deleted = delete_expense(exp_id)
    print("Deleted?", deleted)

    # 5. Set and get a budget
    bud = Budget(month=12, year=2025, budget_amount=1000.0)
    set_budget(bud)
    print("Budget for 12/2025:", get_budget(12, 2025))








