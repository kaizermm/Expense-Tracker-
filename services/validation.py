# services/validation.py

from datetime import datetime


class InvalidAmountError(Exception):
    """Raised when the given amount is not a valid positive number."""
    pass


class InvalidDateError(Exception):
    """Raised when the given date is not in a valid format."""
    pass


class InvalidCategoryError(Exception):
    """Raised when the given category is empty or invalid."""
    pass


class InvalidBudgetError(Exception):
    """Raised when the given budget amount is not valid."""
    pass


def validate_amount(amount_str: str) -> float:
    """
    Validate that amount_str can be converted to a positive float.
    """
    try:
        amount = float(amount_str)
    except (TypeError, ValueError):
        raise InvalidAmountError("Amount must be a numeric value.")

    if amount <= 0:
        raise InvalidAmountError("Amount must be greater than 0.")

    return amount


def validate_date(date_str: str) -> str:
    """
    Validate that date_str matches the format YYYY-MM-DD.
    """
    if not isinstance(date_str, str):
        raise InvalidDateError("Date must be a string in format YYYY-MM-DD.")

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        raise InvalidDateError("Date must be in format YYYY-MM-DD (e.g. 2025-12-02).")

    return date_str


def validate_category(category: str) -> str:
    """
    Validate that category is not empty or whitespace.
    """
    if not isinstance(category, str):
        raise InvalidCategoryError("Category must be a string.")

    cleaned = category.strip()
    if not cleaned:
        raise InvalidCategoryError("Category cannot be empty.")

    return cleaned


def validate_budget_amount(amount_str: str) -> float:
    """
    Validate budget amount. Reuses validate_amount but raises InvalidBudgetError
    """
    try:
        amount = validate_amount(amount_str)
    except InvalidAmountError as e:
        # Wrap it into a more specific error for budgets
        raise InvalidBudgetError(str(e)) from e

    return amount

if __name__ == "__main__":
    print("Running basic validation tests...")

    # Valid cases
    try:
        print("Amount:", validate_amount("100.50"))
        print("Date:", validate_date("2025-12-02"))
        print("Category:", validate_category("  Groceries  "))
        print("Budget:", validate_budget_amount("500"))
        print("All valid tests passed.")
    except Exception as e:
        print("Unexpected error for valid tests:", e)

    ...

