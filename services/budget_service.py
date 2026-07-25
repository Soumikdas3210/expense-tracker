import datetime

from services import storage


def set_budget(category, monthly_limit):
    rows = storage.load_budgets()

    found = False
    updated_rows = []
    for row in rows:
        if row["category"] == category:
            row["monthly_limit"] = monthly_limit
            found = True
        updated_rows.append(row)

    if found == False:
        new_row = {"category": category, "monthly_limit": monthly_limit}
        updated_rows.append(new_row)

    storage.save_budgets(updated_rows)

def remove_budget(category):
    rows = storage.load_budgets()

    remaining_rows = []
    for row in rows:
        if row["category"] != category:
            remaining_rows.append(row)

    storage.save_budgets(remaining_rows)    


def get_budget(category):
    rows = storage.load_budgets()

    for row in rows:
        if row["category"] == category:
            return row["monthly_limit"]

    return None


def get_all_budgets():
    rows = storage.load_budgets()

    budgets = {}
    for row in rows:
        budgets[row["category"]] = row["monthly_limit"]

    return budgets


def calculate_budget_used(category, expenses, month=None):
    if month is None:
        today = datetime.date.today()
        target_year = today.year
        target_month = today.month
    else:
        month_parts = month.split("-")
        target_year = int(month_parts[0])
        target_month = int(month_parts[1])

    total = 0.0
    for expense in expenses:
        if expense.category == category:
            date_parts = expense.date.split("-")
            expense_year = int(date_parts[0])
            expense_month = int(date_parts[1])

            if expense_year == target_year:
                if expense_month == target_month:
                    total = total + expense.amount

    return total


def get_budget_remaining(category, expenses):
    monthly_limit = get_budget(category)

    if monthly_limit is None:
        return None

    used = calculate_budget_used(category, expenses)
    remaining = monthly_limit - used
    return remaining


def is_over_budget(category, expenses):
    monthly_limit = get_budget(category)

    if monthly_limit is None:
        return False

    used = calculate_budget_used(category, expenses)

    if used > monthly_limit:
        return True
    else:
        return False


def get_budget_status_all(expenses):
    all_budgets = get_all_budgets()

    status = {}
    for category in all_budgets:
        monthly_limit = all_budgets[category]
        used = calculate_budget_used(category, expenses)
        remaining = monthly_limit - used

        over = False
        if used > monthly_limit:
            over = True

        status[category] = {
            "used": used,
            "limit": monthly_limit,
            "remaining": remaining,
            "over": over,
        }

    return status