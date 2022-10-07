import time
import RPi.GPIO as GPIO

waterInputPin = 23
waterLedPin = 18
waterLtr = 0

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(waterInputPin, GPIO.IN)
GPIO.setup(waterLedPin, GPIO.OUT)
GPIO.add_event_detect(waterInputPin, GPIO.FALLING)  # add rising edge detection on a channel
#GPIO.add_event_detect(waterInputPin, GPIO.BOTH)
#GPIO.add_event_detect(waterInputPin, GPIO.BOTH)


print("Watersensor goed aangesloten op GPIO 23, pin 16?")


while True:
   if GPIO.input(waterInputPin):
       waterLtr = waterLtr + 1
       print("Water Detect Ltr! ", waterLtr)
        #print("Water Detect  ", waterInt)
        #if waterInt % 2 == 0: #2 pulsen spiegel is 1 liter
        #   global waterLtr 
        #   waterLtr = waterLtr + 1
      


   
"""   
   #if GPIO.input(waterInputPin):
    if GPIO.event_detected(waterInputPin):    
       waterLtr = waterLtr + 1
       print("Water Liters: ", waterLtr)
       GPIO.output(waterLedPin, GPIO.HIGH)
       if (waterLtr >= 1000): #1000 pulsen = 1 M3
                waterM3 = waterM3 + 1
                print("WaterM3: ", waterM3)
    else:
    #   print('Input was LOW')
       GPIO.output(waterLedPin, GPIO.LOW)
       time.sleep(0.5)
    
    #GPIO.wait_for_edge(waterInputPin, GPIO.FALLING) # we wait for the button to be pressed
    #if GPIO.input(waterInputPin, GPIO.HIGH):
        #if pressed:
           #print("Watersensor detect!: ", waterInt)
           #pressed = True
           # waterInt = waterInt + 1
           # GPIO.output(waterLedPin, GPIO.HIGH)
           # print("WaterInt: ", waterInt)
           # if (waterInt >= 10): #Moet 2000 zijn, 1000 pulsen = 1 liter
           #     waterLtr = waterLtr + 1
           #     waterInt = 0
           #     print("WaterLtr: ", waterLtr)
    #else:
     #  pressed = False
      # GPIO.output(waterLedPin, GPIO.LOW)
      # time.sleep(0.1)

#Catch when script is interrupted, cleanup correctly
#try:
    # Main loop
#    while True:
#        print(rc_time(pin_to_circuit))
#except KeyboardInterrupt:
#    pass
#finally:
#    GPIO.cleanup()
"""