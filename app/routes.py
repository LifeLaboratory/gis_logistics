import requests
import json
from app import app
from flask import render_template
from config import GOOGLEMAPS_KEY, HOST


@app.route('/route/all')
def route_all():
    r = requests.get('{}/route/all'.format(HOST))
    roads = json.loads(r.text)
    start_x = []
    start_y = []
    end_x = []
    end_y = []
    rating = []

    for r in range(10):
        start_x.append(roads[r].get('start_x'))
        start_y.append(roads[r].get('start_y'))
        end_x.append(roads[r].get('end_x'))
        end_y.append(roads[r].get('end_y'))
        rating.append(roads[r].get('Индикация'))

    return render_template("map.html",
                           start_x=start_x,
                           start_y=start_y,
                           end_x=end_x,
                           end_y=end_y,
                           lat=55.020790,
                           lng=82.923879,
                           rating=rating,
                           GOOGLEMAPS_KEY=GOOGLEMAPS_KEY
                           )


@app.route('/route/<int:id_route>')
def route_one(id_route):
    r = requests.get('{}/route/{}'.format(HOST, id_route))
    road = json.loads(r.text)
    return render_template("driver.html",
                           start=road.get('start'),
                           end=road.get('end'),
                           waypoints_x=road.get('waypoints_x'),
                           waypoints_y=road.get('waypoints_y'),
                           lat=55.020790,
                           lng=82.923879,
                           GOOGLEMAPS_KEY=GOOGLEMAPS_KEY
                           )
