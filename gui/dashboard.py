import tkinter as tk
from gui.widgets import SummaryCard
from gui.widgets import CategoryDropdown


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