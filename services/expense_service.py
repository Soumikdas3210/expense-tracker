from services import storage
from models.expense import Expense

def get_all_expenses():
    rows = storage.load_expenses()

    expenses = []
    for row in rows:
        expense = Expense.from_dict(row)
        expenses.append(expense)
    return expenses

def get_expense_by_id(expense_id):
    all_expenses = get_all_expenses()

    for expense in all_expenses:
        if expense.id == expense_id:
            return expense
        
    return None

def add_expense(date, category, amount, payment_method, description, notes="", is_recurring=False):
    rows = storage.load_expenses()
    new_id = storage.generate_next_id(rows)
    new_expense = Expense(
        id=new_id,
        date=date,
        category=category,
        amount=amount,
        payment_method=payment_method,
        description=description,
        notes=notes,
        is_recurring=is_recurring,
    )

    rows.append(new_expense.to_dict())
    storage.save_expenses(rows)

    return new_expense

def edit_expense(expense_id, **fields):
    rows = storage.load_expenses()
    updated_expense = None

    updated_rows = []
    for row in rows:
        if row["id"] == expense_id:
            for key in fields:
                row[key] = fields[key]
            updated_expense = Expense.from_dict(row)
        updated_rows.append(row)    
    
    storage.save_expenses(updated_rows)
    return updated_expense

def delete_expense(expense_id):
    rows = storage.load_expenses()
    found = False

    remaining_rows = []
    for row in rows:
        if row["id"] == expense_id:
            found = True
        else:
            remaining_rows.append(row)

    storage.save_expenses(remaining_rows)
    return found


def duplicate_expense(expense_id):
    original = get_expense_by_id(expense_id)

    if original is None:
        return None

    return add_expense(
        date=original.date,
        category=original.category,
        amount=original.amount,
        payment_method=original.payment_method,
        description=original.description,
        notes=original.notes,
        is_recurring=original.is_recurring,
    )


def search_expenses(filters):
    all_expenses = get_all_expenses()
    results = []

    for expense in all_expenses:
        matches = True

        if "date" in filters:
            if expense.date != filters["date"]:
                matches = False

        if "month" in filters:
            expense_month = expense.date[0:7]
            if expense_month != filters["month"]:
                matches = False

        if "category" in filters:
            if expense.category != filters["category"]:
                matches = False

        if "min_amount" in filters:
            if expense.amount < filters["min_amount"]:
                matches = False

        if "max_amount" in filters:
            if expense.amount > filters["max_amount"]:
                matches = False

        if "payment_method" in filters:
            if expense.payment_method != filters["payment_method"]:
                matches = False

        if "keyword" in filters:
            keyword_lower = filters["keyword"].lower()
            description_lower = expense.description.lower()
            if keyword_lower not in description_lower:
                matches = False

        if matches == True:
            results.append(expense)

    return results


def get_expense_date_field(expense):
    return expense.date


def get_recent_expenses(n=10):
    all_expenses = get_all_expenses()
    sorted_expenses = sorted(all_expenses, key=get_expense_date_field, reverse=True)
    return sorted_expenses[0:n]


def mark_recurring(expense_id, value=True):
    return edit_expense(expense_id, is_recurring=value)