import json
import sys
import os
from .overpass import get_boxes
from typing import Dict, List
# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Now import the module
from database import Database
db = Database()

def get_suburbs(names) -> List[Dict]:
    boxes = db.suburb.get_by_names(names)
    found = {b["name"] for b in boxes}
    print("found sububr names:", found)
    remaining = [name for name in names if name not in found]
    print("Remaining suburb names:", remaining)
    if remaining != []:
        remaining_boxes = get_boxes(remaining)
        if remaining_boxes != []:
            print("remaining suburb results:", remaining_boxes)
            db.suburb.add_many(remaining_boxes)
    return db.suburb.get_by_names(names)
