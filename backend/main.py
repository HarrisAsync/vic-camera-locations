from backend.helpers import excel_reader
from fastapi import FastAPI, HTTPException, Response, Request
from starlette.status import HTTP_200_OK
import os
from helpers import download, security
from models import CameraLinksPublicKey
from fastapi.templating import Jinja2Templates
from database import Database

app = FastAPI()
templates = Jinja2Templates(directory="package_docs")
db = Database()

@app.post("/resource-links")
async def resource_links(data: CameraLinksPublicKey):
    try:
        file_path = os.path.join("../data", "private_key.txt")
        with file_path.open("r", encoding="utf-8") as file:
            content = file.read()
            if not security.verify_rsa_key_pair(data.public_key, content):
                raise HTTPException(status_code=400, detail="Public Key is incorrect.")

        f_temp_PHST = download.download_file(data.link_PHST)
        f_temp_SPD = download.download_file(data.link_SPD)

        PHST_rows = excel_reader.read_excel_rows(f_temp_PHST)
        SPD_rows = excel_reader.read_excel_rows(f_temp_SPD)

        os.remove(f_temp_PHST)
        os.remove(f_temp_SPD)

        # TODO: For PHST_rows SPD_rows & Use overpass service to get data

        # TODO: Store in tables
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve data: {str(e)}")

    return Response(status_code=HTTP_200_OK)

@app.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
