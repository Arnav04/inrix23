from flask import Flask, render_template, request, jsonify
# from flask_socketio import SocketIO
#from flask_pymongo import PyMongo
import pandas as pd
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import requests

app = Flask(__name__)
# socketio = SocketIO(app)
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/safepark'
# mongo = PyMongo(app)
payload, headers= {}, {}
INRIX_AUTH_URL = 'https://api.iq.inrix.com/auth/v1/appToken?appId=mpdesmsn7h&hashToken=bXBkZXNtc243aHxjNlNXYXhBaXU1NktMaFZpMll2dnNhT3VTTnU2cTFZSDZKaHF4SFE5'
response = requests.request("GET", INRIX_AUTH_URL, headers=headers, data=payload).json()
INRIX_TOKEN = response["result"]["token"]

lots = {}
vals = {}

# API endpoint for getting parking options
@app.route('/api/get_parking', methods=['POST'])
def get_parking():
    try:
        data = request.get_json()
        
        # Get coordinates and bounding box using the helper functions
        lat = getLatitude(data)
        long = getLongitude(data)
        limit = 25
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {INRIX_TOKEN}'
        }

        INRIX_OFF_PARKING_URL = f"https://api.iq.inrix.com/lots/v3?point={lat}%7C{long}&radius=150&token={INRIX_TOKEN}"
        off_response = requests.request("GET", INRIX_OFF_PARKING_URL, headers=headers, data=payload)
        INRIX_ON_PARKING_URL = f'https://api.iq.inrix.com/blocks/v3?point={lat}%7C{long}&radius=150&limit=25&token={INRIX_TOKEN}'
        on_response = requests.request("GET", INRIX_ON_PARKING_URL, headers=headers, data=payload)

        off_data = off_response.json()
        on_data = on_response.json()

        # Create a unique identifier for each parking location
        parking_locations = []
        for parking in off_data["parking"]:
            parking_locations.append({"type": "off", "location_id": parking["id"]})

        for parking in on_data["parking"]:
            parking_locations.append({"type": "on", "location_id": parking["id"]})

        combined_response = {"off_street": off_data, "on_street": on_data, "locations": parking_locations}
        lots[data] = combined_response

        return combined_response, 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def convertToCoordinates_addy(place):
    payload, headers= {}, {}
    placee = '+'.join(place.split())

    base_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={placee}&key=AIzaSyBCVX3901fCD-pTLejQ8_O0nDvgZK3_E9c'

    response = requests.request("GET", base_url, headers=headers, data=payload)
    data = response.json() 
    if response.status_code == 200 and data['status'] == 'OK':
        # Extract the coordinates from the response
        location = data['results'][0]['geometry']['location']
        latitude, longitude = location['lat'], location['lng']
        
        formatted_coordinates = f"{latitude}|{longitude}"
        return formatted_coordinates
    else:
        return None

def getLatitude(place):
    payload, headers= {}, {}
    placee = '+'.join(place.split())

    base_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={placee}&key=AIzaSyBCVX3901fCD-pTLejQ8_O0nDvgZK3_E9c'

    response = requests.request("GET", base_url, headers=headers, data=payload)
    data = response.json()

    if response.status_code == 200 and data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        latitude = location['lat']
        return latitude
    else:
        print(f"Error: {data['status']}")
        return None

def getLongitude(place):
    payload, headers= {}, {}
    placee = '+'.join(place.split())

    base_url = f'https://maps.googleapis.com/maps/api/geocode/json?address={placee}&key=AIzaSyBCVX3901fCD-pTLejQ8_O0nDvgZK3_E9c'

    response = requests.request("GET", base_url, headers=headers, data=payload)
    data = response.json()

    if response.status_code == 200 and data['status'] == 'OK':
        location = data['results'][0]['geometry']['location']
        longitude = location['lng']
        return longitude
    else:
        print(f"Error: {data['status']}")
        return None
    
