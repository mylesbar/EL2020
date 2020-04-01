#Import libraries
import RPi.GPIO as GPIO
import time
import os
import Adafruit_DHT

#Initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(27,GPIO.OUT)
GPIO.setup(26,GPIO.IN)
GPIO.setup(17,GPIO.IN)
#initializations and stuff
ledPin = 27
buttonPin = 26
tempPin = 17
tempSensor = Adafruit_DHT.DHT11

#This function will make the light blink once
def blinkOnce(pin):
        GPIO.output(pin,True)
        time.sleep(0.5)
        GPIO.output(pin,False)
        time.sleep(0.5)
#temp reading
def readF(tempPin):
        humidity, temperature = Adafruit_DHT.read_retry(tempSensor,tempPin)
        temperature = temperature * 9/5.0 +32
        print('temperature:',temperature)
        if humidity is not None and temperature is not None:
        #       temperature = temperature * 9/5.0 +32
                tempFahr = '{0:0.1f}*F'.format(temperature)
        else:
                print("error reading sensor")
        return temperature

#touchy touchy
try:
        while True:
                button_input_state = GPIO.input(26)
                if button_input_state == True:
                        for i in range(5):
                                blinkOnce(ledPin)
                                #print("blink")
                       		#time.sleep(0.2)
				data = readF(tempPin)
				#print('done')
			button_input_state = False
#keyboard exception
except KeyboardInterrupt:
	os.system('clear')
	GPIO.cleanup()
	print("clear")
#Cleanup the GPIO when done
GPIO.cleanup()
