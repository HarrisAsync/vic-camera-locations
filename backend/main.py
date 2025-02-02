from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import FileResponse
import requests
import pandas as pd
import os

app = FastAPI()

class RequestData(BaseModel):
    link_PHST: str
    link_SPD: str
    public_key: str

def download_file(url: str, filename: str):
    response = requests.get(url)
    if response.status_code == 200:
        with open(filename, "wb") as file:
            file.write(response.content)
        return filename
    else:
        raise HTTPException(status_code=404, detail=f"Failed to download {url}. Status code: {response.status_code}")

def read_excel_rows(file_path: str):
    try:
        df = pd.read_excel(file_path)
        rows = df.to_dict(orient="records")
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading the Excel file: {str(e)}")

@app.get("/")
async def hello_world():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'static', 'index.html')
    print(file_path)
    return FileResponse(file_path)