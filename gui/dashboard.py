import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from services import expense_service
from services import income_service
from services import budget_service
from gui.widgets import SummaryCard
from gui.widgets import CategoryDropdown
from utils.helpers import format_currency
from utils.helpers import get_today_str
from gui.add_expense import AddExpenseWindow
from gui.add_income import AddIncomeWindow


class DashboardFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.build_summary_cards()
        self.build_month_summary_label()
        self.build_budget_warning_label()
        self.build_search_bar()
        self.build_transaction_table()
        self.build_button_row()

        self.refresh_summary()
        self.refresh_transaction_table()

    def build_summary_cards(self):
        cards_frame = tk.Frame(self)
        cards_frame.pack(fill="x", padx=10, pady=10)

        self.income_card = SummaryCard(cards_frame, "Income (This Month)", "$0.00")
        self.income_card.pack(side="left", expand=True, fill="x", padx=5)

        self.expense_card = SummaryCard(cards_frame, "Expense (This Month)", "$0.00")
        self.expense_card.pack(side="left", expand=True, fill="x", padx=5)

        self.balance_card = SummaryCard(cards_frame, "Balance (This Month)", "$0.00")
        self.balance_card.pack(side="left", expand=True, fill="x", padx=5)

        self.budget_card = SummaryCard(cards_frame, "Budget Remaining (Budgeted Categories)", "$0.00")
        self.budget_card.pack(side="left", expand=True, fill="x", padx=5)

        budget_note = tk.Label(self, text="Budget Remaining only totals categories that have a budget set in Settings.", font=("Arial", 9), fg="gray")
        budget_note.pack(padx=10, anchor="w")

    def build_month_summary_label(self):
        self.month_summary_label = tk.Label(self, text="This Month: ...", font=("Arial", 10))
        self.month_summary_label.pack(padx=10, pady=(0, 5), anchor="w")

    def build_budget_warning_label(self):
        self.budget_warning_label = tk.Label(self, text="", fg="red", font=("Arial", 10, "bold"))
        self.budget_warning_label.pack(padx=10, pady=(0, 10), anchor="w")

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
        table_note = tk.Label(self, text="Recent Transactions (all dates — not limited to this month)", font=("Arial", 9), fg="gray")
        table_note.pack(padx=10, anchor="w")

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
        over_budget_categories = []
        budgeted_categories = []
        for category in budget_status:
            total_remaining = total_remaining + budget_status[category]["remaining"]
            budgeted_categories.append(category)
            if budget_status[category]["over"] == True:
                over_budget_categories.append(category)

        self.income_card.update_value(format_currency(total_income))
        self.expense_card.update_value(format_currency(total_expense))
        self.balance_card.update_value(format_currency(balance))
        self.budget_card.update_value(format_currency(total_remaining))

        summary_text = "This Month: Income " + format_currency(total_income) + "  |  Expense " + format_currency(total_expense)
        self.month_summary_label.config(text=summary_text)

        if len(over_budget_categories) > 0:
            categories_text = ", ".join(over_budget_categories)
            warning_text = "Over budget: " + categories_text
            self.budget_warning_label.config(text=warning_text, fg="red")
        elif len(budgeted_categories) > 0:
            categories_text = ", ".join(budgeted_categories)
            info_text = "Budgets tracked: " + categories_text + " (all within limit)"
            self.budget_warning_label.config(text=info_text, fg="gray")
        else:
            self.budget_warning_label.config(text="")

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

    def on_clear_search(self):
        self.keyword_entry.delete(0, "end")
        self.category_filter.set("")
        self.refresh_transaction_table()

    def get_selected_expense_id(self):
        selection = self.table.selection()
        if len(selection) == 0:
            return None
        selected_id_str = selection[0]
        return int(selected_id_str)

    def on_add_expense(self):
        AddExpenseWindow(self, on_success=self.on_transaction_saved)

    def on_add_income(self):
        AddIncomeWindow(self, on_success=self.on_transaction_saved)

    def on_edit_selected(self):
        expense_id = self.get_selected_expense_id()
        if expense_id is None:
            messagebox.showinfo("No Selection", "Select a transaction first.")
            return
        AddExpenseWindow(self, on_success=self.on_transaction_saved, expense_id=expense_id)

    def on_transaction_saved(self):
        self.refresh_summary()
        self.refresh_transaction_table()

    def on_delete_selected(self):
        expense_id = self.get_selected_expense_id()
        if expense_id is None:
            messagebox.showinfo("No Selection", "Select a transaction first.")
            return

        confirmed = messagebox.askyesno("Confirm Delete", "Delete this transaction?")
        if confirmed == True:
            expense_service.delete_expense(expense_id)
            self.refresh_summary()
            self.refresh_transaction_table()

    def open_analytics(self):
        self.app.show_frame("Analytics")
    

    def open_reports(self):
        self.app.show_frame("Reports")

    def open_settings(self):
        self.app.show_frame("Settings")
