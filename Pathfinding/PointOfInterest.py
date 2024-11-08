class POI:
    def __init__(self, name: str, type: str, latitude: float, longitude: float, tags: dict):
        self.name = name
        self.type = type
        self.latitude = latitude
        self.longitude = longitude
        self.tags = tags