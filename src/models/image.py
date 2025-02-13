from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Geometry(BaseModel):
    type: str
    coordinates: List[float]

class ImageMetadata(BaseModel):
    id: str
    geometry: Geometry
    thumb_1024_url: str
    captured_at: Optional[int] = None

    @property
    def filename(self) -> str:
        return f"{self.id}.jpg"

    @property
    def coordinates(self) -> tuple:
        return tuple(self.geometry.coordinates)