import pandas as pd


def load_transactions(csv_file: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(csv_file)
        if "amount" in df.columns:
            df["amount"] = df["amount"].astype(float)
        return df
    except Exception:
        return pd.DataFrame()
