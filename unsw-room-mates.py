#!/usr/bin/python3
from flask import Flask, g, session, request, jsonify, render_template
from unsw-room-mates-backend import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/buildings/name", methods = ["GET"])
def get_all_buildings_name():
    return render_template("index.html")

@app.route("/buildings/id", methods = ["GET"])
def get_all_buildings_id():
    return render_template("index.html")

@app.route("/buildings", methods = ["POST"])
def get_building():
    return render_template("index.html")


@app.route("/buildings/free", methods = ["POST"])
def get_buildings_free():
    return render_template("index.html")


@app.route("/rooms/name", methods = ["GET"])
def get_all_rooms_name():
    return render_template("index.html")

@app.route("/rooms/id", methods = ["GET"])
def get_all_rooms_id():
    return render_template("index.html")

@app.route("/rooms", methods = ["POST"])
def get_room():
    return render_template("index.html")