import json
import sys
import os
import string
from .overpass import get_roads as overpass_get_roads
from .suburb import get_suburbs
from typing import Dict, List, Tuple
# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import the module
from database import Database
db = Database()

def get_roads(names: list[tuple]) -> List[Tuple[str, str]]:
    names = [(string.capwords(n[0]), string.capwords(n[1])) for n in names]
    # get all roads not in db
    roads = db.road.get_by_names(names)
    found = {(r["name"], r["suburb"]) for r in roads}
    print(found)
    remaining_road_names = [r for r in names if r not in found]
    print("remaing: ", remaining_road_names)
    remaining_suburb_names = list({r[1] for r in remaining_road_names})
    print("remaining suburbs: ", remaining_suburb_names)
    remaining_suburbs = []
    if remaining_suburb_names != []:
        remaining_suburbs = get_suburbs(remaining_suburb_names)
    print("remaining subburb results")
    bbox = {s["name"]: s for s in remaining_suburbs}
    print("PASS 4")
    # get road data for remaining roads
    remaining_road_query = [
            {
                "name": r[0], 
                "suburb": bbox[r[1]]["name"],
                "minlat": bbox[r[1]]["minlat"],
                "maxlat": bbox[r[1]]["maxlat"],
                "maxlong": bbox[r[1]]["maxlong"],
                "minlong": bbox[r[1]]["minlong"]
            } for r in names if (r[0], r[1]) not in found and r[1] in bbox
        ]
    print("remaining_road_query", remaining_road_query)
    print("PASS 5")
    # get suburbs for remaining roads
    if remaining_road_query != [] and remaining_suburbs != []:
        overpass_get_roads(remaining_road_query)
    return db.road.get_by_names(names)
if __name__ == "__main__":
    print(get_roads([("South Road", "Hampton"), ("Hampton Street", "Brighton")]))


