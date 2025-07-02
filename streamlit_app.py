import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

st.set_page_config(page_title="2025 Expense Tracker", layout="wide")
st.title("📊 2025 Full-Year Expense & Investment Dashboard")

uploaded_file = st.file_uploader("📁 Upload your Excel Expense File (.xlsx with sheets named as months)", type=["xlsx"])

valid_months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

if uploaded_file:
    all_data = []
    xls = pd.ExcelFile(uploaded_file)
    month_sheets = [s for s in xls.sheet_names if s in valid_months]

    if not month_sheets:
        st.error("No valid monthly sheets found (e.g., January, February...).")
        st.stop()

    for sheet_name in month_sheets:
        df_sheet = pd.read_excel(xls, sheet_name=sheet_name)

        # Extract Category (col F, index 5) and Amount (col G, index 6)
        if df_sheet.shape[1] < 7:
            st.warning(f"Sheet '{sheet_name}' does not have enough columns. Skipping.")
            continue

        df_filtered = df_sheet.iloc[:, [5, 6]].copy()
        df_filtered.columns = ["Category", "Amount"]
        df_filtered["Month"] = sheet_name
        all_data.append(df_filtered)

    df = pd.concat(all_data, ignore_index=True)

    # Clean and normalize
    df["Category"] = df["Category"].astype(str).str.strip()
    df["Amount"] = pd.to_numeric(df["Amount"], errors='coerce').fillna(0)
    df["Month"] = pd.Categorical(df["Month"], categories=valid_months, ordered=True)

    # Classify as Investment or Expense
    df["Type"] = df["Category"].apply(
        lambda x: "Investment" if "investment" in x.lower() else "Expense"
    )

    # 📊 Table 1: Month-wise Category Expenses (Including Investment)
    st.subheader("📊 Month-wise Category Expenses (Including Investment)")

    # Pivot table by Month and Category
    month_category_summary = df.pivot_table(
        index="Month", columns="Category", values="Amount", aggfunc="sum"
    ).fillna(0)

    # Rearranging columns as per desired order
    desired_order = [
        "grocery", "travel", "food", "rent", "loan", "shopping",
        "recharge bill payments", "family", "credit card", "health care",
        "insurance", "emergency fund", "gold investment", "stocks investment", "total"
    ]

    # Normalize columns for matching
    normalized_cols = {col.lower().strip(): col for col in month_category_summary.columns}
    present_normalized = list(normalized_cols.keys())

    # Separate known and unknown categories
    known = [normalized_cols[col] for col in desired_order if col in present_normalized]
    others = [normalized_cols[col] for col in present_normalized if col not in desired_order]

    # Insert 'others' just before 'Emergency fund' if it exists
    try:
        ef_index = known.index(normalized_cols.get("emergency fund", ""))
        final_order = known[:ef_index] + others + known[ef_index:]
    except ValueError:
        final_order = known + others

    # Reindex the columns in final order
    month_category_summary = month_category_summary.reindex(columns=final_order)

    # Display Table
    st.dataframe(month_category_summary.style.format("₹{:,.0f}"))

    # 📈 Trend 1: Category-wise Monthly Expenses
    st.subheader("📈 Trend: Monthly Category-wise Breakdown")
    st.line_chart(month_category_summary)


    # 💹 Month-wise Total: Expense vs Investment
    st.subheader("💹 Month-wise Total: Expense vs Investment")

    # Normalize 'Category' and exclude 'total' rows
    df["Category"] = df["Category"].astype(str).str.strip().str.lower()
    df_filtered = df[df["Category"] != "total"]

    # Classify rows as Investment or Expense
    df_filtered["Type"] = df_filtered["Category"].apply(
        lambda x: "Investment" if "investment" in x else "Expense"
    )

    # Pivot table by Month and Type
    month_type_summary = df_filtered.pivot_table(
        index="Month",
        columns="Type",
        values="Amount",
        aggfunc="sum"
    ).fillna(0)

    # Reorder index to match January → December
    month_type_summary.index = pd.CategoricalIndex(
        month_type_summary.index, categories=valid_months, ordered=True
    )
    month_type_summary = month_type_summary.sort_index()

    # Add a 'Total' column = Expense + Investment
    month_type_summary["Total"] = (
        month_type_summary.get("Expense", 0) + month_type_summary.get("Investment", 0)
    )

    # Show DataFrame
    st.dataframe(month_type_summary.style.format("₹{:,.0f}"))

    # 📉 Trend: Expense vs Investment
    st.subheader("📉 Trend: Expense vs Investment")
    st.line_chart(month_type_summary[["Expense", "Investment"]])

    # 📊 Bar Chart by Category (Full Year)
    st.subheader("📂 Expense Breakdown by Category (Full Year)")

    # Grouping and sorting
    expense_by_cat = df.groupby("Category")["Amount"].sum().sort_values()

    # Remove any category labeled 'Total' (case insensitive)
    expense_by_cat = expense_by_cat[expense_by_cat.index.str.lower() != "total"]

    # Plot bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(expense_by_cat.index, expense_by_cat.values, color='steelblue')

    # Add value labels to the right of each bar
    for bar in bars:
        width = bar.get_width()
        ax.text(width + 1000, bar.get_y() + bar.get_height()/2,
                f"₹{width:,.0f}", va='center', fontsize=9)

    ax.set_xlabel("Total Amount (₹)")
    ax.set_title("Expenses by Category (Full Year)")
    plt.tight_layout()

    st.pyplot(fig)

else:
    st.info("Upload an Excel file with sheets named after months (e.g., January, February...)")
