from fastapi import FastAPI, HTTPException, Response, Request
from starlette.status import HTTP_200_OK
import asyncio
import dotenv
from .helpers import security, camera, excel_reader
from .models.CameraLinksPublicKey import CameraLinksPublicKey
from .models.GetCamera import GetCamera

from fastapi.templating import Jinja2Templates
from database import Database
from models.CameraTypeEnum import CameraType

app = FastAPI()
templates = Jinja2Templates(directory="static")
# db = Database()
dotenv.load_dotenv()
# PRIVATE_KEY = os.getenv("PRIVATE_KEY")

@app.post("/resource-links")
async def resource_links(data: CameraLinksPublicKey):
    try:
        """
        if not security.verify_rsa_key_pair(data.public_key, PRIVATE_KEY):
            raise HTTPException(status_code=400, detail="Public Key is incorrect.")
        """
        # Fetch and read
        PHST_road_suburbs = excel_reader.get_road_suburb_from_excel(data.link_PHST, CameraType.PHST)
        SPD_road_suburbs = excel_reader.get_road_suburb_from_excel(data.link_SPD, CameraType.SPD)

        # Combine lists
        final_list = []
        final_list.extend(PHST_road_suburbs)
        final_list.extend(SPD_road_suburbs)

        # Update cameras in the database
        camera.update_cameras(final_list)
        print("Updated!")
    except Exception as e:
        print(e)
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
    
if __name__ == "__main__":
    c = CameraLinksPublicKey(
        link_PHST="https://www.vic.gov.au/sites/default/files/2024-12/DDS_camera_locations_January-2025.xlsx",
        link_SPD="https://www.vic.gov.au/sites/default/files/2024-12/Mobile_Camera_Locations_January-2025.xlsx",
        public_key="abc123"
    )
    asyncio.run(resource_links(c))