#Incident API
@app.route('/assess_parking_safety', methods=['POST'])
def get_incidents_data(place):
    try:
        lat = getLatitude(place)
        long = getLongitude(place)
        headers = {
        'Content-Type': 'application/json',
        'Authorization':
                'Bearer [eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhcHBJZCI6Im1wZGVzbXNuN2giLCJ0b2tlbiI6eyJpdiI6Ijc2ZmYzNTlhNTE3NWI5NjM5ZmQyZWQ1NTM0YTNhOTFkIiwiY29udGVudCI6ImU2M2UwMjljODQ0MDAwZWVlYzY1MzMxZTlhMmQyZmU1NjI1ZmQ2ODYxMTFhYTJmYTM5YWUyZjJiZTdmNzBkNDNmYTc3NmM0MzU5YmY5NWVhZTc0MGM5OTY5YjllZDZmZDM5ZWQ4NWYyMWRlNTU0ZGQyNzlkNjY5Mjk5YmNiMmFlMjQ0YjM4M2RlMTBmZjFiMDFjODEyOWUxM2VjZTQ3ODRlMTIzZjk2MjRmM2RlNDFlOGYwZDFlMjJkMDJjMzA2NjAwNWRjMjY0ZDU1ZmJmN2RhYTQyNDhlNGJjZTc0N2YwOGZjYzM2MTc0YTVmMzY2MzQ1ZDhjZjhmY2MxZjU3MTNlNGQ5Mjk0NGQ1YzRjZDc0ZTAyZmQwNDAzODM0OGVmYThhOTk3MWUxMGRjOTY4OGQ3YzcwMzBjYWQ4YjQ2ZjBiYWY2NDc5ZmE2N2JkNTgyYzRkNmU5N2QzYWEyM2EwYWRlZDMyZDQ3ODVhYjFiMmMyODFmOTc5NjI0NjY1NWZjNTgxNWI0Nzg1YjA1MzdlODI0MTEzNDYyYzY5YzcxNzJiZjJhYjhiODY0MmU3M2UzMTY2OWY2YjlkNjk2NDY1ODY4N2ZjYmJlNTFhMWM3ZGQ1NmRlNzEwZDYzYjBjOTVhYjI4YzgxODgyYTg4ZWFiY2I0MDE0MWUxYzQ4MjljYmE0ZGQxNDhkYWQ5YzhmMzliMjI1Y2Q2YzdmOTU2MWNmZmFmOTMwYjAwMDczOTdkNzJmNWJiMDM0ZTBkMzYxZmViNDYzMDUwZTQyZjUyMjM0NjVjNTBiMDViZTJlODBmMmVkYTY4MWVhYzczZjRiNGUyYmEyM2RlMTJiZWFmYTg0Mjg1ZTIwZmY4YjRhZjc3YTg2MjJhODNjIn0sInNlY3VyaXR5VG9rZW4iOnsiaXYiOiI3NmZmMzU5YTUxNzViOTYzOWZkMmVkNTUzNGEzYTkxZCIsImNvbnRlbnQiOiJjNTMwMzE5NzgzNTM0ZWUxZDE3YzJmMDFiNTFkMmM4MTRmNjVjN2JjMWQyNWMzYWMwY2ExMjc0Y2ViZmYwYjZkZTMwMDcwMzMyZDk4OGU5MmU3NDFiMWE4In0sImp0aSI6ImVhNmRiNTM4LWFmYmItNDcwYy04NGEwLTE3ZDQ4ZDU4ODk1YyIsImlhdCI6MTY5OTc5NTIxMSwiZXhwIjoxNjk5Nzk4ODExfQ.c8zpzODpepx_K97TMw4sptBxfPWefQRv77xdn3lEcrU]'
        }
        INRIX_INCIDENTS_URL = f"https://api.iq.inrix.com/v1/incidents?box={lat}%7C{long}%2C37.746138%7C-122.395481&radius=150&incidentoutputfields=All&incidenttype=Incidents,Flow,Construction&locale=en&token={INRIX_TOKEN}"
        response = requests.request("GET", INRIX_INCIDENTS_URL, headers=headers, data=payload)
        return response.json()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def assess_parking_safety(place):
    try:
        # Use INRIX Incidents API to get safety information
        incidents_data = get_incidents_data(place)

        # Calculate the total number of incidents, which will dictate how dangerous or safe a certain area is
        num_of_incidents = len(incidents_data)

        return num_of_incidents

    except Exception as e:
        return jsonify({'error': str(e)}), 500


