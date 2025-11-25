from database.db_connection import get_connection
from models.expense import Expense


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


def get_expenses_by_category(category):
    """Fetch expenses by category (case-insensitive)."""
    conn = get_connection()
    cursor = conn.cursor()

    # Also selecting description here
    cursor.execute(
        """
        SELECT id, category, amount, date, description
        FROM expenses
        WHERE LOWER(category) = LOWER(?)
        ORDER BY date;
        """,
        (category,)
    )

    rows = cursor.fetchall()
    conn.close()
    return rows



