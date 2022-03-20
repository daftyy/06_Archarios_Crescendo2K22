from flask import Flask, render_template, request
import requests
import urllib.parse
import numpy as np
from sklearn import preprocessing


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
    dist_list = []
    time_list = []
    green_list = []
    for i in range(int(alternative_routes)):
        #print(f"time for route {i+1}")
        time_list.append(str(routes['routes'][i]['sections'][0]['summary']['duration']/60))
        #print(routes['routes'][i]['sections'][0]['summary']['duration']/60)
        #print(f"distance for route {i+1}")
        dist_list.append(str(routes['routes'][i]['sections'][0]['summary']['length']/1000))
        green_list.append(greenscore_route(routes['routes'][i]['sections'][0]['summary']['length']/1000, routes['routes'][i]['sections'][0]['summary']['duration']/60, mode))
        #print(routes['routes'][i]['sections'][0]['summary']['length']/1000)
    t1=time_list[0]
    t2=time_list[1]
    t3=time_list[2]
    t4=time_list[3]
    t5=time_list[4]

    d1=dist_list[0]
    d2=dist_list[1]
    d3=dist_list[2]
    d4=dist_list[3]
    d5=dist_list[4]

    green_np = np.array(green_list).reshape(-1,1)
    scaler = preprocessing.MinMaxScaler()
    green_normalized = scaler.fit_transform(green_np)

    print(time_list)
    print(dist_list)
    print(green_list)
    #print(green_normalized)

    return render_template('Home.html', t1=t1, t2=t2, t3=t3, t4=t4, t5=t5, d1=d1, d2=d2, d3=d3, d4=d4, d5=d5)

def getLatLong(address):
    # ONLY WORKS FOR AREA NAME AND CITY (CITY HAS TO BE THERE) OR ENABLE MAPS API FOR GEOCODING (BEST)
    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
    response = requests.get(url).json()
    lat = response[0]["lat"]
    longit = response[0]["lon"]
    return [lat, longit]

def greenscore_route(distance, time, vehicle):
    if vehicle=="car":
        avg_mileage=10
    if vehicle=="bike":
        avg_mileage=15
    if vehicle=="truck":
        avg_mileage=5
    
    greenscore = (distance/time)*avg_mileage
    return str(greenscore)
