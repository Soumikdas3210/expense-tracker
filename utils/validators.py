from datetime import datetime

from utils.constants import DATE_FORMAT
from utils.constants import PAYMENT_METHODS


def validate_amount(amount):
    try:
        amount_as_number = float(amount)
    except TypeError:
        return False
    except ValueError:
        return False

    if amount_as_number > 0:
        return True
    else:
        return False


def validate_date(date_str):
    if date_str == "":
        return False

    try:
        datetime.strptime(date_str, DATE_FORMAT)
        return True
    except ValueError:
        return False


def validate_category(category, valid_categories):
    if category in valid_categories:
        return True
    else:
        return False


def validate_payment_method(method):
    if method in PAYMENT_METHODS:
        return True
    else:
        return False


def validate_description(description):
    if len(description) <= 100:
        return True
    else:
        return False


def is_duplicate_id(new_id, existing_ids):
    if new_id in existing_ids:
        return True
    else:
        return False
