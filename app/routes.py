from app import app
from flask import render_template
from config import GOOGLEMAPS_KEY


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
