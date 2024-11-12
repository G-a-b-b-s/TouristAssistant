from typing import List

class POI:
    def __init__(self, name: str, type: str, latitude: float, longitude: float, tags: List[str]):
        self.name = name
        self.type = type
        self.latitude = latitude
        self.longitude = longitude
        self.tags = tags
    
    def __eq__(self, value):
        if isinstance(value, POI):
            return (self.name, self.type, self.latitude, self.longitude) == (value.name, value.type, value.latitude, value.longitude)
        return False

    def __hash__(self):
        return hash((self.name, self.type, self.latitude, self.longitude))

    def __repr__(self):
        return f"{self.name}, {self.type} ({self.latitude}, {self.longitude})"