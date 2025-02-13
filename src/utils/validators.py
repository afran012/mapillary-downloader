from typing import Tuple
from ..services.geospatial import BoundingBox

def validate_bbox(bbox: Tuple[float, float, float, float]) -> bool:
    try:
        box = BoundingBox(*bbox)
        return box.validate()
    except Exception:
        return False

def validate_username(username: str) -> bool:
    return bool(username and isinstance(username, str) and len(username.strip()) > 0)