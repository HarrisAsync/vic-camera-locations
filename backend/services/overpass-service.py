import requests
import json
import sys
import os

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import the module
from database import Database

db = Database()

def construct_overpass_query(suburbs, bbox=(-39.1590, 140.9617, -33.9806, 150.0133)):
    query = '[out:json][timeout:25];\n'
    query += '(\n'
    for suburb in suburbs:
        query += f'  relation\n    ["boundary"="administrative"]\n    ["name"="{suburb}"]\n    ({bbox[0]}, {bbox[1]}, {bbox[2]}, {bbox[3]});\n\n'
    query += ');\n'
    query += 'out bb;'
    return query

def execute_overpass_query(query):
    url = "https://overpass-api.de/api/interpreter"
    response = requests.post(url, data={"data": query})
    return response.json()

def process_results(results):
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
    db.suburb.add_many(res)

# Example usage
suburbs = ["Hampton", "Prahran", "St Kilda"]
overpass_query = construct_overpass_query(suburbs)
result = execute_overpass_query(overpass_query)
process_results(result)