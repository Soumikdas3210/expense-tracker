import tkinter as tk
from tkinter import ttk



from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



from services import expense_service
from services import analytics
from utils.helpers import format_currency





class AnalyticsFrame(tk.Frame):
   def __init__(self, parent, app):
       super().__init__(parent)
       self.app = app



       self.build_back_button()
       self.build_stats_panel()
       self.build_charts_panel()
       self.build_category_table()



       self.load_stats()



   def build_back_button(self):
       back_button = tk.Button(self, text="Back to Dashboard", command=self.on_back_to_dashboard)
       back_button.pack(padx=10, pady=10, anchor="w")



   def on_back_to_dashboard(self):
       self.app.show_frame("Dashboard")



   def build_stats_panel(self):
       self.stats_frame = tk.Frame(self)
       self.stats_frame.pack(padx=10, pady=(0, 10), fill="x")



       self.total_label = tk.Label(self.stats_frame, text="Total: ...", anchor="w")
       self.total_label.pack(fill="x")



       self.average_label = tk.Label(self.stats_frame, text="Average: ...", anchor="w")
       self.average_label.pack(fill="x")



       self.median_label = tk.Label(self.stats_frame, text="Median: ...", anchor="w")
       self.median_label.pack(fill="x")



       self.highest_label = tk.Label(self.stats_frame, text="Highest: ...", anchor="w")
       self.highest_label.pack(fill="x")



       self.lowest_label = tk.Label(self.stats_frame, text="Lowest: ...", anchor="w")
       self.lowest_label.pack(fill="x")



       self.std_dev_label = tk.Label(self.stats_frame, text="Std Dev: ...", anchor="w")
       self.std_dev_label.pack(fill="x")



       self.variance_label = tk.Label(self.stats_frame, text="Variance: ...", anchor="w")
       self.variance_label.pack(fill="x")



   def build_charts_panel(self):
       self.notebook = ttk.Notebook(self)
       self.notebook.pack(padx=10, pady=(0, 10), fill="both", expand=True)



       pie_tab = tk.Frame(self.notebook)
       self.notebook.add(pie_tab, text="Pie Chart")
       self.pie_figure = Figure(figsize=(5, 4))
       self.pie_axes = self.pie_figure.add_subplot(111)
       self.pie_canvas = FigureCanvasTkAgg(self.pie_figure, master=pie_tab)
       self.pie_canvas.get_tk_widget().pack(fill="both", expand=True)



       bar_tab = tk.Frame(self.notebook)
       self.notebook.add(bar_tab, text="Bar Chart")
       self.bar_figure = Figure(figsize=(5, 4))
       self.bar_axes = self.bar_figure.add_subplot(111)
       self.bar_canvas = FigureCanvasTkAgg(self.bar_figure, master=bar_tab)
       self.bar_canvas.get_tk_widget().pack(fill="both", expand=True)



       line_tab = tk.Frame(self.notebook)
       self.notebook.add(line_tab, text="Line Chart")
       self.line_figure = Figure(figsize=(5, 4))
       self.line_axes = self.line_figure.add_subplot(111)
       self.line_canvas = FigureCanvasTkAgg(self.line_figure, master=line_tab)
       self.line_canvas.get_tk_widget().pack(fill="both", expand=True)



   def build_category_table(self):
       columns = ("category", "percent", "count")



       self.category_table = ttk.Treeview(self, columns=columns, show="headings", height=6)
       self.category_table.heading("category", text="Category")
       self.category_table.heading("percent", text="% of Total")
       self.category_table.heading("count", text="Count")



       self.category_table.pack(padx=10, pady=(0, 10), fill="both")



   def load_stats(self):
       expenses = expense_service.get_all_expenses()



       total = analytics.total_expense(expenses)
       average = analytics.average_expense(expenses)
       median = analytics.median_expense(expenses)
       std_dev = analytics.std_dev_expense(expenses)
       variance = analytics.variance_expense(expenses)
       highest = analytics.highest_expense(expenses)
       lowest = analytics.lowest_expense(expenses)



       self.total_label.config(text="Total: " + format_currency(total))
       self.average_label.config(text="Average: " + format_currency(average))
       self.median_label.config(text="Median: " + format_currency(median))
       self.std_dev_label.config(text="Std Dev: " + format_currency(std_dev))
       self.variance_label.config(text="Variance: " + format_currency(variance))



       if highest is None:
           self.highest_label.config(text="Highest: N/A")
       else:
           highest_text = "Highest: " + format_currency(highest["amount"]) + " (" + highest["category"] + ")"
           self.highest_label.config(text=highest_text)



       if lowest is None:
           self.lowest_label.config(text="Lowest: N/A")
       else:
           lowest_text = "Lowest: " + format_currency(lowest["amount"]) + " (" + lowest["category"] + ")"
           self.lowest_label.config(text=lowest_text)



       self.draw_pie_chart(expenses)
       self.draw_bar_chart(expenses)
       self.draw_line_chart(expenses)
       self.load_category_table(expenses)



   def draw_pie_chart(self, expenses):
       self.pie_axes.clear()



       percentages = analytics.category_percentage(expenses)



       if len(percentages) == 0:
           self.pie_axes.text(0.5, 0.5, "No expense data yet", ha="center")
       else:
           labels = []
           values = []
           for category in percentages:
               labels.append(category)
               values.append(percentages[category])



           self.pie_axes.pie(values, labels=labels, autopct="%1.1f%%")



       self.pie_axes.set_title("Spending by Category")
       self.pie_canvas.draw()



   def draw_bar_chart(self, expenses):
       self.bar_axes.clear()



       month_totals = analytics.spending_trend(expenses, "monthly")



       sorted_months = []
       for month_key in month_totals:
           sorted_months.append(month_key)
       sorted_months.sort()



       totals = []
       for month_key in sorted_months:
           totals.append(month_totals[month_key])



       if len(sorted_months) == 0:
           self.bar_axes.text(0.5, 0.5, "No expense data yet", ha="center")
       else:
           self.bar_axes.bar(sorted_months, totals)
           self.bar_axes.tick_params(axis="x", rotation=45)



       self.bar_axes.set_title("Monthly Spending Comparison")
       self.bar_figure.tight_layout()
       self.bar_canvas.draw()



   def draw_line_chart(self, expenses):
       self.line_axes.clear()



       month_totals = analytics.spending_trend(expenses, "monthly")



       sorted_months = []
       for month_key in month_totals:
           sorted_months.append(month_key)
       sorted_months.sort()



       totals = []
       for month_key in sorted_months:
           totals.append(month_totals[month_key])



       if len(sorted_months) == 0:
           self.line_axes.text(0.5, 0.5, "No expense data yet", ha="center")
       else:
           self.line_axes.plot(sorted_months, totals, marker="o")
           self.line_axes.tick_params(axis="x", rotation=45)



       self.line_axes.set_title("Spending Trend")
       self.line_figure.tight_layout()
       self.line_canvas.draw()



   def load_category_table(self, expenses):
       existing_rows = self.category_table.get_children()
       for row_id in existing_rows:
           self.category_table.delete(row_id)



       percentages = analytics.category_percentage(expenses)
       frequency = analytics.expense_frequency(expenses)



       for category in percentages:
           percent_value = percentages[category]



           count_value = 0
           if category in frequency:
               count_value = frequency[category]



           percent_text = "{:.1f}%".format(percent_value)
           row_values = (category, percent_text, count_value)
           self.category_table.insert("", "end", values=row_values)
