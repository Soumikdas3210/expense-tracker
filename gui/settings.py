import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import csv

from services import storage
from services import budget_service


class SettingsFrame(tk.Frame):
  def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        self.build_categories_section()
        self.build_budgets_section()

        self.refresh_categories_list()
        self.refresh_budgets_section()

    def build_back_button(self):
        back_button = tk.Button(self, text="Back to Dashboard", command=self.on_back_to_dashboard)
        back_button.pack(padx=10, pady=10, anchor="w")

    def on_back_to_dashboard(self):
        self.app.show_frame("Dashboard")

    def build_categories_section(self):
        section_label = tk.Label(self, text="Categories", font=("Arial", 12, "bold"))
        section_label.pack(padx=10, pady=(10, 5), anchor="w")

        content_frame = tk.Frame(self)
        content_frame.pack(padx=10, pady=(0, 10), fill="x")

        self.categories_listbox = tk.Listbox(content_frame, height=8)
        self.categories_listbox.pack(side="left", fill="both", expand=True)

        controls_frame = tk.Frame(content_frame)
        controls_frame.pack(side="left", padx=10, fill="y")

        self.new_category_entry = tk.Entry(controls_frame)
        self.new_category_entry.pack(pady=(0, 5), fill="x")

        add_button = tk.Button(controls_frame, text="Add Category", command=self.on_add_category)
        add_button.pack(pady=2, fill="x")

        delete_button = tk.Button(controls_frame, text="Delete Selected", command=self.on_delete_category)
        delete_button.pack(pady=2, fill="x")

    def refresh_categories_list(self):
        self.categories_listbox.delete(0, "end")

        categories = storage.load_categories()
        self.category_rows = categories

        for category in categories:
            display_text = category["name"]
            if category["is_default"] == True:
                display_text = display_text + " (default)"
            self.categories_listbox.insert("end", display_text)

    def get_selected_category(self):
        selection = self.categories_listbox.curselection()

        if len(selection) == 0:
            return None

        selected_index = selection[0]
        return self.category_rows[selected_index]

    def on_add_category(self):
        new_name = self.new_category_entry.get()

        if new_name == "":
            messagebox.showerror("Error", "Category name cannot be empty.")
            return

        categories = storage.load_categories()

        for category in categories:
            if category["name"] == new_name:
                messagebox.showerror("Error", "That category already exists.")
                return

        new_id = storage.generate_next_id(categories)
        new_category = {"id": new_id, "name": new_name, "is_default": False}
        categories.append(new_category)
        storage.save_categories(categories)

        self.new_category_entry.delete(0, "end")
        self.refresh_categories_list()
        self.refresh_budgets_section()
        messagebox.showinfo("Success", "Category added.")

    def on_delete_category(self):
        selected_category = self.get_selected_category()

        if selected_category is None:
            messagebox.showinfo("No Selection", "Select a category first.")
            return

        if selected_category["is_default"] == True:
            messagebox.showerror("Error", "Default categories cannot be deleted.")
            return

        confirm_message = "Delete category '" + selected_category["name"] + "'?"
        confirmed = messagebox.askyesno("Confirm Delete", confirm_message)

        if confirmed == False:
            return

        categories = storage.load_categories()

        remaining_categories = []
        for category in categories:
            if category["id"] != selected_category["id"]:
                remaining_categories.append(category)

        storage.save_categories(remaining_categories)
        self.refresh_categories_list()
        self.refresh_budgets_section()
        messagebox.showinfo("Success", "Category deleted.")

    def build_budgets_section(self):
        section_label = tk.Label(self, text="Budgets", font=("Arial", 12, "bold"))
        section_label.pack(padx=10, pady=(10, 5), anchor="w")

        self.budgets_container = tk.Frame(self)
        self.budgets_container.pack(padx=10, pady=(0, 5), fill="x")

        save_budgets_button = tk.Button(self, text="Save Budgets", command=self.on_save_budgets)
        save_budgets_button.pack(padx=10, pady=(0, 10), anchor="w")

    def refresh_budgets_section(self):
        existing_widgets = self.budgets_container.winfo_children()
        for widget in existing_widgets:
            widget.destroy()

        categories = storage.load_categories()
        all_budgets = storage.load_budgets()

        budget_lookup = {}
        for budget_row in all_budgets:
            budget_lookup[budget_row["category"]] = budget_row["monthly_limit"]

        self.budget_entries = {}

        for category in categories:
            category_name = category["name"]

            row_frame = tk.Frame(self.budgets_container)
            row_frame.pack(fill="x", pady=2)

            name_label = tk.Label(row_frame, text=category_name, width=20, anchor="w")
            name_label.pack(side="left")

            entry = tk.Entry(row_frame, width=15)
            entry.pack(side="left")

            if category_name in budget_lookup:
                current_value = budget_lookup[category_name]
                entry.insert(0, str(current_value))

            self.budget_entries[category_name] = entry

    def on_save_budgets(self):
        for category_name in self.budget_entries:
            entry = self.budget_entries[category_name]
            value_text = entry.get()

            if value_text == "":
                continue

            try:
                value_number = float(value_text)
            except ValueError:
                error_message = "Budget for '" + category_name + "' must be a number."
                messagebox.showerror("Error", error_message)
                return

            if value_number <= 0:
                error_message = "Budget for '" + category_name + "' must be greater than 0."
                messagebox.showerror("Error", error_message)
                return

            budget_service.set_budget(category_name, value_number)

        messagebox.showinfo("Success", "Budgets saved.")

    def build_data_section(self):
        section_label = tk.Label(self, text="Data", font=("Arial", 12, "bold"))
        section_label.pack(padx=10, pady=(10, 5), anchor="w")

        button_frame = tk.Frame(self)
        button_frame.pack(padx=10, pady=(0, 10), fill="x")

        import_button = tk.Button(button_frame, text="Import CSV", command=self.on_import_csv)
        import_button.pack(side="left", padx=5)

        export_button = tk.Button(button_frame, text="Export CSV", command=self.on_export_csv)
        export_button.pack(side="left", padx=5)

    def on_export_csv(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Export Expenses As",
        )

        if file_path == "":
            return

        expenses = storage.load_expenses()

        file = open(file_path, "w", newline="", encoding="utf-8")
        writer = csv.DictWriter(file, fieldnames=storage.EXPENSE_FIELDS)
        writer.writeheader()
        writer.writerows(expenses)
        file.close()

        messagebox.showinfo("Success", "Expenses exported.")

    def on_import_csv(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")],
            title="Import Expenses From",
        )

        if file_path == "":
            return

        file = open(file_path, "r", newline="", encoding="utf-8")
        reader = csv.DictReader(file)
        imported_rows = list(reader)
        file.close()

        if reader.fieldnames is None:
            messagebox.showerror("Error", "The selected file has no header row.")
            return

        missing_columns = []
        for required_column in storage.EXPENSE_FIELDS:
            if required_column not in reader.fieldnames:
                missing_columns.append(required_column)

        if len(missing_columns) > 0:
            missing_text = ", ".join(missing_columns)
            error_message = "The CSV is missing required columns: " + missing_text
            messagebox.showerror("Error", error_message)
            return

        existing_expenses = storage.load_expenses()
        combined_expenses = existing_expenses + imported_rows

        storage.save_expenses(combined_expenses)

        success_message = "Imported " + str(len(imported_rows)) + " expenses."
        messagebox.showinfo("Success", success_message)
