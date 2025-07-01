# 📊 2025 Expense & Investment Tracker

A Streamlit-based web dashboard to track and visualize monthly **expenses** and **investments** from an Excel file. Easily analyze your spending patterns across different categories and monitor your investments throughout the year.

---

## 🔧 Features

- Upload Excel files with sheets for each month (`January`, `February`, ..., `December`)
- Extracts data from columns F (Category) and G (Amount)
- Automatically categorizes entries as **Expense** or **Investment**
- Month-wise summary tables:
  - Category-level breakdown (including investment)
  - Expense vs. Investment
- Visualizations:
  - Line chart for category-wise trends
  - Line chart for Expense vs Investment (color-coded: red for expense, green for investment)
  - Horizontal bar chart for full-year category totals
- Smart column ordering (common categories like Rent, Food, etc. shown first)
- Downloadable Excel summary report

---

## 📁 Excel File Format

Each sheet in the uploaded Excel file must correspond to a **month** (e.g., `January`, `February`, ...).

- The app expects:
  - **Column F** = `Category`
  - **Column G** = `Amount`

Ensure there are at least 7 columns per sheet so that columns F and G can be extracted.

---

## 📦 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/expense-tracker-2025.git
   cd expense-tracker-2025


## Create a virtual environment:
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`

## Install dependencies:
pip install -r requirements.txt


## Running the App
streamlit run app.py
