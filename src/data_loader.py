import pandas as pd
import os

def load_adresar():
    csv_path = "/data/in/tables/ADRESAR.csv"   # EXACT NAME FROM KEEBOOLA
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"adresar.csv neexistuje: {csv_path}")
    return pd.read_csv(csv_path).fillna("")

def get_people_list():
    df = load_adresar()
    return {row["NAME"]: row.to_dict() for _, row in df.iterrows()}
