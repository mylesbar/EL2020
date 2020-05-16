#testLog.py
#Purpose of this program is to test the data Logging

#Libraries used
import RPi.GPIO as GPIO
import Adafruit_DHT
import time as clk
import os
import csv
import sqlite3 as sql
import sys
import Adafruit_BMP.BMP085 as BMP085
from midiutil import *
import pandas #error importing into python 2.7
import random
import datetime
import math

#Initialize hardware
tempSensor = Adafruit_DHT.DHT11
tempPin = 12

bmp = BMP085.BMP085()

#Initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(tempPin, GPIO.IN)


#Initialize Midi Writing Variables
colnames = ['Temperature' , 'Humidity','Pressure','Timestamp']

tracks = [1,2,3] #midi track
channel = 0 #channel for midi writing

time = 0 #cursor for beat track
duration = 1 #duration of each note
tempo = 60 #BPM

volume = 95

#read Temp into DHT11
def readF(tempPin):
	humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
	temperature = temperature * 9/5.0 +32
	if humidity is not None and temperature is not None:
		tempFahr = '{0:0.2f}'.format(temperature)
	else:
		print('Error Reading Sensor')
	return tempFahr

#read Humid into DHT11
def readH(tempPin):
        humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
        temperature = temperature * 9/5.0 +32
        if humidity is not None and temperature is not None:
                humid = '{0:0.2f}'.format(humidity)
        else:
                print('Error Reading Sensor')
        return humid


#Reading Loop
try:
	i = 1
	print('Connecting to Database')

	con = sql.connect('dataLog.db')
	cur = con.cursor()

	cur.execute( '''
		CREATE TABLE IF NOT EXISTS "dataLog" (
		"Temperature" TEXT,
		"Humidity" TEXT,
		"Pressure" TEXT,
		"Timestamp" TEXTL
			)
		''')
	print('Connected')

	print("Opening CSV file")
	with open("dataLog.csv","w") as log:
		writer = csv.writer(log)
		writer.writerow(["Temperature  ","Humidity   " ,"Barometric Pressure   ","Timestamp   "])

		print("CSV opened")
		print("Program Start")
		while True:

			bmpPressure = bmp.read_pressure()
			tempOut = readF(tempPin)
			humidOut = readH(tempPin)

			print('*********')
			print('Cycle ' + str(i) )
			print('')
			print('Temp = ' +  tempOut+' F' )
			print('Humidity =  %.02f ' % float(humidOut) )
			print("Pressure from bmp: %.2f hPa" % (bmpPressure/100) )


			timeOut = "{0}\n".format(clk.strftime("%Y-%m-%d %H:%M:%S"))
			print('*********')
			print("Writing to CSV")
			log.write("{0},{1},{2},{3}\n".format( str(tempOut) , str(humidOut), str(bmpPressure) , timeOut  ) )
			print("Successful write to CSV")


			print("writing to db")
			cur.execute(''' INSERT INTO dataLog(Temperature,Humidity,Pressure,Timestamp) VALUES (?,?,?,?)''',
			(str(tempOut) , str(humidOut), str(bmpPressure) ,"{0}\n".format(clk.strftime("%Y-%m-%d %H:%M:%S") ) )   )
			con.commit()
			print("successful write to db")

			print('*********')

			i+=1

except KeyboardInterrupt:
	print("*****************************")
	print("Writing to MID file")

	#initialize MIDI track on program termination
	MyMidi = MIDIFile(4) #3 track file

	#set tempo of tracks to equal tempo
	MyMidi.addTempo(tracks[0],time,tempo)
	MyMidi.addTempo(tracks[1],time,tempo)
	MyMidi.addTempo(tracks[2],time,tempo)

	#formatting for transcription --> getting rid of headers
	data = pandas.read_csv("dataLog.csv", names=colnames)

	tempList 	= data.Temperature.tolist()
	tempList.pop(0)
	print('temperature: ' + str(tempList))

	humidList 	= data.Humidity.tolist()
	humidList.pop(0)
	print('humidity: '+ str(humidList) )

	pressureList 	= data.Pressure.tolist()
	pressureList.pop(0)
	print('pressure '+ str(pressureList) )

	timeList 	= data.Timestamp.tolist() #unused lmao

	print('********************************************************')
	#Converted Temp to Kelvin, used the modulo operator to limit between 0-127. Added nonce for variety
	j = 0
	while j < len(tempList):
		tempList[j] =  int(int( (float(tempList[j]) + 459.67 ) * float(5/9) + random.randint(0,2) )%127)
		j+=1
	print('temperature in kelvin: '+ str(tempList) )

	#normalize pressure to value  between 0-127 and added a "nonce" with a value between 1 and 10
	j = 0
	while j < len(pressureList):
		pressureList[j] = int( ( float(pressureList[j])%127 ) + random.randint(0,10) )
		j+=1
	print('normalized pressure: '+ str(pressureList) )

	#Add to Midi Track on program termination
	for num, pitch  in enumerate(tempList):
		MyMidi.addNote(tracks[0], channel, math.floor(float(pitch)), time + num, duration, volume)

	for nums, pitch  in enumerate(humidList):
		MyMidi.addNote(tracks[1], channel, math.floor(float(pitch)), time + nums, duration, volume)

	for numz, pitch  in enumerate(pressureList):
		#randomizedPitch = (float(pitch)%127) + random.randint(0,10)
		MyMidi.addNote(tracks[2], channel, math.floor(float(pitch)), time + numz, duration, volume)

	with open("TrashBeat.mid","wb") as outFile:
		MyMidi.writeFile(outFile)

	print("Sucessfully Wrote Your Trash Ass Beat.\n You should be ashamed of yourself.")
	print('Program Terminated')
#	GPIO.cleanup()

GPIO.cleanup()
