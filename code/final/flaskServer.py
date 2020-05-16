#!/usr/bin/python

#THis script creates a Flask server, and serves the index.html out of the templates folder.
#It also creates an app route to be called via ajax from javascript in the index.html to query
#the database that is being written to by tempReader.py, and return the data as a json object.

#This was written for Joshua Simons's Embedded Linux Class at SUNY New Paltz 2020
#And is licenses under the MIT Software License

#Import libraries as needed
from flask import Flask, render_template, jsonify, Response, request
from flask import *
from werkzeug.utils import secure_filename
import sqlite3 as sql
import json
import RPi.GPIO as GPIO
import time
import os

#Globals
#Flask
UPLOAD_FOLDER ='/log'
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.isdir(UPLOAD_FOLDER):
	os.mkdir(UPLOAD_FOLDER)

#GPIO LED stuff

@app.route("/")
def index():
#	return('in server')
	return render_template('index.html')

@app.route("/sqlData")

def chartData():
	con = sql.connect('log/dataLog.db')
	cur = con.cursor()
	con.row_factory = sql.Row
	cur.execute("SELECT Timestamp, Temperature FROM dataLog WHERE Temperature > 0") #renamed variables to match script
	dataset = cur.fetchall()
	print (dataset)
	chartData = []

	for row in dataset:
		chartData.append({"Date": row[0], "Temperature": float(   row[1][:-2]      )})

	return Response(json.dumps(chartData), mimetype='application/json')

@app.route("/sqlHumidData")
def humidData():
	con = sql.connect('log/dataLog.db')
	cur = con.cursor()
	con.row_factory = sql.Row

	cur.execute("SELECT Timestamp, Humidity FROM dataLog WHERE Humidity > 0")
	humidSet = cur.fetchall()
	humidityData = []
	print(humidSet)

	for row in humidSet:
		humidityData.append({"Date": row[0], "Humidity": float(   row[1][:-2]      )})

	return Response(json.dumps(humidityData), mimetype='application/json')

@app.route("/sqlPressureData")
def pressureData():
	con = sql.connect('log/dataLog.db')
	cur = con.cursor()
	con.row_factory = sql.Row

	cur.execute("SELECT Timestamp, Pressure FROM dataLog WHere Pressure > 0")
	pressureSet = cur.fetchall()
	pressureData = []
	print(pressureSet)

	for row in pressureSet:
		pressureData.append({"Date": row[0], "Pressure": float(   row[1][:-2]      )})

	return Response(json.dumps(pressureData), mimetype='application/json')


@app.route('/button', methods = ['GET', 'POST'])

def button():
	if request.method == 'POST':
		f = request.files['../log/TrashBeat.mid']
		f.save(secure_filename(f.filename))
	return 'file uploaded successfuly'

#send midifile to server for playback
	filename = 'TrashBeat.mid'
	print('sending')
	return send_from_directory(app.config['UPLOAD_FOLDER'],filename)

#	return Response()


if __name__ == "__main__":
	app.run(host='0.0.0.0',debug = True)
