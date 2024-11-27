import requests

# API Key
API_KEY = 'AIzaSyCUws2hUjBLhWoiMCxt2qnPQYjI4TCTCbY'
# Place Details endpoint
details_url = "https://maps.googleapis.com/maps/api/place/details/json"

# Parameters
params = {
    'place_id': 'ChIJY7-qdG1bFkcRUWWvcALT8y4',  # Obtained from the Nearby Search response
    'fields': 'name,opening_hours',  # Specify fields to include in the response
    'key': API_KEY
}

# Make the request
response = requests.get(details_url, params=params)

# Extract and display opening hours
if response.status_code == 200:
    details = response.json().get('result', {})
    name = details.get('name')
    opening_hours = details.get('opening_hours', {}).get('weekday_text', 'Not available')
    
    print(f"Name: {name}")
    print("Opening Hours:")
    if opening_hours != 'Not available':
        for day in opening_hours:
            print(day)
    else:
        print(opening_hours)
else:
    print(f"Error: {response.status_code}, {response.text}")
