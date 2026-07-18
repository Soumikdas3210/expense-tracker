import datetime


def format_currency(amount):
    formatted_number = "{:,.2f}".format(amount)
    return "$" + formatted_number


def parse_date(date_str):
    date_parts = date_str.split("-")
    year = int(date_parts[0])
    month = int(date_parts[1])
    day = int(date_parts[2])
    return datetime.date(year, month, day)


def get_today_str():
    today = datetime.date.today()

    year_str = str(today.year)

    month_str = str(today.month)
    if len(month_str) == 1:
        month_str = "0" + month_str

    day_str = str(today.day)
    if len(day_str) == 1:
        day_str = "0" + day_str

    return year_str + "-" + month_str + "-" + day_str


def get_month_range(d):
    year = d.year
    month = d.month
    start_date = datetime.date(year, month, 1)

    if month == 12:
        next_month_year = year + 1
        next_month = 1
    else:
        next_month_year = year
        next_month = month + 1

    first_day_next_month = datetime.date(next_month_year, next_month, 1)
    end_date = first_day_next_month - datetime.timedelta(days=1)

    return (start_date, end_date)


def get_year_range(d):
    year = d.year
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    return (start_date, end_date)