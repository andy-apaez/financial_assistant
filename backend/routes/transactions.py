from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
import pandas as pd
from backend.database import SessionLocal
import os

router = APIRouter()

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/upload")
async def upload_transactions(file: UploadFile = File(...)):
    """
    Upload a CSV of transactions.
    Expected columns: description, category (optional), amount, date
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    df = pd.read_csv(file_path)

    clean_path = os.path.join("data", "transactions.csv")
    df.to_csv(clean_path, index=False)

    return {"status": "success", "rows": len(df)}


@router.get("/all")
async def get_transactions():
    """
    Return all stored transactions as JSON.
    """
    file_path = os.path.join("data", "transactions.csv")
    if not os.path.exists(file_path):
        return {"transactions": []}

    df = pd.read_csv(file_path)
    return {"transactions": df.to_dict(orient="records")}
