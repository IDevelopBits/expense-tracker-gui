from datetime import datetime

class Expense:
    _id_counter = 1

    def __init__(self, title, description, date_, amount):
        self.id = Expense._id_counter
        Expense._id_counter += 1

        self.title = title
        self.description = description
        self.amount = amount
        self.date_ = date_

    # Prints expense details
    def print_details(self):
        print(f'ID {self.id}: {self.title} {self.description} {self.amount} {self.date_}')
        return f'ID {self.id}: {self.title} {self.description} {self.amount} {self.date_} '

    def to_dict(self):
        return {"id": self.id, "title": self.title, "date": self.date_.isoformat(), "description": self.description,
                "amount": self.amount}

    # Loads object from json
    @classmethod
    def from_dict(cls, data):
        obj = cls(data["title"], data["description"], datetime.fromisoformat(data["date"]), data["amount"])
        obj.id = data["id"]
        return obj
