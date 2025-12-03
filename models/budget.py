class Budget:
    def __init__(self, month, year, budget_amount):
        self.month = month
        self.year = year
        self.budget_amount = budget_amount

    def __repr__(self):
        return (
            f"Budget(month={self.month!r}, year={self.year!r}, "
            f"budget_amount={self.budget_amount!r})"
        )
