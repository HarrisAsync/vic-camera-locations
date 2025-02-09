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
    remaining = [name for name in names if name not in found]

    if remaining != []:
        remaining_boxes = get_boxes(remaining)
        db.suburb.add_many(remaining_boxes)
    return db.suburb.get_by_names(names)
