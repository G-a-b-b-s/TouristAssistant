import requests
from Pathfinding.PointOfInterest import POI

from typing import List

class POIScrapper:
    tourist_type: str
    GOOGLE_API_KEY = 'AIzaSyCUws2hUjBLhWoiMCxt2qnPQYjI4TCTCbY'

    def __init__(self, tourist_type):
        self.tourist_type = tourist_type

    def get_coords(self, city: str):
        url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={self.GOOGLE_API_KEY}"
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            if data['status'] == 'OK':
                location = data["results"][0]["geometry"]["location"]
                lat = location['lat']
                lng = location['lng']
                return (lat, lng)
            else:
                print(f'Error: {data["status"]}')
        else:
            print(f'Failed to connect to API {res.text}')

    def get_POIS_by_type(self, lat: float, lng: float, type: str, amount: int):
        includedTypes = []
        if type== 'general':
            includedTypes = ['tourist_attraction']
        elif type == 'cultural':
            includedTypes = ['monument', 'cultural_landmark', 'historical_landmark', 'historical_place', 'performing_arts_theater', 'museum', 'art_gallery', 'philharmonic_hall', 'opera_house']
        elif type == 'sport':
            includedTypes = ['sports_activity_location', 'ski_resort', 'sports_complex', 'ice_skating_rink', 'golf_course', 'arena', 'stadium', 'adventure_sports_center']
        elif type == 'entertainment':
            includedTypes = ['beach', 'amusement_center', 'amusement_park', 'aquarium', 'botanical_garden', 'bowling_alley', 'comedy_club', 'concert_hall', 'planetarium', 'night_club', 'national_park', 'marina', 'zoo']

        res = requests.post("https://places.googleapis.com/v1/places:searchNearby", json={
                "includedTypes": includedTypes,
                "maxResultCount": amount,
                "locationRestriction": {
                "circle": {
                    "center": {
                        "latitude": lat,
                        "longitude": lng
                    },
                    "radius": 10000.0
                    }
                }
            }, headers={
                "X-Goog-Api-Key": self.GOOGLE_API_KEY,
                "X-Goog-FieldMask": "places.id,places.displayName,places.primaryType,places.types,places.location"
            })

        if res.status_code == 200:
            places = res.json()['places']
            pois = []
            for place in places:
                id = place['id']
                name = place['displayName']['text']
                type = place['primaryType'] if 'primaryType' in place else place['types'][0]
                location = place['location']
                tags = place['types']
                poi = POI(id, name, type, location['latitude'], location['longitude'], tags)
                pois.append(poi)
            return pois
        else:
            print(f'Failed to connect to API {res.text}')

    def get_POIs(self, city: str, num_of_days: int):
        lat, lng = self.get_coords(city)
        pois = self.get_POIS_by_type(lat, lng, self.tourist_type, num_of_days * 10)
        return pois

    # def get_POIs(self, city: str, num_of_days: int):
    #     lat, lng = self.get_coords(city)
    #     num = 2 * num_of_days
    #     pois0 = self.get_POIS_by_type(lat, lng, 'general', num)
    #     pois1 = self.get_POIS_by_type(lat, lng, "cultural", 2*num if self.tourist_type == 'cultural' else num)
    #     pois2 = self.get_POIS_by_type(lat, lng, "sport", 2*num if self.tourist_type == 'sport' else num)
    #     pois3 = self.get_POIS_by_type(lat, lng, "entertainment", 2*num if self.tourist_type == 'entertainment' else num)

    #     ids = [x.id for x in pois0]
    #     for poi in pois1:
    #         if poi.id not in ids:
    #             pois0.append(poi)
    #     ids = [x.id for x in pois0]
    #     for poi in pois2:
    #         if poi.id not in ids:
    #             pois0.append(poi)
    #     ids = [x.id for x in pois0]
    #     for poi in pois3:
    #         if poi.id not in ids:
    #             pois0.append(poi)
    #     return pois0

    def get_POIs_single_type(self, city: str, type: str, num_of_days: int) -> List[POI]:
        lat, lng = self.get_coords(city)
        pois = self.get_POIS_by_type(lat, lng, type, num_of_days)
        return pois