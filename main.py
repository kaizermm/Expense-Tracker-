from database.db_connection import initialize_db
from models.expense import Expense
from services.db_service import add_expense,get_all_expenses, get_expenses_by_category

def add_expense_flow():
    print("---add new expense")
    category=input("Category (ex:Food, Rend, Transport)")
    amount_str=(input('Amount :'))
    date=input("Date (YYYY-MM-DD)")
    description=input('Enter the description')
    #convert into float fomat
    try:
        amount = float(amount_str)
    except ValueError:
        print("Invalid amount. Please enter a number like 12.5")
        return

    expense = Expense(category, amount, date,description)
    add_expense(expense)
    print("Expense saved!")

def show_expenses(expenses):
    """print a list of expense"""
    if not expenses:
        print('no expense found')
        return
    #print header row and column name
    print("\nID | Date | Category | Amount | Description")
    print("-"*70)
    for row in expenses:
        #print each row formated array
        expense_id, category, amount, date, description = row
        print(f"{expense_id:<3} {date:<11} {category:<10} {amount:>7.2f} {description or ''}")
def view_all_expenses_flow():
    print("\n=== All expenses ===")
    #call database service to fetch all expense
    expenses=get_all_expenses()
    show_expenses(expenses)

def search_by_category_flow():
    print('search expense by category')
    #ask user what category to search for
    category=input("Enter category :")
    #call function that queries database
    expenses=get_expenses_by_category(category)
    print(f"Category : {category}")
    #display filter result
    show_expenses(expenses)

def main():
    # make sure database and tables exist
    initialize_db()
    #start a loop
    while True:
        print("\n=== Personal Expense Tracker ===")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Search expenses by category")
        print("4. Exit")
        choice = input("Choose an option (1-4): ")
        if choice == "1":
            add_expense_flow()
        elif choice == "2":
            view_all_expenses_flow()
        elif choice == "3":
            search_by_category_flow()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice, please enter a number between 1 and 4.")
    # for now, just allow adding one expense
    add_expense_flow()


if __name__ == "__main__":
    main()
