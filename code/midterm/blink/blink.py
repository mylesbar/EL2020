#Import libraries
import RPi.GPIO as GPIO
import time
import os

#Initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.IN)
GPIO.setup(21,GPIO.OUT)

#This function will make the light blink once
def blinkOnce(pin):
	GPIO.output(pin,True)
	time.sleep(0.5)
	GPIO.output(pin,False)
	time.sleep(0.5)

#Call the blinkOnce function above in a loop
while True:
	try:
		input_state = GPIO.input(26)
		if input_state == True:
			for i in range(5): #changed for brevity and debug
				blinkOnce(21)
				print('blinking')

#keyboard exception
	except KeyboardInterrupt:
		os.system('clear')
		GPIO.cleanup()
		print("clear")

#Cleanup the GPIO when done
GPIO.cleanup()

