import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import csv
import datetime
from utils import validators
from services import expense_service
from gui.widgets import CategoryDropdown
from utils.helpers import format_currency

REPORT_TYPES = ["Daily", "Weekly", "Monthly", "Yearly", "Category"]
MONTH_NUMBERS = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]


def build_year_options():
    today = datetime.date.today()
    current_year = today.year

    years = []
    start_year = current_year - 5
    end_year = current_year + 1

    year = start_year
    while year <= end_year:
        years.append(str(year))
        year = year + 1

    return years


class ReportsFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.current_report_rows = []

        self.build_back_button()
        self.build_type_selector()
        self.build_input_area()
        self.build_table()
        self.build_totals_label()
        self.build_action_buttons()

        self.on_type_changed(None)

    def build_back_button(self):
        back_button = tk.Button(self, text="Back to Dashboard", command=self.on_back_to_dashboard)
        back_button.pack(padx=10, pady=10, anchor="w")

    def on_back_to_dashboard(self):
        self.app.show_frame("Dashboard")

    def build_type_selector(self):
        selector_frame = tk.Frame(self)
        selector_frame.pack(padx=10, pady=(0, 10), fill="x")

        type_label = tk.Label(selector_frame, text="Report Type:")
        type_label.pack(side="left")

        self.report_type_dropdown = ttk.Combobox(selector_frame, values=REPORT_TYPES, state="readonly")
        self.report_type_dropdown.set(REPORT_TYPES[0])
        self.report_type_dropdown.pack(side="left", padx=5)
        self.report_type_dropdown.bind("<<ComboboxSelected>>", self.on_type_changed)

    def build_input_area(self):
        self.input_area = tk.Frame(self)
        self.input_area.pack(padx=10, pady=(0, 10), fill="x")

    def build_table(self):
        columns = ("date", "category", "amount", "payment", "description")

        self.report_table = ttk.Treeview(self, columns=columns, show="headings", height=12)
        self.report_table.heading("date", text="Date")
        self.report_table.heading("category", text="Category")
        self.report_table.heading("amount", text="Amount")
        self.report_table.heading("payment", text="Payment")
        self.report_table.heading("description", text="Description")

        self.report_table.pack(padx=10, pady=(0, 5), fill="both", expand=True)

    def build_totals_label(self):
        self.totals_label = tk.Label(self, text="Total: $0.00", font=("Arial", 11, "bold"))
        self.totals_label.pack(padx=10, pady=(0, 10), anchor="w")

    def build_action_buttons(self):
        button_frame = tk.Frame(self)
        button_frame.pack(padx=10, pady=(0, 10), fill="x")

        generate_button = tk.Button(button_frame, text="Generate", command=self.on_generate)
        generate_button.pack(side="left", padx=5)

        export_button = tk.Button(button_frame, text="Export to CSV", command=self.export_report)
        export_button.pack(side="left", padx=5)

    def on_type_changed(self, event):
        existing_widgets = self.input_area.winfo_children()
        for widget in existing_widgets:
            widget.destroy()

        report_type = self.report_type_dropdown.get()

        if report_type == "Daily":
            self.build_daily_inputs()
        elif report_type == "Weekly":
            self.build_weekly_inputs()
        elif report_type == "Monthly":
            self.build_monthly_inputs()
        elif report_type == "Yearly":
            self.build_yearly_inputs()
        elif report_type == "Category":
            self.build_category_inputs()

    def build_daily_inputs(self):
        date_label = tk.Label(self.input_area, text="Date (YYYY-MM-DD):")
        date_label.pack(side="left")

        self.daily_date_entry = tk.Entry(self.input_area)
        self.daily_date_entry.pack(side="left", padx=5)

    def build_weekly_inputs(self):
        date_label = tk.Label(self.input_area, text="Any date in the week (YYYY-MM-DD):")
        date_label.pack(side="left")

        self.weekly_date_entry = tk.Entry(self.input_area)
        self.weekly_date_entry.pack(side="left", padx=5)

    def build_monthly_inputs(self):
        month_label = tk.Label(self.input_area, text="Month:")
        month_label.pack(side="left")

        self.monthly_month_dropdown = ttk.Combobox(self.input_area, values=MONTH_NUMBERS, state="readonly", width=5)
        self.monthly_month_dropdown.pack(side="left", padx=5)

        year_label = tk.Label(self.input_area, text="Year:")
        year_label.pack(side="left")

        self.monthly_year_dropdown = ttk.Combobox(self.input_area, values=build_year_options(), state="readonly", width=8)
        self.monthly_year_dropdown.pack(side="left", padx=5)

    def build_yearly_inputs(self):
        year_label = tk.Label(self.input_area, text="Year:")
        year_label.pack(side="left")

        self.yearly_year_dropdown = ttk.Combobox(self.input_area, values=build_year_options(), state="readonly", width=8)
        self.yearly_year_dropdown.pack(side="left", padx=5)

    def build_category_inputs(self):
        category_label = tk.Label(self.input_area, text="Category:")
        category_label.pack(side="left")

        self.category_report_dropdown = CategoryDropdown(self.input_area)
        self.category_report_dropdown.pack(side="left", padx=5)
    def build_daily_report(self, date_str):
        all_expenses = expense_service.get_all_expenses()

        matching = []
        for expense in all_expenses:
            if expense.date == date_str:
                matching.append(expense)

        return matching

    def build_weekly_report(self, date_str):
        date_parts = date_str.split("-")
        year = int(date_parts[0])
        month = int(date_parts[1])
        day = int(date_parts[2])
        target_date = datetime.date(year, month, day)

        weekday_number = target_date.weekday()
        week_start = target_date - datetime.timedelta(days=weekday_number)
        week_end = week_start + datetime.timedelta(days=6)

        all_expenses = expense_service.get_all_expenses()

        matching = []
        for expense in all_expenses:
            expense_date_parts = expense.date.split("-")
            expense_year = int(expense_date_parts[0])
            expense_month = int(expense_date_parts[1])
            expense_day = int(expense_date_parts[2])
            expense_date = datetime.date(expense_year, expense_month, expense_day)

            if expense_date >= week_start and expense_date <= week_end:
                matching.append(expense)

        return matching

    def build_monthly_report(self, year_str, month_str):
        target_year_month = year_str + "-" + month_str

        all_expenses = expense_service.get_all_expenses()

        matching = []
        for expense in all_expenses:
            expense_year_month = expense.date[0:7]
            if expense_year_month == target_year_month:
                matching.append(expense)

        return matching

    def build_yearly_report(self, year_str):
        all_expenses = expense_service.get_all_expenses()

        matching = []
        for expense in all_expenses:
            expense_year = expense.date[0:4]
            if expense_year == year_str:
                matching.append(expense)

        return matching

    def build_category_report(self, category_name):
        all_expenses = expense_service.get_all_expenses()

        matching = []
        for expense in all_expenses:
            if expense.category == category_name:
                matching.append(expense)

        return matching

    def fill_table(self, expenses):
        existing_rows = self.report_table.get_children()
        for row_id in existing_rows:
            self.report_table.delete(row_id)

        for expense in expenses:
            row_values = (expense.date, expense.category, format_currency(expense.amount), expense.payment_method, expense.description)
            self.report_table.insert("", "end", values=row_values)

    def update_totals(self, expenses):
        total = 0.0
        for expense in expenses:
            total = total + expense.amount

        totals_text = "Total: " + format_currency(total) + "  (" + str(len(expenses)) + " transactions)"
        self.totals_label.config(text=totals_text)

    def on_generate(self):
        report_type = self.report_type_dropdown.get()
        matching = []

        if report_type == "Daily":
            date_value = self.daily_date_entry.get()
            if validators.validate_date(date_value) == False:
                messagebox.showerror("Error", "Please enter a valid date in YYYY-MM-DD format.")
                return
            matching = self.build_daily_report(date_value)

        elif report_type == "Weekly":
            date_value = self.weekly_date_entry.get()
            if validators.validate_date(date_value) == False:
                messagebox.showerror("Error", "Please enter a valid date in YYYY-MM-DD format.")
                return
            matching = self.build_weekly_report(date_value)

        elif report_type == "Monthly":
            month_value = self.monthly_month_dropdown.get()
            year_value = self.monthly_year_dropdown.get()
            if month_value == "" or year_value == "":
                messagebox.showerror("Error", "Please select both a month and a year.")
                return
            matching = self.build_monthly_report(year_value, month_value)

        elif report_type == "Yearly":
            year_value = self.yearly_year_dropdown.get()
            if year_value == "":
                messagebox.showerror("Error", "Please select a year.")
                return
            matching = self.build_yearly_report(year_value)

        elif report_type == "Category":
            category_value = self.category_report_dropdown.get()
            if category_value == "":
                messagebox.showerror("Error", "Please select a category.")
                return
            matching = self.build_category_report(category_value)

        self.current_report_rows = matching
        self.fill_table(matching)
        self.update_totals(matching)

    def export_report(self):
        if len(self.current_report_rows) == 0:
            messagebox.showerror("Error", "Generate a report first before exporting.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Export Report As",
        )

        if file_path == "":
            return

        report_fields = ["date", "category", "amount", "payment_method", "description"]

        file = open(file_path, "w", newline="", encoding="utf-8")
        writer = csv.DictWriter(file, fieldnames=report_fields)
        writer.writeheader()

        for expense in self.current_report_rows:
            row = {
                "date": expense.date,
                "category": expense.category,
                "amount": expense.amount,
                "payment_method": expense.payment_method,
                "description": expense.description,
            }
            writer.writerow(row)

        file.close()

        messagebox.showinfo("Success", "Report exported.")
 

