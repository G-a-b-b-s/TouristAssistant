from Pathfinding.Locations import Locations
from Scrappers.POIScrapper import POIScrapper

# scr = POIScrapper('cultural')
# pois = scr.get_POIs('Warsaw', 3)
# locations = Locations(pois)
# daily_sets = locations.get_daily_sets(2)
# print(Locations.daily_sets_to_json(daily_sets))

scr = POIScrapper('')
pois_cultural = scr.get_POIs_single_type('Wrocław', 'cultural', 10)
pois_sport = scr.get_POIs_single_type('Wrocław', 'sport', 10)
pois_entertainment = scr.get_POIs_single_type('Wrocław', 'entertainment', 10)

print('City: Wrocław')
print('Cultural:')
for i, poi in enumerate(pois_cultural):
    print(f"{i + 1}. {poi.name}, {poi.type}; tags: {poi.tags}")
print('Sport:')
for i, poi in enumerate(pois_sport):
    print(f"{i + 1}. {poi.name}, {poi.type}; tags: {poi.tags}")
print('Entertainment:')
for i, poi in enumerate(pois_entertainment):
    print(f"{i + 1}. {poi.name}, {poi.type}; tags: {poi.tags}")