import os
import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# Configuration
# -------------------------
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

st.set_page_config(page_title="AI Finance Dashboard", layout="wide")
st.title("Andy's AI-Powered Personal Finance Dashboard")

# -------------------------
# CSV Upload
# -------------------------
st.subheader("Upload Transactions CSV")
uploaded_files = st.file_uploader(
    "Drag and drop CSV files here (multiple allowed)",
    type=["csv"],
    accept_multiple_files=True
)

for uploaded_file in uploaded_files:
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"File uploaded: {uploaded_file.name}")

# -------------------------
# Load and Combine CSVs
# -------------------------
all_files = [os.path.join(UPLOAD_DIR, f)
             for f in os.listdir(UPLOAD_DIR) if f.endswith(".csv")]

if not all_files:
    st.warning("No transactions available. Upload a CSV to begin.")
    st.stop()

try:
    combined_df = pd.concat([pd.read_csv(f)
                            for f in all_files], ignore_index=True)
except Exception as e:
    st.error(f"Error reading CSVs: {e}")
    st.stop()

# -------------------------
# Sanitize Columns & Categories
# -------------------------
combined_df.columns = combined_df.columns.str.strip().str.lower()
required_columns = ["date", "description", "amount", "category"]
for col in required_columns:
    if col not in combined_df.columns:
        st.error(f"The uploaded CSV is missing the '{col}' column.")
        st.stop()

# Ensure 'date' is datetime
combined_df["date"] = pd.to_datetime(combined_df["date"], errors="coerce")

# Clean categories: remove empty, NaN, 'all', 'uncategorized'
combined_df["category"] = combined_df["category"].fillna("").str.strip()
exclude_categories = ["all", "uncategorized", ""]
combined_df = combined_df[~combined_df["category"].str.lower().isin(
    exclude_categories)]

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.subheader("Filters")

# Date range filter
min_date = combined_df["date"].min()
max_date = combined_df["date"].max()
start_date, end_date = st.sidebar.date_input(
    "Date range", [min_date, max_date])
combined_df = combined_df[(combined_df["date"] >= pd.to_datetime(start_date)) &
                          (combined_df["date"] <= pd.to_datetime(end_date))]

# Category filter
categories = combined_df["category"].unique().tolist()
selected_categories = st.sidebar.multiselect(
    "Categories", categories, default=categories)
combined_df = combined_df[combined_df["category"].isin(selected_categories)]

# -------------------------
# Summary Statistics
# -------------------------
st.subheader("📊 Summary Statistics")

total_income = combined_df[combined_df["amount"] > 0]["amount"].sum()
total_expense = combined_df[combined_df["amount"] < 0]["amount"].sum()
net_total = total_income + total_expense

col1, col2, col3 = st.columns(3)
col1.metric("Total Income", f"${total_income:,.2f}")
col2.metric("Total Expenses", f"${-total_expense:,.2f}")
col3.metric("Net Total", f"${net_total:,.2f}")

# -------------------------
# Transactions Table
# -------------------------
st.subheader("📋 Transactions")
st.dataframe(combined_df)

# -------------------------
# Charts
# -------------------------
# Spending by Category (expenses only)
st.subheader("📊 Spending by Category")
expenses_df = combined_df[combined_df["amount"] < 0]

if not expenses_df.empty:
    cat_chart = expenses_df.groupby(
        "category")["amount"].sum().abs().reset_index()
    fig1 = px.pie(cat_chart, names="category",
                  values="amount", title="Spending Breakdown")
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.info("No expense transactions to display in category chart.")

# Spending Over Time (separate lines for income and expenses)
st.subheader("📉 Spending Over Time")

income_df = combined_df[combined_df["amount"] > 0].groupby(
    "date")["amount"].sum().reset_index()
expense_df = combined_df[combined_df["amount"] < 0].groupby(
    "date")["amount"].sum().abs().reset_index()

fig2 = px.line()
if not income_df.empty:
    fig2.add_scatter(
        x=income_df["date"], y=income_df["amount"], mode="lines+markers", name="Income")
if not expense_df.empty:
    fig2.add_scatter(
        x=expense_df["date"], y=expense_df["amount"], mode="lines+markers", name="Expenses")
st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# Download Combined CSV
# -------------------------
st.subheader("💾 Download Combined Transactions")
csv_data = combined_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download CSV",
    data=csv_data,
    file_name="combined_transactions.csv",
    mime="text/csv"
)
