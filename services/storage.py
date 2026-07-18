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
