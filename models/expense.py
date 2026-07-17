class Expense:
    def __init__(self, id, date, category, amount, payment_method,
                 description, notes="", is_recurring=False):
        self.id = id
        self.date = date
        self.category = category
        self.amount = amount
        self.payment_method = payment_method
        self.description = description
        self.notes = notes
        self.is_recurring = is_recurring

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "description": self.description,
            "notes": self.notes,
            "is_recurring": self.is_recurring,
        }

    @staticmethod
    def from_dict(data):
        return Expense(
            id=data["id"],
            date=data["date"],
            category=data["category"],
            amount=data["amount"],
            payment_method=data["payment_method"],
            description=data["description"],
            notes=data.get("notes", ""),
            is_recurring=data.get("is_recurring", False),
        )
