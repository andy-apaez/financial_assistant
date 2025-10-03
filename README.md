🏦 AI-Powered Finance Assistant
---

A personal finance dashboard built with FastAPI (backend) and Streamlit (frontend), allowing users to upload, track, and visualize their transactions. The dashboard supports drag-and-drop CSV uploads, category filtering, summary statistics, and interactive charts.

---
DEMO
---

![ezgif com-video-to-gif-converter (7)](https://github.com/user-attachments/assets/a7eda8cb-7cbb-4a7b-abb7-522b329ed39a)


---
Features
---

- Drag-and-drop CSV upload for transactions

- Combine multiple CSV files into one dataset

- Summary statistics: Total Income, Total Expenses, Net Total

- Visualizations:

  > Spending by category (pie chart)

  > Income vs Expenses over time (line chart)

- Filters:

  > Date range

  > Transaction categories

- Download combined transactions as CSV

- Backend API for storing and fetching transactions

---
Tech Stack
---

> Backend: Python, FastAPI, SQLAlchemy, SQLite

> Frontend: Python, Streamlit, Plotly, Pandas

> Data Storage: CSV files (data/uploads/) and optional database

> Visualization: Plotly charts

---
Usage
---
1️⃣ Run Backend (FastAPI)
> `uvicorn backend.main:app --reload`

2️⃣ Run Frontend (Streamlit)
> `streamlit run frontend/dashboard.py`
