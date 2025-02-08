from pydantic import BaseModel
from collections import defaultdict
from .CameraTypeEnum import CameraType
from typing import Any, List, Dict

class GetCamera(BaseModel):
    id: int
    camera_type: CameraType
    points: str
    road: str
    suburb: str