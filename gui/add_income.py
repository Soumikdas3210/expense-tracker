import tkinter as tk
from tkinter import ttk

from services import income_service
from utils import validators
from gui.widgets import show_success

INCOME_SOURCES = ["Salary", "Investment", "Freelance", "Other"]


class AddIncomeWindow(tk.Toplevel):
    def __init__(self, parent, on_success=None, income_id=None):
        super().__init__(parent)
        self.on_success = on_success
        self.income_id = income_id

        if income_id is None:
            self.title("Add Income")
        else:
            self.title("Edit Income")

        self.geometry("400x380")

        self.build_form()

        if income_id is not None:
            income = income_service.get_income_by_id(income_id)
            self.populate_for_edit(income)

    def build_form(self):
        date_label = tk.Label(self, text="Date (YYYY-MM-DD)")
        date_label.pack(padx=10, pady=(10, 0), anchor="w")
        self.date_entry = tk.Entry(self)
        self.date_entry.pack(padx=10, fill="x")
        self.date_error_label = tk.Label(self, text="", fg="red")
        self.date_error_label.pack(padx=10, anchor="w")

        source_label = tk.Label(self, text="Source")
        source_label.pack(padx=10, pady=(10, 0), anchor="w")
        self.source_dropdown = ttk.Combobox(self, values=INCOME_SOURCES)
        self.source_dropdown.pack(padx=10, fill="x")
        self.source_error_label = tk.Label(self, text="", fg="red")
        self.source_error_label.pack(padx=10, anchor="w")

        amount_label = tk.Label(self, text="Amount")
        amount_label.pack(padx=10, pady=(10, 0), anchor="w")
        self.amount_entry = tk.Entry(self)
        self.amount_entry.pack(padx=10, fill="x")
        self.amount_error_label = tk.Label(self, text="", fg="red")
        self.amount_error_label.pack(padx=10, anchor="w")

        description_label = tk.Label(self, text="Description")
        description_label.pack(padx=10, pady=(10, 0), anchor="w")
        self.description_entry = tk.Entry(self)
        self.description_entry.pack(padx=10, fill="x")
        self.description_error_label = tk.Label(self, text="", fg="red")
        self.description_error_label.pack(padx=10, anchor="w")

        button_frame = tk.Frame(self)
        button_frame.pack(padx=10, pady=10, fill="x")

        save_button = tk.Button(button_frame, text="Save", command=self.on_save)
        save_button.pack(side="left", padx=5)

        cancel_button = tk.Button(button_frame, text="Cancel", command=self.on_cancel)
        cancel_button.pack(side="left", padx=5)

    def populate_for_edit(self, income):
        self.date_entry.insert(0, income.date)
        self.source_dropdown.set(income.source)
        self.amount_entry.insert(0, str(income.amount))
        self.description_entry.insert(0, income.description)

    def validate_form(self):
        is_valid = True

        date_value = self.date_entry.get()
        if validators.validate_date(date_value) == True:
            self.date_error_label.config(text="")
        else:
            self.date_error_label.config(text="Date must be in YYYY-MM-DD format.")
            is_valid = False

        source_value = self.source_dropdown.get()
        if source_value in INCOME_SOURCES:
            self.source_error_label.config(text="")
        else:
            self.source_error_label.config(text="Please select a valid source.")
            is_valid = False

        amount_value = self.amount_entry.get()
        if validators.validate_amount(amount_value) == True:
            self.amount_error_label.config(text="")
        else:
            self.amount_error_label.config(text="Amount must be a positive number.")
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
        source_value = self.source_dropdown.get()
        amount_value = float(self.amount_entry.get())
        description_value = self.description_entry.get()

        if self.income_id is None:
            income_service.add_income(
                date=date_value,
                source=source_value,
                amount=amount_value,
                description=description_value,
            )
            show_success("Income added.")
        else:
            income_service.edit_income(
                self.income_id,
                date=date_value,
                source=source_value,
                amount=amount_value,
                description=description_value,
            )
            show_success("Income updated.")

        if self.on_success is not None:
            self.on_success()

        self.destroy()

    def on_cancel(self):
        self.destroy()

  
