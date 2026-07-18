from services import storage
from models.expense import Expense

# 1. First run: creates data/*.csv from scratch if they don't exist yet,
#    and seeds categories.csv with the defaults. Should never crash,
#    even with zero files present.
storage.ensure_data_files_exist()
print("ensure_data_files_exist ran without crashing")

# 2. Categories should be seeded
categories = storage.load_categories()
assert len(categories) >= 11
print("categories.csv loaded, count is:")
print(len(categories))

# 3. Load-modify-save round trip on expenses
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

# 4. Reload from disk and check it actually persisted correctly
reloaded = storage.load_expenses()
count_after = len(reloaded)
assert count_after == count_before + 1

last_expense = reloaded[count_after - 1]
assert last_expense["amount"] == 250.0
assert last_expense["id"] == next_id
print("reloaded expense matches what was saved")

# 5. Confirm auto-increment actually increments
next_id_2 = storage.generate_next_id(reloaded)
assert next_id_2 == next_id + 1
print("generate_next_id correctly returns:")
print(next_id_2)

print("")
print("All M1 storage tests passed.")