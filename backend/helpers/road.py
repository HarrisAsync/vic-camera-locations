import json
import sys
import os
from .overpass import get_roads
from .suburb import get_suburbs
from typing import Dict, List, Tuple
# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import the module
from database import Database
db = Database()

def get_roads(names: list[tuple]) -> List[Tuple[str, str]]:
    # get all roads not in db
    roads = db.road.get_by_names(names)
    found = {(r["name"], r["suburb"]) for r in roads}

    remaining_road_names = [r for r in names if r not in found]
    remaining_suburb_names = list({r[1] for r in remaining_road_names})
    remaining_suburbs = []

    if remaining_suburb_names != []:
        remaining_suburbs = get_suburbs(remaining_suburb_names)
    bbox = {s["name"]: s for s in remaining_suburbs}
    print("PASS 4")
    # get road data for remaining roads
    remaining_road_query = [
            {
                "name": r[0], 
                "minlat": bbox[r[1]]["minlat"],
                "maxlat": bbox[r[1]]["maxlat"],
                "maxlong": bbox[r[1]]["maxlong"],
                "minlong": bbox[r[1]]["minlong"]
            } for r in names if r not in found
        ]
    print("PASS 5")
    # get suburbs for remaining roads
    remaining_roads = []
    if remaining_road_query != [] and remaining_suburbs != []:
        remaining_roads = get_roads(remaining_road_query, remaining_suburbs)
        db.road.add_many([{"name": k[0], "suburb": k[1], "points": points} for k, points in remaining_roads.items()])
    return db.road.get_by_names(names)
if __name__ == "__main__":
    print(get_roads([("South Road", "Hampton"), ("Hampton Street", "Brighton")]))


