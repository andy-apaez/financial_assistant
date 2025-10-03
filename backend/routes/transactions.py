import glob
import os
from fastapi import APIRouter, UploadFile, File
import pandas as pd

router = APIRouter()

# Directory for uploaded CSVs
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload")
async def upload_transactions(file: UploadFile = File(...)):
    """
    Upload a CSV of transactions.
    Expected columns: date, description, amount, category
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save the uploaded file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Optional: verify CSV can be read
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        return {"status": "error", "message": f"Failed to read CSV: {e}"}

    return {"status": "success", "filename": file.filename, "rows": len(df)}


@router.get("/all")
async def get_transactions():
    """
    Returns combined transactions from all CSVs in data/uploads/
    """
    files = glob.glob(os.path.join(UPLOAD_DIR, "*.csv"))
    if not files:
        return {"transactions": []}

    # Combine all CSVs
    df_list = []
    for f in files:
        try:
            df_list.append(pd.read_csv(f))
        except Exception:
            continue  # skip invalid CSVs

    if not df_list:
        return {"transactions": []}

    df = pd.concat(df_list, ignore_index=True)
    return {"transactions": df.to_dict(orient="records")}
