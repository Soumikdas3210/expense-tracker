import tkinter as tk
from tkinter import Menu
from tkinter import messagebox


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

    def build_frames(self):
        placeholder = tk.Frame(self.container)
        placeholder_label = tk.Label(placeholder, text="Dashboard - built in Task 4", font=("Arial", 14))
        placeholder_label.pack(pady=50)
        placeholder.place(x=0, y=0, relwidth=1, relheight=1)

        self.frames["Dashboard"] = placeholder

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def on_import_csv(self):
        messagebox.showinfo("Coming Soon", "Import CSV is not built yet.")

    def on_export_csv(self):
        messagebox.showinfo("Coming Soon", "Export CSV is not built yet.")

    def on_manage_categories(self):
        messagebox.showinfo("Coming Soon", "Categories screen is coming in Milestone 5.")

    def on_manage_budgets(self):
        messagebox.showinfo("Coming Soon", "Budgets screen is coming in Milestone 5.")

    def on_view_dashboard(self):
        self.show_frame("Dashboard")

    def on_view_analytics(self):
        messagebox.showinfo("Coming Soon", "Analytics screen is coming in Milestone 6.")

    def on_view_reports(self):
        messagebox.showinfo("Coming Soon", "Reports screen is coming in Milestone 7.")

    def on_about(self):
        messagebox.showinfo("About", "Personal Expense Tracker\nBuilt with Python, Tkinter, and NumPy.")                 

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()       