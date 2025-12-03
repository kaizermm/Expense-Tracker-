from database.db_connection import initialize_db
from models.expense import Expense
from services.db_service import (
    add_expense,
    get_all_expenses,
    get_expenses_by_category,
    get_total_spent,
    get_monthly_total,
    get_monthly_category_totals,
)


def add_expense_flow():
    print("=== Add a new expense ===")

    category = input("Category (e.g. Food, Rent, Transport): ").strip()
    amount_str = input("Amount: ").strip()
    date = input("Date (YYYY-MM-DD): ").strip()
    description = input("Description (optional): ").strip()

    # try to convert the amount to a number
    try:
        amount = float(amount_str)
    except ValueError:
        print("Invalid amount. Please enter a number like 12.5")
        return

    # create an Expense object
    expense = Expense(category, amount, date, description)

    # save it to the database
    add_expense(expense)

    print("Expense saved.")


def show_expenses(expenses):
    """Print a list of expenses."""
    if not expenses:
        print("No expenses found.")
        return

    print("\nID | Date       | Category   | Amount  | Description")
    print("-" * 70)

    for row in expenses:
        # row is in this order: (id, category, amount, date, description)
        expense_id = row[0]
        category = row[1]
        amount = row[2]
        date = row[3]
        description = row[4]

        # simple formatting using f-string
        print(f"{expense_id:<3} {date:<11} {category:<10} {amount:>7.2f}  {description or ''}")


def view_all_expenses_flow():
    print("\n=== All expenses ===")
    expenses = get_all_expenses()
    show_expenses(expenses)


def search_by_category_flow():
    print("\n=== Search expenses by category ===")
    category = input("Enter category: ").strip()
    expenses = get_expenses_by_category(category)
    print(f"Results for category: {category}")
    show_expenses(expenses)


def view_total_spent_flow():
    """Show total spent across all expenses (no filters)."""
    total = get_total_spent()
    print(f"\nTotal spent on all expenses: {total:.2f}")


def view_monthly_summary_flow():
    """Show summary for a specific month."""
    print("\n=== Monthly summary ===")

    year_str = input("Enter year (e.g. 2025): ").strip()
    month_str = input("Enter month (1-12): ").strip()

    # check that year and month are valid integers
    try:
        year = int(year_str)
        month = int(month_str)
    except ValueError:
        print("Please enter valid numbers for year and month.")
        return

    total = get_monthly_total(year, month)

    if total == 0.0:
        print(f"No expenses found for {year}-{month:02d}.")
        return

    print(f"\nTotal spent in {year}-{month:02d}: {total:.2f}")

    # category breakdown
    category_rows = get_monthly_category_totals(year, month)

    if not category_rows:
        print("No category breakdown available.")
        return

    print("\nBy category:")
    print("Category   | Total")
    print("-" * 25)
    for row in category_rows:
        category = row[0]
        cat_total = row[1]
        print(f"{category:<10} {cat_total:>8.2f}")


def main():
    # make sure database and tables exist
    initialize_db()

    print("Welcome to the Personal Expense Tracker!")
    print("Press Ctrl+C at any time to exit.\n")

    try:
        while True:
            print("\n=== Personal Expense Tracker ===")
            print("1. Add expense")
            print("2. View all expenses")
            print("3. Search expenses by category")
            print("4. View total spent (all time)")
            print("5. View monthly summary")
            print("6. Exit")

            choice = input("Choose an option (1-6): ").strip()

            if choice == "1":
                try:
                    add_expense_flow()
                except Exception as e:
                    print("An error happened while adding an expense:", e)

            elif choice == "2":
                try:
                    view_all_expenses_flow()
                except Exception as e:
                    print("An error happened while viewing expenses:", e)

            elif choice == "3":
                try:
                    search_by_category_flow()
                except Exception as e:
                    print("An error happened while searching expenses:", e)

            elif choice == "4":
                try:
                    view_total_spent_flow()
                except Exception as e:
                    print("An error happened while calculating total spent:", e)

            elif choice == "5":
                try:
                    view_monthly_summary_flow()
                except Exception as e:
                    print("An error happened while showing monthly summary:", e)

            elif choice == "6":
                print("Goodbye!")
                break
            else:
                print("Invalid choice, please enter a number between 1 and 6.")

    except KeyboardInterrupt:
        # handles Ctrl+C
        print("\n\nInterrupted by user. Exiting the program. Goodbye!")


if __name__ == "__main__":
    main()
