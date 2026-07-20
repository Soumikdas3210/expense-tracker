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
        
    def validate_form(self):
        is_valid = True

        date_value = self.date_entry.get()
        if validators.validate_date(date_value) == True:
            self.date_error_label.config(text="")
        else:
            self.date_error_label.config(text="Date must be in YYYY-MM-DD format.")
            is_valid = False

        category_value = self.category_dropdown.get()
        valid_categories = self.category_dropdown["values"]
        if validators.validate_category(category_value, valid_categories) == True:
            self.category_error_label.config(text="")
        else:
            self.category_error_label.config(text="Please select a valid category.")
            is_valid = False

        amount_value = self.amount_entry.get()
        if validators.validate_amount(amount_value) == True:
            self.amount_error_label.config(text="")
        else:
            self.amount_error_label.config(text="Amount must be a positive number.")
            is_valid = False

        payment_value = self.payment_dropdown.get()
        if validators.validate_payment_method(payment_value) == True:
            self.payment_error_label.config(text="")
        else:
            self.payment_error_label.config(text="Please select a valid payment method.")
            is_valid = False

        description_value = self.description_entry.get()
        if validators.validate_description(description_value) == True:
            self.description_error_label.config(text="")
        else:
            self.description_error_label.config(text="Description must be 100 characters or fewer.")
            is_valid = False

        return is_valid

    def on_save(self):
        form_is_valid = self.validate_form()
        if form_is_valid == False:
            return

        date_value = self.date_entry.get()
        category_value = self.category_dropdown.get()
        amount_value = float(self.amount_entry.get())
        payment_value = self.payment_dropdown.get()
        description_value = self.description_entry.get()
        notes_value = self.notes_text.get("1.0", "end-1c")
        recurring_value = self.recurring_var.get()

        if self.expense_id is None:
            expense_service.add_expense(
                date=date_value,
                category=category_value,
                amount=amount_value,
                payment_method=payment_value,
                description=description_value,
                notes=notes_value,
                is_recurring=recurring_value,
            )
            show_success("Expense added.")
        else:
            expense_service.edit_expense(
                self.expense_id,
                date=date_value,
                category=category_value,
                amount=amount_value,
                payment_method=payment_value,
                description=description_value,
                notes=notes_value,
                is_recurring=recurring_value,
            )
            show_success("Expense updated.")

        if self.on_success is not None:
            self.on_success()

        self.destroy()

    def on_cancel(self):
        self.destroy()
  
