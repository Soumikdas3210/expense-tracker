import tkinter as tk
from tkinter import Menu


class ExpenseTrackerApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Personal Expense Tracker")
        self.geometry("1000x650")

        self.frames = {}

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.build_menu_bar()
        self.build_frames()
        self.show_frame("Dashboard")

    def build_menu_bar(self):
        menu_bar = Menu(self)

        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Import CSV", command=self.on_import_csv)
        file_menu.add_command(label="Export CSV", command=self.on_export_csv)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        manage_menu = Menu(menu_bar, tearoff=0)
        manage_menu.add_command(label="Categories", command=self.on_manage_categories)
        manage_menu.add_command(label="Budgets", command=self.on_manage_budgets)
        menu_bar.add_cascade(label="Manage", menu=manage_menu)

        view_menu = Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Dashboard", command=self.on_view_dashboard)
        view_menu.add_command(label="Analytics", command=self.on_view_analytics)
        view_menu.add_command(label="Reports", command=self.on_view_reports)
        menu_bar.add_cascade(label="View", menu=view_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.on_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menu_bar)             

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()       