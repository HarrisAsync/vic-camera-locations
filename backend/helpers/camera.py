import json
import sys
import os
import overpass
from typing import Dict, List
from road import get_roads

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.CameraTypeEnum import CameraType
from database import Database
db = Database()

# [(road name, suburb, type)]
def update_cameras(cameras):
    roads = get_roads(list({(c[0], c[1]) for c in cameras}))
    # Create a dictionary mapping (name, suburb) to id
    road_id_map = {(road["name"], road["suburb"]): road["id"] for road in roads}

    # Transform the data
    camera_data = [{"camera_type": r_type, "road_id": road_id_map.get((name, suburb))} for name, suburb, r_type in cameras]
    db.camera.set_new(camera_data)

def get_cameras(type):
    return db.camera.get_all(type)

if __name__ == "__main__":
    print(get_cameras(None))
