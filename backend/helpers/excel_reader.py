import pandas as pd
from fastapi import HTTPException

def read_excel_rows(file_path: str):
    try:
        df = pd.read_excel(file_path)
        rows = df.to_dict(orient="records")
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading the Excel file: {str(e)}")