
#Import Libraries we will be using
import RPi.GPIO as GPIO
import Adafruit_DHT
import time
import os
import sqlite3 as sql
import sys

#Assign GPIO pins
redPin = 21
tempPin = 17
buttonPin = 26

#Temp and Humidity Sensor
tempSensor = Adafruit_DHT.DHT11

#LED Variables--------------------------------------------------------
#Duration of each Blink
blinkDur = 1
#Number of times to Blink the LED
blinkTime = 5
#---------------------------------------------------------------------


#Initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(redPin,GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(tempPin, GPIO.IN)

print('Program Start!')
print('------------------------------')
def oneBlink(pin):
	GPIO.output(pin,True)
	time.sleep(blinkDur)
	GPIO.output(pin,False)
	time.sleep(blinkDur)

def readF(tempPin):
	humidity, temperature = Adafruit_DHT.read_retry(tempSensor, tempPin)
	temperature = temperature * 9/5.0 +32
	if humidity is not None and temperature is not None:
		tempFahr = '{0:0.1f}*F'.format(temperature)
	else:
		print('Error Reading Sensor')
	return tempFahr

def readH(tempPin):
        temperature,humidity = Adafruit_DHT.read_retry(tempSensor, tempPin)
        temperature = temperature * 9/5.0 +32
        if humidity is not None and temperature is not None:
                humid = 'Humidity: {}%'.format(humidity)
        else:
                print('Error Reading Sensor')
        return humid

try:

	con = sql.connect('../log/tempLog.db')
	cur = con.cursor()
	cur.execute( '''
	 CREATE TABLE IF NOT EXISTS "tempLog" ( 
	"timestamp" TEXT,
	"temp" TEXT,
	"humid" TEXTL
		)
	 ''') #renamed" sensor data" from tempLog SQL branch
	with open("log60s.csv","a") as log:
		while True:

#run logging every 60s-------------------------------------------------------------
			starttime = time.time() 
			time.sleep(60.0 - ((time.time()-starttime) % 60.0) )
#blink when 60s is over and record temp and humidity--------------------------------
			oneBlink(redPin)
			dataF = readF(tempPin)
			dataH = readH(tempPin)
			print (dataF,dataH)
#stringify for db-------------------------------------------------------------------
			date_insert = "{0}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"))
			temp_insert = str(dataF)
			humid_insert= str(dataH)
#write to csv-----------------------------------------------------------------------
             #           log.write("{0},{1},{2}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),str(dataF),str(dataH)))
             #           print("wrote to CSV")
#write to db------------------------------------------------------------------------
			cur.execute('''INSERT INTO tempLog(timestamp,temp,humid) VALUES (?,?,?)''',(date_insert,temp_insert,humid_insert))
			con.commit()

			print("wrote to database")
			print('-----------------------------------------')

except sql.Error, e:
	print"Error %s:" %e.args[0]
	sys.exit(1)

except KeyboardInterrupt:
	os.system('clear')
	con.close()
	print('Thanks for Blinking and Thinking!')
	GPIO.cleanup()
