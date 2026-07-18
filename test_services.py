from services import storage
from models.expense import Expense

storage.ensure_data_files_exist()
print("ensure_data_files_exist ran without crashing")

categories = storage.load_categories()
assert len(categories) >= 11
print("categories.csv loaded, count is:")
print(len(categories))


expenses = storage.load_expenses()
count_before = len(expenses)

next_id = storage.generate_next_id(expenses)
new_expense = Expense(
    id=next_id,
    date="2026-07-18",
    category="Food",
    amount=250.0,
    payment_method="Cash",
    description="Groceries",
)
expenses.append(new_expense.to_dict())
storage.save_expenses(expenses)
print("added expense with id:")
print(next_id)

reloaded = storage.load_expenses()
count_after = len(reloaded)
assert count_after == count_before + 1

last_expense = reloaded[count_after - 1]
assert last_expense["amount"] == 250.0
assert last_expense["id"] == next_id
print("reloaded expense matches what was saved")


next_id_2 = storage.generate_next_id(reloaded)
assert next_id_2 == next_id + 1
print("generate_next_id correctly returns:")
print(next_id_2)

print("")
print("All M1 storage tests passed.")
