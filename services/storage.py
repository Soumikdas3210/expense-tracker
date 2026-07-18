import csv

from utils.constants import FILE_PATHS
from utils.constants import DEFAULT_CATEGORIES

EXPENSE_FIELDS = ["id", "date", "category", "amount", "payment_method", "description", "notes", "is_recurring"]
INCOME_FIELDS = ["id", "date", "source", "amount", "description"]
CATEGORY_FIELDS = ["id", "name", "is_default"]
BUDGET_FIELDS = ["category", "monthly_limit"]


def ensure_data_files_exist():
    try:
        file = open(FILE_PATHS["expenses"], "r", encoding="utf-8")
        file.close()
    except FileNotFoundError:
        file = open(FILE_PATHS["expenses"], "w", newline="", encoding="utf-8")
        writer = csv.DictWriter(file, fieldnames=EXPENSE_FIELDS)
        writer.writeheader()
        file.close()

    try:
        file = open(FILE_PATHS["income"], "r", encoding="utf-8")
        file.close()
    except FileNotFoundError:
        file = open(FILE_PATHS["income"], "w", newline="", encoding="utf-8")
        writer = csv.DictWriter(file, fieldnames=INCOME_FIELDS)
        writer.writeheader()
        file.close()

    try:
        file = open(FILE_PATHS["budgets"], "r", encoding="utf-8")
        file.close()
    except FileNotFoundError:
        file = open(FILE_PATHS["budgets"], "w", newline="", encoding="utf-8")
        writer = csv.DictWriter(file, fieldnames=BUDGET_FIELDS)
        writer.writeheader()
        file.close()

    try:
        file = open(FILE_PATHS["categories"], "r", encoding="utf-8")
        file.close()
    except FileNotFoundError:
        file = open(FILE_PATHS["categories"], "w", newline="", encoding="utf-8")
        writer = csv.DictWriter(file, fieldnames=CATEGORY_FIELDS)
        writer.writeheader()

        category_id = 1
        for name in DEFAULT_CATEGORIES:
            row = {"id": category_id, "name": name, "is_default": True}
            writer.writerow(row)
            category_id = category_id + 1

        file.close()


def load_expenses():
    file = open(FILE_PATHS["expenses"], "r", newline="", encoding="utf-8")
    reader = csv.DictReader(file)
    rows = list(reader)
    file.close()

    for row in rows:
        row["id"] = int(row["id"])
        row["amount"] = float(row["amount"])
        row["is_recurring"] = row["is_recurring"] == "True"

    return rows


def save_expenses(rows):
    file = open(FILE_PATHS["expenses"], "w", newline="", encoding="utf-8")
    writer = csv.DictWriter(file, fieldnames=EXPENSE_FIELDS)
    writer.writeheader()
    writer.writerows(rows)
    file.close()


def load_income():
    file = open(FILE_PATHS["income"], "r", newline="", encoding="utf-8")
    reader = csv.DictReader(file)
    rows = list(reader)
    file.close()

    for row in rows:
        row["id"] = int(row["id"])
        row["amount"] = float(row["amount"])

    return rows


def save_income(rows):
    file = open(FILE_PATHS["income"], "w", newline="", encoding="utf-8")
    writer = csv.DictWriter(file, fieldnames=INCOME_FIELDS)
    writer.writeheader()
    writer.writerows(rows)
    file.close()


def load_categories():
    file = open(FILE_PATHS["categories"], "r", newline="", encoding="utf-8")
    reader = csv.DictReader(file)
    rows = list(reader)
    file.close()

    for row in rows:
        row["id"] = int(row["id"])
        row["is_default"] = row["is_default"] == "True"

    return rows


def save_categories(rows):
    file = open(FILE_PATHS["categories"], "w", newline="", encoding="utf-8")
    writer = csv.DictWriter(file, fieldnames=CATEGORY_FIELDS)
    writer.writeheader()
    writer.writerows(rows)
    file.close()


def load_budgets():
    file = open(FILE_PATHS["budgets"], "r", newline="", encoding="utf-8")
    reader = csv.DictReader(file)
    rows = list(reader)
    file.close()

    for row in rows:
        row["monthly_limit"] = float(row["monthly_limit"])

    return rows


def save_budgets(rows):
    file = open(FILE_PATHS["budgets"], "w", newline="", encoding="utf-8")
    writer = csv.DictWriter(file, fieldnames=BUDGET_FIELDS)
    writer.writeheader()
    writer.writerows(rows)
    file.close()


def generate_next_id(rows):
    if len(rows) == 0:
        return 1

    highest_id = 0
    for row in rows:
        if row["id"] > highest_id:
            highest_id = row["id"]

    return highest_id + 1