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


    