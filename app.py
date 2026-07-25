import tkinter as tk
from tkinter import Menu
from tkinter import messagebox

from gui.dashboard import DashboardFrame
from gui.settings import SettingsFrame
from gui.analytics import AnalyticsFrame
from gui.reports import ReportsFrame


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


        manage_menu = Menu(menu_bar, tearoff=0)
        manage_menu.add_command(label="Categories", command=self.on_manage_categories)
        manage_menu.add_command(label="Budgets", command=self.on_manage_budgets)
        menu_bar.add_cascade(label="Manage", menu=manage_menu)

        view_menu = Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Dashboard", command=self.on_view_dashboard)
        view_menu.add_command(label="Analytics", command=self.on_view_analytics)
        view_menu.add_command(label="Reports", command=self.on_view_reports)
        menu_bar.add_cascade(label="View", menu=view_menu)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.on_about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menu_bar)

    def build_frames(self):
        dashboard_frame = DashboardFrame(self.container, self)
        dashboard_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.frames["Dashboard"] = dashboard_frame

        settings_frame = SettingsFrame(self.container, self)
        settings_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.frames["Settings"] = settings_frame

        analytics_frame = AnalyticsFrame(self.container, self)
        analytics_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.frames["Analytics"] = analytics_frame

        reports_frame = ReportsFrame(self.container, self)
        reports_frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.frames["Reports"] = reports_frame

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

        if name == "Analytics":
            self.frames["Analytics"].load_stats()

        if name == "Dashboard":
            self.frames["Dashboard"].category_filter.refresh_categories()
            self.frames["Dashboard"].refresh_summary()
            self.frames["Dashboard"].refresh_transaction_table()

    def on_manage_categories(self):
        self.show_frame("Settings")

    def on_manage_budgets(self):
        self.show_frame("Settings")

    def on_view_dashboard(self):
        self.show_frame("Dashboard")

    def on_view_analytics(self):
        self.show_frame("Analytics")

    def on_view_reports(self):
        self.show_frame("Reports")

    def on_about(self):
        messagebox.showinfo("About", "Personal Expense Tracker\nBuilt with Python, Tkinter, and NumPy.")


if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()