def crim_file_data(latitude, longitude):
    df = pd.read_csv("Police_Department_Incident_Reports__2018_to_Present.csv", delimiter = ",")
    df.drop(columns=['Current Police Districts','Supervisor District 2012', 'Analysis Neighborhood', 'CNN','CAD Number', 'Filed Online','ESNCAG - Boundary File', 'Invest In Neighborhoods (IIN) Areas','Central Market/Tenderloin Boundary Polygon - Updated', 'HSOC Zones as of 2018-06-05', 'Civic Center Harm Reduction Project Boundary']) #removing those with >35% null vals
    key_strings = [
    'Vandalism',
    'Motor Vehicle Theft',
    'Larceny Theft',
    'Robbery'
    ]

    df = df[df['Incident Category'].isin(key_strings)]
    df = df.dropna(subset='Point')

    square_corners = calc_square(latitude, longitude)

    top_left = square_corners[0]
    top_right = square_corners[1]
    bottom_left = square_corners[2]
    bottom_right = square_corners[3]

    lat_TL = top_left[0]
    long_TL = top_left[1]

    lat_TR = top_right[0]
    long_TR = top_right[1]

    lat_BL = bottom_left[0]
    long_BL = bottom_left[1]

    lat_BR = bottom_right[0]
    long_BR = bottom_right[1]

    boundary_points = [(lat_TL, long_TL), (lat_TR, long_TR), (lat_BL, long_BL), (lat_BR, long_BR)]
    polygon = Polygon(boundary_points)

    crimes_inside = 0

    for index, row in df.iterrows():
        tlat = row['Latitude']
        tlong = row['Longitude']
        lat = round(tlat, 4)
        long = round(tlong, 4)
        test_point = Point(lat, long)
        if test_point.within(polygon):
            crimes_inside += 1

    return crimes_inside;


def calc_square(latitude, longitude):
    side = 0.0006

    top_left = (latitude + side, longitude - side)
    top_right = (latitude + side, longitude + side)
    bottom_left = (latitude - side, longitude - side)
    bottom_right = (latitude - side, longitude + side)

    return [top_left, top_right, bottom_left, bottom_right]

@app.route('/api/sort_search', methods=['GET'])
def sort_search():
    try:
        scores = {}
        for place, data in lots.items():
            score = calculate_score(place)
            scores[place] = {"score": score, "locations": data.get("locations", [])}

        # Sort the results based on the scores
        sorted_scores = dict(sorted(scores.items(), key=lambda item: item[1]["score"], reverse=True))
        return sorted_scores

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/assess_parking_safety', methods=['POST'])
def assess_safety(): # test this
    try:
        for place in lots:
            crime = crim_file_data(getLatitude(place), getLongitude(place))
            incidents = assess_parking_safety(place)
            score_denom = (1.5 * crime) + incidents + 1
            score = 1 / score_denom
            vals[place] = score

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/get_sorted_vals', methods=['GET'])
def get_sorted_vals():
    try:
        sorted_vals = dict(sorted(vals.items(), key=lambda item: item[1], reverse=True))
        return sorted_vals

    except Exception as e:
        return jsonify({'error': str(e)}), 500

def getCoordinates():
    # Assuming you want to get a map of parking lot names to coordinates from the 'lots' dictionary
    parking_lot_coordinates = {}

    for place, data in lots.items():
        # Extract the first location's name and coordinates
        if data["locations"]:
            location = data["locations"][0]
            latitude = data["peps"]["pepPt"][1]
            latitude = data["peps"]["pepPt"][0]
            parking_lot_coordinates[lot_name] = {"latitude": latitude, "longitude": longitude}