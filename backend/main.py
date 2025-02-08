from fastapi import FastAPI, HTTPException, Response, Request
from starlette.status import HTTP_200_OK
import os
import dotenv
from .helpers import download, security, camera, excel_reader
from .models.CameraLinksPublicKey import CameraLinksPublicKey
from .models.GetCamera import GetCamera

from fastapi.templating import Jinja2Templates
from database import Database
from models.CameraTypeEnum import CameraType

app = FastAPI()
templates = Jinja2Templates(directory="static")
# db = Database()
dotenv.load_dotenv()
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

@app.post("/resource-links")
async def resource_links(data: CameraLinksPublicKey):
    try:
        """
        if not security.verify_rsa_key_pair(data.public_key, PRIVATE_KEY):
            raise HTTPException(status_code=400, detail="Public Key is incorrect.")
        """

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
async def get_cameras() -> list[GetCamera]:
    try:
        return camera.get_cameras(None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get cameras data: {str(e)}")
    

@app.get("/")
async def main_page(request: Request):
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get main page: {str(e)}")