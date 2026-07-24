# expense-tracker
Offline personal expense tracker — Tkinter + NumPy, Desktop Application
# Personal Expense Tracker

A desktop application for tracking personal income and expenses, built with Python and Tkinter. Runs fully offline — all data is stored locally in CSV files.

## Features

- Add, edit, and delete expenses and income
- Live search and category filtering on the dashboard
- Category and monthly budget management, with over-budget warnings
- Analytics: total, average, median, highest/lowest, standard deviation, and variance, plus pie/bar/line charts (powered by NumPy and Matplotlib)
- Reports: Daily, Weekly, Monthly, Yearly, and Category views, exportable to CSV
- Import/export expense data as CSV

## Tech Stack

- Python 3
- Tkinter (GUI)
- NumPy (statistics)
- Matplotlib (charts)
- CSV files (storage — no database required)

## Setup

**Requirements:** Python 3.10+ installed on Windows.

```powershell
git clone <your-repo-url>
cd expense-tracker

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

python main.py
```

The app seeds `data/` with default categories and empty CSV files on first run.

## Project Structure
 
