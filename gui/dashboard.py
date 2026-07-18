import tkinter as tk
from tkinter import ttk
from gui.widgets import SummaryCard
from gui.widgets import CategoryDropdown
from services import expense_service
from services import income_service
from services import budget_service
from utils import get_today_str
from utils import format_currency


class DashboardFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.build_summary_cards()
        self.build_month_summary_label()
        self.build_search_bar()
        self.build_transaction_table()
        self.build_button_row()

        self.refresh_summary()
        self.refresh_transaction_table()

    def build_summary_cards(self):
        cards_frame = tk.Frame(self)
        cards_frame.pack(fill="x", padx=10, pady=10)

        self.income_card = SummaryCard(cards_frame, "Total Income", "$0.00")
        self.income_card.pack(side="left", expand=True, fill="x", padx=5)

        self.expense_card = SummaryCard(cards_frame, "Total Expense", "$0.00")
        self.expense_card.pack(side="left", expand=True, fill="x", padx=5)

        self.balance_card = SummaryCard(cards_frame, "Balance", "$0.00")
        self.balance_card.pack(side="left", expand=True, fill="x", padx=5)

        self.budget_card = SummaryCard(cards_frame, "Budget Remaining", "$0.00")
        self.budget_card.pack(side="left", expand=True, fill="x", padx=5)

    def build_month_summary_label(self):
        self.month_summary_label = tk.Label(self, text="This Month: ...", font=("Arial", 10))
        self.month_summary_label.pack(padx=10, pady=(0, 10), anchor="w")

    def build_search_bar(self):
        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", padx=10, pady=(0, 10))

        keyword_label = tk.Label(search_frame, text="Search:")
        keyword_label.pack(side="left")

        self.keyword_entry = tk.Entry(search_frame)
        self.keyword_entry.pack(side="left", padx=(5, 15))
        self.keyword_entry.bind("<KeyRelease>", self.on_search_changed)

        category_label = tk.Label(search_frame, text="Category:")
        category_label.pack(side="left")

        self.category_filter = CategoryDropdown(search_frame)
        self.category_filter.pack(side="left", padx=5)
        self.category_filter.bind("<<ComboboxSelected>>", self.on_search_changed)

        clear_button = tk.Button(search_frame, text="Clear", command=self.on_clear_search)
        clear_button.pack(side="left", padx=5)

    def build_transaction_table(self):
        columns = ("date", "category", "amount", "payment", "description")

        self.table = ttk.Treeview(self, columns=columns, show="headings", height=10)
        self.table.heading("date", text="Date")
        self.table.heading("category", text="Category")
        self.table.heading("amount", text="Amount")
        self.table.heading("payment", text="Payment")
        self.table.heading("description", text="Description")

        self.table.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def build_button_row(self):
        button_frame = tk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=(0, 10))

        add_expense_button = tk.Button(button_frame, text="Add Expense", command=self.on_add_expense)
        add_expense_button.pack(side="left", padx=5)

        add_income_button = tk.Button(button_frame, text="Add Income", command=self.on_add_income)
        add_income_button.pack(side="left", padx=5)

        edit_button = tk.Button(button_frame, text="Edit", command=self.on_edit_selected)
        edit_button.pack(side="left", padx=5)

        delete_button = tk.Button(button_frame, text="Delete", command=self.on_delete_selected)
        delete_button.pack(side="left", padx=5)

        analytics_button = tk.Button(button_frame, text="Analytics", command=self.open_analytics)
        analytics_button.pack(side="left", padx=5)

        reports_button = tk.Button(button_frame, text="Reports", command=self.open_reports)
        reports_button.pack(side="left", padx=5)

        settings_button = tk.Button(button_frame, text="Settings", command=self.open_settings)
        settings_button.pack(side="left", padx=5)

    def refresh_summary(self):
        total_income = income_service.get_total_income("month")
        all_expenses = expense_service.get_all_expenses()

        today_str = get_today_str()
        today_year_month = today_str[0:7]

        total_expense = 0.0
        for expense in all_expenses:
            expense_year_month = expense.date[0:7]
            if expense_year_month == today_year_month:
                total_expense = total_expense + expense.amount

        balance = total_income - total_expense

        budget_status = budget_service.get_budget_status_all(all_expenses)
        total_remaining = 0.0
        for category in budget_status:
            total_remaining = total_remaining + budget_status[category]["remaining"]

        self.income_card.update_value(format_currency(total_income))
        self.expense_card.update_value(format_currency(total_expense))
        self.balance_card.update_value(format_currency(balance))
        self.budget_card.update_value(format_currency(total_remaining))

        summary_text = "This Month: Income " + format_currency(total_income) + "  |  Expense " + format_currency(total_expense)
        self.month_summary_label.config(text=summary_text)

    def refresh_transaction_table(self):
        existing_rows = self.table.get_children()
        for row_id in existing_rows:
            self.table.delete(row_id)

        recent_expenses = expense_service.get_recent_expenses(10)

        for expense in recent_expenses:
            row_values = (expense.date, expense.category, format_currency(expense.amount), expense.payment_method, expense.description)
            self.table.insert("", "end", iid=str(expense.id), values=row_values)

    def on_search_changed(self, event):
        keyword = self.keyword_entry.get()
        category = self.category_filter.get()

        filters = {}
        if keyword != "":
            filters["keyword"] = keyword
        if category != "":
            filters["category"] = category

        existing_rows = self.table.get_children()
        for row_id in existing_rows:
            self.table.delete(row_id)

        if len(filters) == 0:
            results = expense_service.get_recent_expenses(10)
        else:
            results = expense_service.search_expenses(filters)

        for expense in results:
            row_values = (expense.date, expense.category, format_currency(expense.amount), expense.payment_method, expense.description)
            self.table.insert("", "end", iid=str(expense.id), values=row_values)

   