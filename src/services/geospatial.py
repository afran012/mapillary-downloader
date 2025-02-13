from typing import Tuple

class BoundingBox:
    def __init__(self, min_lon: float, min_lat: float, max_lon: float, max_lat: float):
        self.min_lon = min_lon
        self.min_lat = min_lat
        self.max_lon = max_lon
        self.max_lat = max_lat

    @property
    def as_tuple(self) -> Tuple[float, float, float, float]:
        return (self.min_lon, self.min_lat, self.max_lon, self.max_lat)

    def validate(self) -> bool:
        if not (-180 <= self.min_lon <= 180 and -180 <= self.max_lon <= 180):
            return False
        if not (-90 <= self.min_lat <= 90 and -90 <= self.max_lat <= 90):
            return False
        if self.min_lon > self.max_lon or self.min_lat > self.max_lat:
            return False
        return True