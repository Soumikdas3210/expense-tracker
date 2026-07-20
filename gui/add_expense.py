import tkinter as tk
from tkinter import ttk

from services import expense_service
from utils import validators
from utils.constants import PAYMENT_METHODS
from gui.widgets import CategoryDropdown
from gui.widgets import show_success


class AddExpenseWindow(tk.Toplevel):
    def __init__(self, parent, on_success=None, expense_id=None):
        super().__init__(parent)
        self.on_success = on_success
        self.expense_id = expense_id

        if expense_id is None:
            self.title("Add Expense")
        else:
            self.title("Edit Expense")

        self.geometry("400x520")

        self.build_form()

        if expense_id is not None:
            expense = expense_service.get_expense_by_id(expense_id)
            self.populate_for_edit(expense)

    def build_form(self):
        date_label = tk.Label(self, text="Date (YYYY-MM-DD)")
        date_label.pack(padx=10, pady=(10, 0), anchor="w")
        self.date_entry = tk.Entry(self)
        self.date_entry.pack(padx=10, fill="x")
        self.date_error_label = tk.Label(self, text="", fg="red")
        self.date_error_label.pack(padx=10, anchor="w")

        category_label = tk.Label(self, text="Category")
        category_label.pack(padx=10, pady=(10, 0), anchor="w")
        self.category_dropdown = CategoryDropdown(self)
        self.category_dropdown.pack(padx=10, fill="x")
        self.category_error_label = tk.Label(self, text="", fg="red")
        self.category_error_label.pack(padx=10, anchor="w")

        amount_label = tk.Label(self, text="Amount")
        amount_label.pack(padx=10, pady=(10, 0), anchor="w")
        self.amount_entry = tk.Entry(self)
        self.amount_entry.pack(padx=10, fill="x")
        self.amount_error_label = tk.Label(self, text="", fg="red")
        self.amount_error_label.pack(padx=10, anchor="w")

        payment_label = tk.Label(self, text="Payment Method")
        payment_label.pack(padx=10, pady=(10, 0), anchor="w")
        self.payment_dropdown = ttk.Combobox(self, values=PAYMENT_METHODS)
        self.payment_dropdown.pack(padx=10, fill="x")
        self.payment_error_label = tk.Label(self, text="", fg="red")
        self.payment_error_label.pack(padx=10, anchor="w")

        description_label = tk.Label(self, text="Description")
        description_label.pack(padx=10, pady=(10, 0), anchor="w")
        self.description_entry = tk.Entry(self)
        self.description_entry.pack(padx=10, fill="x")
        self.description_error_label = tk.Label(self, text="", fg="red")
        self.description_error_label.pack(padx=10, anchor="w")

        notes_label = tk.Label(self, text="Notes")
        notes_label.pack(padx=10, pady=(10, 0), anchor="w")
        self.notes_text = tk.Text(self, height=3)
        self.notes_text.pack(padx=10, fill="x")

        self.recurring_var = tk.BooleanVar()
        self.recurring_check = tk.Checkbutton(self, text="Recurring", variable=self.recurring_var)
        self.recurring_check.pack(padx=10, pady=10, anchor="w")

        button_frame = tk.Frame(self)
        button_frame.pack(padx=10, pady=10, fill="x")

        save_button = tk.Button(button_frame, text="Save", command=self.on_save)
        save_button.pack(side="left", padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=self.on_cancel)
        cancel_button.pack(side="left", padx=5)

    def populate_for_edit(self, expense):
        self.date_entry.insert(0, expense.date)
        self.category_dropdown.set(expense.category)
        self.amount_entry.insert(0, str(expense.amount))
        self.payment_dropdown.set(expense.payment_method)
        self.description_entry.insert(0, expense.description)
        self.notes_text.insert("1.0", expense.notes)
        self.recurring_var.set(expense.is_recurring)

  
