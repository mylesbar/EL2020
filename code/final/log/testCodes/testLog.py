#testLog.py
#Purpose of this program is to test the data Logging

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
		"Barrometric_Pressure" TEXT,
		"Time_Recorded" TEXTL
			)
		''')
	print('Connected')

	print("Opening CSV file")
	with open("dataLog.csv","w") as log:
		writer = csv.writer(log)
		writer.writerow(["Temperature  ","Humidity   " ,"Barometric Pressure   ","Time Recorded   "])

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


			print("Writing to CSV")
			log.write("{0},{1},{2},{3}\n".format( str(tempOut) , str(humidOut), str(bmpPressure) ,time.strftime("%Y-%m-%d %H:%M:%S")  ) )
			print("Successful write to CSV")


			print("writing to db")
			cur.execute(''' INSERT INTO dataLog(Temperature,Humidity,Barrometric_Pressure,Time_Recorded) VALUES (?,?,?,?)''',
			(str(tempOut) , str(humidOut), str(bmpPressure) ,time.strftime("%Y-%m-%d %H:%M:%S") )   )
			con.commit()
			print("successful write to db")

			print('*********')

			i+=1

except KeyboardInterrupt:
#	os.system('clear')
	print('Program Terminated')
	GPIO.cleanup()

GPIO.cleanup()
