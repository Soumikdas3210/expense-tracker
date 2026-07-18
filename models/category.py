class Category:
    def __init__(self, id, name, is_default=False):
        self.id = id
        self.name = name
        self.is_default = is_default

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "is_default": self.is_default,
        }

    @staticmethod
    def from_dict(data):
        return Category(
            id=data["id"],
            name=data["name"],
            is_default=data.get("is_default", False),
        )
      
