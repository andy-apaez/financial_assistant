import streamlit as st
import pandas as pd
import plotly.express as px
import requests

API_URL = "http://127.0.0.1:8000"  # backend FastAPI server

st.set_page_config(page_title="AI Finance Dashboard", layout="wide")
st.title("💰 AI-Powered Personal Finance Dashboard")

# Fetch transactions from backend


def fetch_transactions():
    try:
        res = requests.get(f"{API_URL}/transactions/all")
        if res.status_code == 200:
            data = res.json()["transactions"]
            return pd.DataFrame(data)
    except Exception as e:
        st.error(f"Error connecting to API: {e}")
    return pd.DataFrame()


transactions = fetch_transactions()

if transactions.empty:
    st.warning("No transactions available. Upload a CSV via backend API.")
else:
    # Show table
    st.subheader("📋 Transactions")
    st.dataframe(transactions)

    # Spending by category
    if "category" in transactions.columns:
        st.subheader("📊 Spending by Category")
        cat_chart = transactions.groupby(
            "category")["amount"].sum().reset_index()
        fig = px.pie(cat_chart, names="category",
                     values="amount", title="Spending Breakdown")
        st.plotly_chart(fig, use_container_width=True)

    # Spending over time
    if "date" in transactions.columns:
        st.subheader("📈 Spending Over Time")
        time_chart = transactions.groupby("date")["amount"].sum().reset_index()
        fig2 = px.line(time_chart, x="date", y="amount",
                       title="Expenses Over Time")
        st.plotly_chart(fig2, use_container_width=True)
