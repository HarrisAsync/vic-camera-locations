from backend.helpers import excel_reader
from fastapi import FastAPI, HTTPException, Response, Request
from starlette.status import HTTP_200_OK
import os
from helpers import download, security, camera
from models import CameraLinksPublicKey, GetCamera
from fastapi.templating import Jinja2Templates
from database import Database
from models.CameraTypeEnum import CameraType

app = FastAPI()
templates = Jinja2Templates(directory="package_docs")
db = Database()

@app.post("/resource-links")
async def resource_links(data: CameraLinksPublicKey):
    try:
        # Verify public key
        file_path = os.path.join("../data", "private_key.txt")
        with file_path.open("r", encoding="utf-8") as file:
            content = file.read()
            if not security.verify_rsa_key_pair(data.public_key, content):
                raise HTTPException(status_code=400, detail="Public Key is incorrect.")

        # Download files
        f_temp_PHST = download.download_file(data.link_PHST)
        f_temp_SPD = download.download_file(data.link_SPD)

        # Get rows in files
        PHST_road_suburbs = excel_reader.get_road_suburb_from_excel(f_temp_PHST, CameraType.PHONE)
        SPD_road_suburbs = excel_reader.get_road_suburb_from_excel(f_temp_SPD, CameraType.MOBILE)
        os.remove(f_temp_PHST)
        os.remove(f_temp_SPD)

        # Combine lists
        final_list = PHST_road_suburbs + SPD_road_suburbs

        # Update cameras in the database
        camera.update_cameras(final_list)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve data: {str(e)}")

    return Response(status_code=HTTP_200_OK)

@app.get("/get-cameras")
async def get_cameras() -> list[GetCamera.GetCamera]:
    return camera.get_cameras()

@app.get("/")
async def main_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
