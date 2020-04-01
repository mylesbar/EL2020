#Import libraries
import RPi.GPIO as GPIO
import time
import os

#Initialize the GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17,GPIO.OUT)
GPIO.setup(26,GPIO.IN)
GPIO.setup(21,GPIO.IN)

#This function will make the light blink once
def blinkOnce(pin):
        GPIO.output(pin,True)
        time.sleep(0.5)
        GPIO.output(pin,False)
        time.sleep(0.5)

#Call the blinkOnce function above in a loop
#for i in range(100):
#       blinkOnce(17)

#touchy touchy
try:
        while True:
                input_state = GPIO.input(26)
                temp_state = GPIO.input(21)
                if input_state == True:
                        for i in range(5):
                                blinkOnce(17)
                                print("blink")
                        time.sleep(0.2)

#keyboard exception
except KeyboardInterrupt:
	os.system('clear')
	GPIO.cleanup()
	print("clear")

#Cleanup the GPIO when done
GPIO.cleanup()

