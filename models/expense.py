class Expense:
    """A simple class"""

    def __init__(self, category, amount, date, description=""):
        self.category = category      
        self.amount = amount          
        self.date = date              
        self.description = description  

    def to_tuple(self):
        """Return data for the SQL INSERT."""
        return (self.category, self.amount, self.date, self.description)
