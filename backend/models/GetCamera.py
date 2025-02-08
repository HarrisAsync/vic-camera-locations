from pydantic import BaseModel
from collections import defaultdict
from models.CameraTypeEnum import CameraType
from typing import Any, List

class GetCamera(BaseModel):
    id: int
    camera_type: CameraType
    points: defaultdict[Any, List]
    road: str
    suburb: str