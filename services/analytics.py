import numpy as np


def build_amount_array(expenses):
    amounts = []
    for expense in expenses:
        amounts.append(expense.amount)
    return np.array(amounts)


def total_expense(expenses):
    amounts = build_amount_array(expenses)
    total = np.sum(amounts)
    return float(total)


def total_income(income):
    amounts = []
    for entry in income:
        amounts.append(entry.amount)

    amounts_array = np.array(amounts)
    total = np.sum(amounts_array)
    return float(total)


def average_expense(expenses):
    if len(expenses) == 0:
        return 0.0

    amounts = build_amount_array(expenses)
    average = np.mean(amounts)
    return float(average)


def median_expense(expenses):
    if len(expenses) == 0:
        return 0.0

    amounts = build_amount_array(expenses)
    median = np.median(amounts)
    return float(median)


def highest_expense(expenses):
    if len(expenses) == 0:
        return None

    amounts = build_amount_array(expenses)
    highest_amount = np.max(amounts)

    for expense in expenses:
        if expense.amount == float(highest_amount):
            return expense.to_dict()

    return None


def lowest_expense(expenses):
    if len(expenses) == 0:
        return None

    amounts = build_amount_array(expenses)
    lowest_amount = np.min(amounts)

    for expense in expenses:
        if expense.amount == float(lowest_amount):
            return expense.to_dict()

    return None


def std_dev_expense(expenses):
    if len(expenses) == 0:
        return 0.0

    amounts = build_amount_array(expenses)
    std_dev = np.std(amounts)
    return float(std_dev)


def variance_expense(expenses):
    if len(expenses) == 0:
        return 0.0

    amounts = build_amount_array(expenses)
    variance = np.var(amounts)
    return float(variance)


def get_month_totals(expenses):
    month_totals = {}

    for expense in expenses:
        month_key = expense.date[0:7]

        if month_key in month_totals:
            month_totals[month_key] = month_totals[month_key] + expense.amount
        else:
            month_totals[month_key] = expense.amount

    return month_totals


def monthly_growth(expenses):
    month_totals = get_month_totals(expenses)

    sorted_months = []
    for month_key in month_totals:
        sorted_months.append(month_key)
    sorted_months.sort()

    growth = {}

    for i in range(len(sorted_months)):
        current_month = sorted_months[i]
        current_total = month_totals[current_month]

        if i == 0:
            growth[current_month] = 0.0
        else:
            previous_month = sorted_months[i - 1]
            previous_total = month_totals[previous_month]

            if previous_total == 0:
                growth[current_month] = 0.0
            else:
                change = current_total - previous_total
                percent_change = (change / previous_total) * 100
                growth[current_month] = float(percent_change)

    return growth


def category_percentage(expenses):
    if len(expenses) == 0:
        return {}

    category_totals = {}
    grand_total = 0.0

    for expense in expenses:
        grand_total = grand_total + expense.amount

        if expense.category in category_totals:
            category_totals[expense.category] = category_totals[expense.category] + expense.amount
        else:
            category_totals[expense.category] = expense.amount

    percentages = {}
    for category in category_totals:
        category_amount = category_totals[category]
        percent = (category_amount / grand_total) * 100
        percentages[category] = float(percent)

    return percentages


def expense_frequency(expenses):
    frequency = {}

    for expense in expenses:
        if expense.category in frequency:
            frequency[expense.category] = frequency[expense.category] + 1
        else:
            frequency[expense.category] = 1

    return frequency


def spending_trend(expenses, period="monthly"):
    if period == "monthly":
        return get_month_totals(expenses)

    if period == "yearly":
        year_totals = {}
        for expense in expenses:
            year_key = expense.date[0:4]
            if year_key in year_totals:
                year_totals[year_key] = year_totals[year_key] + expense.amount
            else:
                year_totals[year_key] = expense.amount
        return year_totals

    if period == "daily":
        day_totals = {}
        for expense in expenses:
            day_key = expense.date
            if day_key in day_totals:
                day_totals[day_key] = day_totals[day_key] + expense.amount
            else:
                day_totals[day_key] = expense.amount
        return day_totals

    return {}
  
