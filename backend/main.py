from fastapi import FastAPI
from backend.routes import auth, transactions, insights

app = FastAPI(title="AI Finance Assistant")

# Register routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(transactions.router,
                   prefix="/transactions", tags=["Transactions"])
app.include_router(insights.router, prefix="/insights", tags=["Insights"])


@app.get("/")
def root():
    return {"message": "Welcome to AI-Powered Personal Finance Assistant 🚀"}
