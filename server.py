import json
from flask import Flask, render_template, request, jsonify, session

from Pathfinding.PointOfInterest import POI
from Pathfinding.Itinerary import Itinerary
from Scrappers.InstaScrapper import InstaScrapper
from Scrappers.TwitterScraper import TwitterScrapper

app = Flask(__name__)
app.secret_key = 'turysta'

@app.route('/')
def hello_world():
    return render_template('mainPage.html')

@app.route('/form')
def form():
    return render_template('form.html')
@app.route('/formTouristType')
def formTouristType():
    return render_template('formTouristType.html')
@app.route('/formSelectDataOrigin')
def formSelectDataOrigin():
    return render_template('formSelectDataOrigin.html')
@app.route('/twitter')
def twitter():
    return render_template('twitter.html')
@app.route('/instagram')
def instagram():
    return render_template('instagram.html')
@app.route('/map')
def map():
    return render_template('map.html')

@app.post('/save-tourist-data')
def save_tourist_data():
    with open('data/tourist_data.json', 'r') as file:
        data = json.load(file)
    data.append(request.get_json())
    with open('data/tourist_data.json', 'w') as file:
        json.dump(data, file)

    return 'Data saved successfully!'

@app.get('/itinerary/<int:num_of_days>')
def itinerary(num_of_days: int):
    with open('Pathfinding/POIs.json', 'r') as file:
        data = json.load(file)
    POIs = []
    for entry in data['tourist_attractions']:
        POIs.append(POI(entry['name'], entry['type'], entry['position']['latitude'], entry['position']['longitude'], entry['tags']))
    it = Itinerary(POIs, num_of_days)
    return it.to_json()

@app.route('/save-username-twitter', methods=['POST'])
def save_username_twitter():
    try:
        # Get the JSON data sent from the client
        data_received = request.get_json()
        username = data_received.get('username')
        if not username:
            return jsonify({"error": "Username is required"}), 400

        tweeter_scrapper = TwitterScrapper(username)
        profile_data = {"username": username}
        session['twitter_data'] = profile_data


        return jsonify({"message": "Your profile has been analysed!"}), 200  # Respond with success

    except Exception as e:
        # Handle any errors and return a 500 response
        return jsonify({"error": str(e)}), 500


@app.route('/save-username-instagram', methods=['POST'])
def save_username_instagram():
    try:
        # Get the JSON data sent from the client
        data_received = request.get_json()
        username = data_received.get('username')

        if not username:
            return jsonify({"error": "Username is required"}), 400

        insta_scrapper = InstaScrapper(username)
        profile_data = {"username": username}
        session['instagram_data'] = profile_data


        return jsonify({"message": "Your profile has been analysed!"}), 200  # Respond with success

    except Exception as e:
        # Handle any errors and return a 500 response
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)