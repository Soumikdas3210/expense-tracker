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

   
