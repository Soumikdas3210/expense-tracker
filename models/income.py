class Income:
    def __init__(self, id, date, source, amount, description=""):
        self.id = id
        self.date = date
        self.source = source
        self.amount = amount
        self.description = description

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "source": self.source,
            "amount": self.amount,
            "description": self.description,
        }

    @staticmethod
    def from_dict(data):
        return Income(
            id=data["id"],
            date=data["date"],
            source=data["source"],
            amount=data["amount"],
            description=data.get("description", ""),
        )
