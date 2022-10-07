import time
import RPi.GPIO as GPIO


#Waterverbruik
waterInputPin = 23
waterInt = 0
waterLtr = 0
sensorState = False

def waterDetect(waterInputPin):
    #sleep(0.005)
    if GPIO.input(waterInputPin):
        global waterInt
        waterInt = waterInt + 1
        print("Water Detect Int! ", waterInt)
        if waterInt % 2 == 0: #2 pulsen spiegel is 1 liter
           global waterLtr 
           waterLtr = waterLtr + 1
           print("Water Detect Ltr! ", waterLtr)
        
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(waterInputPin, GPIO.IN)
#GPIO.add_event_detect(waterInputPin, GPIO.FALLING, callback = waterDetect, bouncetime = 100)  # add rising edge detection on a channel

print("Wachten op waterDetect...")

while True:
    if((GPIO.input(waterInputPin) == False) and sensorState == True):
        sensorState = False
        waterLtr = waterLtr + 1
        print("Water Ltr: ", waterLtr)
    if((GPIO.input(waterInputPin) == True) and sensorState == False):
        sensorState = True
    time.sleep(1)