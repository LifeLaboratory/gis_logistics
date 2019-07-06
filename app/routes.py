from app import app
from flask import render_template
from config import GOOGLEMAPS_KEY
import json


@app.route('/', methods=['GET'])
def index():
    start = '55.008588,82.9422249'
    end = '55.0184809,82.9269283'
    waypoints_x = [55.019960]
    waypoints_y = [82.936605]
    return render_template("index.html",
                           start=start,
                           end=end,
                           waypoints_x=waypoints_x,
                           waypoints_y=waypoints_y,
                           lat=55.020790,
                           lng=82.923879,
                           GOOGLEMAPS_KEY=GOOGLEMAPS_KEY
                           )


@app.route('/map', methods=['GET'])
def map():
    start_x = [55.008588, 55.004583, 55.003973, 55.023319, 55.011743]
    start_y = [82.9422249, 82.945431, 82.943901, 82.945089, 82.935623]
    end_x = [55.0184809, 55.004621, 55.019223, 55.011126, 54.998835]
    end_y = [82.9269283, 82.973148, 82.938468, 82.976636, 82.956684]
    waypoints_x = [[55.019960], [55.005725], [55.013949], [55.018689], [55.001317]]
    waypoints_y = [[82.936605], [82.970770], [82.950834], [82.972365], [82.950325]]
    rating = [5, 1, 2, 3, 4]

    return render_template("map.html",
                           start_x=start_x,
                           start_y=start_y,
                           end_x=end_x,
                           end_y=end_y,
                           waypoints_x=waypoints_x,
                           waypoints_y=waypoints_y,
                           lat=55.020790,
                           lng=82.923879,
                           rating=rating,
                           GOOGLEMAPS_KEY=GOOGLEMAPS_KEY
                           )