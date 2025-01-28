from typing import List

class POI:
    hour: int
    minute: int

    def __init__(self, id: int, name: str, type: str, latitude: float, longitude: float, tags: List[str]):
        self.id = id
        self.name = name
        self.type = type
        self.latitude = latitude
        self.longitude = longitude
        self.tags = tags
    
    def set_time(self, hour, minute):
        self.hour = hour
        self.minute = minute

    def __eq__(self, value):
        if isinstance(value, POI):
            return (self.name, self.type, self.latitude, self.longitude) == (value.name, value.type, value.latitude, value.longitude)
        return False

    def __hash__(self):
        return hash((self.name, self.type, self.latitude, self.longitude))

    def __repr__(self):
        formatted_hour = ('0' if self.hour < 10 else '' ) + str(int(self.hour))
        formatted_minute = ('0' if self.minute < 10 else '' ) + str(int(self.minute))
        return f"{formatted_hour}:{formatted_minute} - {self.name}, {self.type}"
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type,
            'position': {
                'latitude': self.latitude,
                'longitude': self.longitude
            },
            'tags': self.tags,
            'time': {
                'hour': self.hour,
                'minute': self.minute
            }
        }