from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.responses import FileResponse
import requests
import pandas as pd

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
    return FileResponse("static/index.html")

@app.post("/resource-links")
async def resource_links(request_data: RequestData):
    phst_filename = "downloaded_PHST_file.xlsx"
    spd_filename = "downloaded_SPD_file.xlsx"
    try:
        if request_data.link_PHST:
            phst_file_path = download_file(request_data.link_PHST, phst_filename)
            phst_rows = read_excel_rows(phst_file_path)
        if request_data.link_SPD:
            spd_file_path = download_file(request_data.link_SPD, spd_filename)
            spd_rows = read_excel_rows(spd_file_path)

        return {
            "message": "Files downloaded and read successfully",
            "files": {
                "PHST": phst_rows if request_data.link_PHST else "No PHST file",
                "SPD": spd_rows if request_data.link_SPD else "No SPD file"
            }
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
