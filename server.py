import json
from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS

from datetime import date

from Pathfinding.PointOfInterest import POI
from Pathfinding.Itinerary import Itinerary
from Pathfinding.Locations import Locations
from Scrappers.InstaScrapper import InstaScrapper
from Scrappers.POIScrapper import POIScrapper

app = Flask(__name__)
CORS(app)
# app.secret_key = 'turysta'

tourist_type={}

@app.route('/')
def hello_world():
    return render_template('mainPage.html')

@app.route('/form')
def form():
    return render_template('form.html')
@app.route('/survey')
def survey():
    return render_template('survey.html')
@app.route('/formSelectDataOrigin')
def formSelectDataOrigin():
    return render_template('formSelectDataOrigin.html')
@app.route('/chatBot')
def instagram():
    return render_template('chatBot.html')
@app.route('/instagram', methods=['GET'], endpoint='instagram_page')
def instagram():
    return render_template('instagram.html')
@app.route('/map')
def map():
    return render_template('map.html')


@app.route('/save-data-state', methods=['POST'])
def save_data_state():
    data = request.get_json()
    app.logger.debug(f"Saving data state: {data}")
    session['dataState'] = data
    return jsonify({'message': 'Data state saved successfully!'}), 200

@app.route('/get-data-state', methods=['GET'])
def get_data_state():
    data_state = session.get('dataState', {'chatBot': False, 'instagram': False, 'survey': False})
    app.logger.debug(f"Retrieving data state: {data_state}")
    return jsonify(data_state), 200


@app.route('/touristTypeDisplay')
def touristTypeDisplay():
    return render_template('touristTypeDisplay.html')


@app.post('/save-tourist-data')
def save_tourist_data():
    with open('data/tourist_data.json', 'r') as file:
        data = json.load(file)
    data.append(request.get_json())
    with open('data/tourist_data.json', 'w') as file:
        json.dump(data, file)

    return 'Data saved successfully!'

@app.get('/locations/')
def locations():
    city_name = request.args.get('city-name')
    num_of_days = int(request.args.get('num-of-days'))
    tourist_type = request.args.get('tourist-type')
    print(request.args.to_dict())
    start_date = date.fromisoformat(request.args.get('start-date'))
    scr = POIScrapper(tourist_type)
    pois = scr.get_POIs(city_name, num_of_days)
    locations = Locations(pois, start_date)
    daily_sets = locations.get_daily_sets(num_of_days)
    return locations.daily_sets_to_json(daily_sets)


@app.get('/itinerary/<int:num_of_days>')
def itinerary(num_of_days: int):
    with open('Pathfinding/POIs.json', 'r') as file:
        data = json.load(file)
    POIs = []
    for entry in data['tourist_attractions']:
        POIs.append(POI(entry['name'], entry['type'], entry['position']['latitude'], entry['position']['longitude'], entry['tags']))
    locations = Locations(POIs)
    daily_sets = locations.get_daily_sets(num_of_days)
    return Locations.daily_sets_to_json(daily_sets)
@app.route('/save-chatbot-data', methods=['POST'])
def save_chatbot_data():
    try:
        # Get the JSON data sent from the client
        form_data = request.get_json()
        chatbot_type = form_data.get("touristType")
        session['chatbot'] = tourist_type
        return jsonify({"message": "Your profile has been analysed!"}), 200  # Respond with success

    except Exception as e:
        # Handle any errors and return a 500 response
        return jsonify({"error": str(e)}), 500
@app.route('/save-instagram-username', methods=['POST'], endpoint='save_instagram_username')
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


@app.route('/save-survey-data', methods=['POST'])
def save_survey_data():
    try:
        # Get the JSON data sent from the client
        form_data = request.get_json()
        tourist_type = form_data.get("touristType")
        session['survey'] = tourist_type
        return jsonify({"message": "Your profile has been analysed!"}), 200  # Respond with success

    except Exception as e:
        # Handle any errors and return a 500 response
        return jsonify({"error": str(e)}), 500


@app.route('/get-instagram-data', methods=['GET'])
def get_instagram_data():
    instagram_data = session.get('instagram_data', {})
    return jsonify(instagram_data), 200

@app.route('/get-survey-data', methods=['GET'])
def get_survey_data():
    survey_data = session.get('survey', {})
    return jsonify(survey_data), 200
@app.route('/get-chatbot-data', methods=['GET'])
def get_chatbot_data():
    chatbot_data = session.get('chatbot', {})
    return jsonify(chatbot_data), 200

if __name__ == '__main__':
    app.run(debug=True)