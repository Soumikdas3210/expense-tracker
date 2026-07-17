import tkinter as tk

class ExpenseTrackerApp(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Personal Expense Tracker")
        self.geometry("1000x650")

if __name__ == "__main__":
    app = ExpenseTrackerApp()
    app.mainloop()       