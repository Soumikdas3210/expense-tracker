import datetime

from services import storage
from models.income import Income


def get_all_income():
    rows = storage.load_income()

    income_list = []
    for row in rows:
        income = Income.from_dict(row)
        income_list.append(income)

    return income_list


def get_income_by_id(income_id):
    all_income = get_all_income()

    for income in all_income:
        if income.id == income_id:
            return income

    return None


def add_income(date, source, amount, description=""):
    rows = storage.load_income()
    new_id = storage.generate_next_id(rows)

    new_income = Income(
        id=new_id,
        date=date,
        source=source,
        amount=amount,
        description=description,
    )

    rows.append(new_income.to_dict())
    storage.save_income(rows)

    return new_income


def edit_income(income_id, **fields):
    rows = storage.load_income()
    updated_income = None

    updated_rows = []
    for row in rows:
        if row["id"] == income_id:
            for key in fields:
                row[key] = fields[key]
            updated_income = Income.from_dict(row)
        updated_rows.append(row)

    storage.save_income(updated_rows)
    return updated_income


def delete_income(income_id):
    rows = storage.load_income()
    found = False

    remaining_rows = []
    for row in rows:
        if row["id"] == income_id:
            found = True
        else:
            remaining_rows.append(row)

    storage.save_income(remaining_rows)
    return found


def search_income(filters):
    all_income = get_all_income()
    results = []

    for income in all_income:
        matches = True

        if "date" in filters:
            if income.date != filters["date"]:
                matches = False

        if "month" in filters:
            income_month = income.date[0:7]
            if income_month != filters["month"]:
                matches = False

        if "source" in filters:
            if income.source != filters["source"]:
                matches = False

        if "min_amount" in filters:
            if income.amount < filters["min_amount"]:
                matches = False

        if "max_amount" in filters:
            if income.amount > filters["max_amount"]:
                matches = False

        if "keyword" in filters:
            keyword_lower = filters["keyword"].lower()
            description_lower = income.description.lower()
            if keyword_lower not in description_lower:
                matches = False

        if matches == True:
            results.append(income)

    return results

def get_income_date_field(income):
    return income.date


def get_recent_income(n=10):
    all_income = get_all_income()
    sorted_income = sorted(all_income, key=get_income_date_field, reverse=True)
    return sorted_income[0:n]

def get_total_income(period="month"):
    all_income = get_all_income()

    today = datetime.date.today()
    today_year = today.year
    today_month = today.month

    total = 0.0

    for income in all_income:
        date_parts = income.date.split("-")
        income_year = int(date_parts[0])
        income_month = int(date_parts[1])

        include_this_one = False

        if period == "all":
            include_this_one = True

        if period == "year":
            if income_year == today_year:
                include_this_one = True

        if period == "month":
            if income_year == today_year:
                if income_month == today_month:
                    include_this_one = True

        if include_this_one == True:
            total = total + income.amount

    return total