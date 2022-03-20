from flask import Flask, render_template, request
import requests
import urllib.parse


app=Flask(__name__)
#https://router.hereapi.com/v8/routes?
# transportMode=car
# &origin=52.5308,13.3847
# &destination=52.5323,13.3789
# &return=summary&apiKey=ihGga0Q7bhvnW8UAliqEYnlB-fy3rKjDTEKvNSIkfq0&alternatives=5
HERE_URL = 'https://router.hereapi.com/v8/routes?'
HERE_KEY = 'ihGga0Q7bhvnW8UAliqEYnlB-fy3rKjDTEKvNSIkfq0'
alternative_routes = '5'


@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/getroute',methods=['POST', 'GET'])
def getroute():
    origin = request.form.get("origin")
    destination = request.form.get("destination")
    mode = request.form.get("modeoftrans")

    origin_coords = getLatLong(origin)
    dest_coords = getLatLong(destination)
    
    route_request = HERE_URL+'transportMode='+mode+'&origin='+origin_coords[0]+','+origin_coords[1]+'&destination='+dest_coords[0]+','+dest_coords[1]+'&return=summary&apiKey='+HERE_KEY+'&alternatives='+alternative_routes
    routes = requests.get(route_request).json()
    for i in range(int(alternative_routes)):
        print(f"time for route {i+1}")
        print(routes['routes'][i]['sections'][0]['summary']['duration']/60)
        print(f"distance for route {i+1}")
        print(routes['routes'][i]['sections'][0]['summary']['length']/1000)


    return render_template('Home.html')

def getLatLong(address):
    # ONLY WORKS FOR AREA NAME AND CITY (CITY HAS TO BE THERE) OR ENABLE MAPS API FOR GEOCODING (BEST)
    print(urllib.parse.quote(address))
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
    response = requests.get(url).json()
    lat = response[0]["lat"]
    longit = response[0]["lon"]
    return [lat, longit]