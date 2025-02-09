import requests
import pprint
import json
import time
import string
from collections import defaultdict
import sys, os
from typing import Dict, List
# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import the module
from database import Database
db = Database()

def execute_overpass_query(query):
    url = "https://overpass-api.de/api/interpreter"
    response = requests.post(url, data={"data": query})
    return response.json()

def construct_road_query(data):
    query = "[out:json][timeout:25];\n("
    for row in data:
        bounding_box = f"({row['minlat']},{row['minlong']},{row['maxlat']},{row['maxlong']})"
        query += f"  way {bounding_box}\n  [\"highway\"]\n  [\"name\"=\"{string.capwords(row['name'])}\"];\n"
    query += ");\nout geom;"
    return query

def process_road_results(overpass_data, road_dict):
    ways = defaultdict(list)

    for element in overpass_data.get("elements", []):
        if element.get("type") == "way":
            tags = element.get("tags", {})
            name = tags.get("name")
            if name not in road_dict:
                continue

            geometry = element.get("geometry", [])

            # Only store ways that actually have a name
            if name and geometry:
                coords = []
                for g in geometry:
                    coords.append({"lat": g["lat"], "lng": g["lon"]})
                if road_in_suburb(coords, road_dict[name]):
                    ways[(name, road_dict[name]["suburb"])].append(coords)
    return ways


def construct_suburb_query(suburbs, bbox=(-39.1590, 140.9617, -33.9806, 150.0133)):
    query = '[out:json][timeout:25];\n'
    query += '(\n'
    for suburb in suburbs:
        query += f'  relation\n    ["boundary"="administrative"]\n    ["name"="{string.capwords(suburb)}"]\n    ({bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]});\n\n'
    query += ');\n'
    query += 'out bb;'
    return query

def process_suburb_results(results):
    res = []
    for element in results.get("elements", []):
        name = element.get("tags", {}).get("name", "Unknown")
        bounds = element.get("bounds", {})
        res.append({
            "name": name, 
            "minlat": bounds.get('minlat'), 
            "minlong": bounds.get('minlon'), 
            "maxlat": bounds.get('maxlat'), 
            "maxlong": bounds.get('maxlon')
        })
    return res

def get_boxes(names):
    res = []
    for i in range(0, len(names), 20):
        q = construct_suburb_query(names[i:i + 10])
        # print(q)
        r = execute_overpass_query(q)
        res = res + process_suburb_results(r)
        # print(res)
        time.sleep(0.5)
    return res

def get_roads(names):
    print(len(names))
    road_dict = {r["name"]: r for r in names}
    for i in range(0, len(names), 20):
        print(i)
        q = construct_road_query(names[i:i+10])
        # print(names[i:i+10], i)
        r = execute_overpass_query(q)
        roads = process_road_results(r, road_dict)
        print("len", len(roads))
        # print(roads)
        db.road.add_many([{"name": k[0], "suburb": k[1], "points": points} for k, points in roads.items()])
        time.sleep(0.5)

def road_in_suburb(points, suburb):
    number_outside = 0
    for p in points:
        if not in_suburb(p, suburb): 
            number_outside += 1
            if number_outside > 10:
                return False
    return True

def in_suburb(point, suburb):
    maxDist = 1.5 * max(
            (abs(suburb["maxlong"] - suburb["minlong"])), 
            (abs(suburb["maxlat"] - suburb["minlat"]))
        )
    

    if (
            max(abs(point["lng"] - suburb["minlong"]), abs(point["lng"] - suburb["maxlong"])) > maxDist or
            max(abs(point["lat"] - suburb["minlat"]), abs(point["lng"] - suburb["maxlat"])) > maxDist
        ):
        return False
    return True

def merge_dicts(d1, d2):
    new = defaultdict(list)
    for k, v in d1.items():
        new[k] = v
    for k, v in d2.items():
        new[k] = v
    return new
if __name__ == "__main__":
    data = [
        {"name": "Marine Parade", "minlong": 144.970653, "minlat": -37.876291, "maxlong": 144.993262, "maxlat": -37.852189},
        {"name": "Chapel Street", "minlong": 144.984201, "minlat": -37.8601785, "maxlong": 145.0123174, "maxlat": -37.845688},
        {"name": "HAMPTON STREET", "minlong": 144.992117, "minlat": -37.946992, "maxlong": 145.025241, "maxlat": -37.92871}
    ]
    names = ["HAMPTON", "HALLS GAP"]
    q = construct_suburb_query(names)
    print(q)
    r = execute_overpass_query(q)
    print(process_suburb_results(r))
    # get_roads(data)
    # print(get_roads(data))
    # print(construct_road_query(data))
    # pprint.pprint(execute_overpass_query(q))