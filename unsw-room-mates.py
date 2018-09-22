#!/usr/bin/python3
from flask import Flask, g, session, request, jsonify, render_template
from unsw-room-mates-backend import *

app = Flask(__name__)

@app.route("/")
def index_route():
    return render_template("index.html")

# API CALLS

# DONE
# Get a list of all buildings by name
@app.route("/buildings/name", methods = ["GET"])
def get_all_building_names_route():
    building_names = get_all_buildings_name()
    return {"data": building_names}

# DONE
# Get a list of all buildings by ID
@app.route("/buildings/id", methods = ["GET"])
def get_all_building_ids_route():
    building_ids = get_all_building_ids()
    return {"data": building_ids}

# Get a list of buildings be number of rooms free at a given time
@app.route("/buildings/free", methods = ["POST"])
def get_buildings_free_route():

    # Get the post data
    data = request.form
    
    # Get the time data
    time_int, day, week = convert_from_epoch(data["epoch_time"])

    # Get buildings sorted by number of free rooms
    free_buildings = get_buildings_free(time_int, day, week)

    return free_buildings

# DONE
# Get a list of all room names in a give building
@app.route("/rooms/<buildingID>/name", methods = ["GET"])
def get_all_room_names_route(buildingID):
    room_names = get_all_room_names(buildingID)
    return {"data": room_names}

# DONE
# Get a list of all room IDs in a give building
@app.route("/rooms/<buildingID>/id", methods = ["GET"])
def get_all_room_ids_route():
    room_ids = get_all_room_ids(buildingID)
    return {"data": room_ids}

# Done
# Get a room's free time from a given building and given time
@app.route("/rooms", methods = ["POST"])
def get_room_route():

    # Get the post data
    data = request.form
    
    buildingID = data["buildingID"]
    roomID     = data["roomID"]

    # Get the time data
    time_int, day, week = convert_from_epoch(data["epoch_time"])

    # Return the free_time array
    return get_room_from_day_week(buildingID, roomID, day, week)