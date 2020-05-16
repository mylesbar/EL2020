#testSense.py
#Purpose of this program is to test the functionality of the sensors

#Libraries used
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import os
import csv
import sqlite3 as sql
import sys
import Adafruit_BMP.BMP085 as BMP085

#Initialize hardware
tempSensor = Adafruit_DHT.DHT11
tempPin = 12

bmp = BMP085.BMP085()

#Initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(tempPin, GPIO.IN)

#read Temp into DHT11
def readF(tempPin):
	humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
	temperature = temperature * 9/5.0 +32
	if humidity is not None and temperature is not None:
		tempFahr = '{0:0.1f}'.format(temperature)
	else:
		print('Error Reading Sensor')
	return tempFahr

#read Humid into DHT11
def readH(tempPin):
        humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
        temperature = temperature * 9/5.0 +32
        if humidity is not None and temperature is not None:
                humid = '{0:0.1f}'.format(humidity)
        else:
                print('Error Reading Sensor')
        return humid


#Reading Loop
try:
	i = 0
	print('Program Start')
	while True:

		bmpPressure = bmp.read_pressure()
		tempOut = readF(tempPin)
		humidOut = readH(tempPin)

		print('*********')
		print('Cycle ' + str(i) )
		print('Temp = ' +  tempOut+' F' )
                print('Humidity =  %.02f ' % float(humidOut) )
		print("Pressure from bmp: %.2f hPa" % (bmpPressure/100) )
		print('*********')

		i+=1

except KeyboardInterrupt:
#	os.system('clear')
	print('Program Terminated')
	GPIO.cleanup()

GPIO.cleanup()
