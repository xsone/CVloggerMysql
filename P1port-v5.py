""""
" Versie info:
  -------------
  File name: P1port.py
  Werking: zend iedere 24 uur een waarde naar de database MySQL "Energielogger" o.b.v. Timeserver
  (c) Jack Cop 2012-2022
  
  8/6/2022 P1-port + watersensor in deksel
  10/2/2018 probleem met watersensor opgelost


  Codes DSMR voor de slimme meter Landys&Gyr E350 SMR5.0
  0-0:96.1.1.255   Identifier van meter
  1-0:1.8.1.255    Geleverde elektriciteit AAN klant Tarief T1 in 0,001 KWh
  1-0:2.8.1.255    Geleverde elektriciteit DOOR klant Tarief T1 in 0,001 KWh (Zonnepanelen)
  1-0:1.8.2.255    Geleverde elektriciteit AAN klant Tarief T2 in 0,001 KWh
  1-0:2.8.2.255    Geleverde elektriciteit DOOR klant Tarief T2 in 0,001 KWh (Zonnepanelen)
  1-0:1.7.0.255    Actuele elektriciteitsproductie (+P) AAN klant met 1 Watt nauwkeurig (resolutie)
  1-0:2.7.0.255    Actuele elektriciteitsproductie (-P) DOOR klant met 1 Watt nauwkeurig (resolutie)
  0-0:96.7.21.255  Aantal storingen in een van de fasen
  0-0:96.7.9.255   Aantal lange storingen in een van de fasen
  1-0:99:97.0.255  Event logger lange storingen
  1-0:32.32.0.255  Aantal Voltage pieken in L1
  1-0:32.36.0.255  Aantal Voltage dalen in L1
  0-0:96.13.0.255  Text bericht max. 1024 chars


  Voorbeeld bericht via P1 poort
    /XMX5LGBBFG10

    1-3:0.2.8(42)
    0-0:1.0.0(170108161107W)
    0-0:96.1.1(4530303331303033303031363939353135)
    1-0:1.8.1(002074.842*kWh)
    1-0:1.8.2(000881.383*kWh)
    1-0:2.8.1(000010.981*kWh)
    1-0:2.8.2(000028.031*kWh)
    0-0:96.14.0(0001)
    1-0:1.7.0(00.494*kW)
    1-0:2.7.0(00.000*kW)
    0-0:96.7.21(00004)
    0-0:96.7.9(00003)
    1-0:99.97.0(3)(0-0:96.7.19)(160315184219W)(0000000310*s)(160207164837W)(0000000981*s)(151118085623W)(0000502496*s)
    1-0:32.32.0(00000)
    1-0:32.36.0(00000)
    0-0:96.13.1()
    0-0:96.13.0()
    1-0:31.7.0(003*A)
    1-0:21.7.0(00.494*kW)
    1-0:22.7.0(00.000*kW)
    0-1:24.1.0(003)
    0-1:96.1.0(4730303139333430323231313938343135)
    0-1:24.2.1(170108160000W)(01234.000*m3)
    !D3B0

           # 1 - 0: 1.8.1.255 Geleverde elektriciteit AAN klant Tarief T1(LT) in 0, 001 KWh
        # 1 - 0: 2.8.1.255 Geleverde elektriciteit DOOR klant Tarief T1(LT) in 0, 001 KWh(Zonnepanelen)
        # 1 - 0: 1.8.2.255 Geleverde elektriciteit AAN klant Tarief T2(HT) in 0, 001 KWh
        # 1 - 0: 2.8.2.255 Geleverde elektriciteit DOOR klant Tarief T2(HT) in 0, 001 KWh(Zonnepanelen)
        # 1 - 0: 1.7.0.255 Actuele elektriciteitsproductie(+P) AAN klant met 1 Watt nauwkeurig(resolutie)
        # 1 - 0: 2.7.0.255 Actuele elektriciteitsproductie(-P) DOOR klant met 1 Watt nauwkeurig(resolutie)
        # 0 - 1: 24.2.1.255 Gas verbruikt in M3

        # Elektriciteit Laag tarief verbuikt
        # substring nummer  0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20
        # substring(0, 9)   1 - 0 : 1 . 8 . 1 5 0  .  3  3
        # substring(0, 9)   1 - 0 : 1 . 7 . 0 0 .  3  5
        # act.verbruikt     1 - 0 : 1 . 7 . 0 0 0  .  4  9  4
        # act.gelevert      1 - 0 : 2 . 7 . 0 0 0  .  0  0  0
"""
import serial
import time
import mysql.connector
import re
import RPi.GPIO as GPIO
import requests

print("DSMR 5.0 P1 uitlezer", versie)
print("DSMR 5.0 P1 uitlezer", versie)
print("Control-C om te stoppen")
print("Energie-logger gestart...")
print("Tijdstip: ", time.asctime(time.localtime()))

#Sensor Pins
# waterLedPin =  4
# waterInputPin = 2

#Inlezen van Slimme Meterdata naar String
inputString = []

global gas #Meter Gas verbruikt

#Waterverbruik
waterInputPin = 23
waterInt = 0
waterLtr = 0

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
GPIO.add_event_detect(waterInputPin, GPIO.RISING, callback = waterDetect, bouncetime = 5)  # add rising edge detection on a channel

#Waarden Slimme Meter P1-poort
elecLTverbruik = 0 #Meter laag tarief Electriciteit verbruikt
elecLTgeleverd = 0  #Meter laag tarief Electriciteit opgewekt
elecHTverbruik = 0 #Meter hoog tarief Electriciteit verbruikt
elecHTgeleverd = 0  #Meter hoog tarief Electriciteit opgewekt
elecACTverbruik = 0 #Meter laag tarief Electriciteit verbruikt
elecACTgeleverd = 0 #Meter laag tarief Electriciteit opgewekt

elecTOTverbruik = 0 #Meter totaal laag + hoog tarief Electriciteit verbruikt
elecTOTgeleverd = 0  #Meter totaal laag + hoog tarief Electriciteit opgewekt

#Test o.b.v. tijdsinterval definitieve versie met NTP-time via ethernet
postingInterval = 10 # 10 sec.
#postingInterval = 300 # 5 min.
lastConnectionTime = time.time()

# Set COM port config
ser = serial.Serial()
ser.baudrate = 115200
ser.bytesize = serial.EIGHTBITS
ser.parity = serial.PARITY_NONE
ser.stopbits = serial.STOPBITS_ONE
ser.xonxoff = 0
ser.rtscts = 0
ser.timeout = 20
ser.port = "/dev/ttyUSB0"

# Uitlezen Slimme Meter via P1 - poort en bericht decoderen
def decodeTelegramSql():
    ser.open()
    checksum = False
    while not checksum:
        inputString = ser.readline()  # leest een seriele lijn in
        inputString = inputString.decode('ascii').strip()  # stript spaties en blanke regels
        # print(inputString)
      
        if re.match('(?=1-0:1.8.1)', inputString):
           global elecLTverbruik
           elecLTverbruik = inputString[10:16]
           print("elecLTverbruik (kWh): ", elecLTverbruik)
        if re.match('(?=1-0:2.8.1)', inputString):
           global elecLTgeleverd 
           elecLTgeleverd = inputString[10:16]
           print("elecLTgeleverd (kWh): ", elecLTgeleverd)

        if re.match('(?=1-0:1.8.2)', inputString):
           global elecHTverbruik
           elecHTverbruik = inputString[10:16]
           print("elecHTverbruik (kWh): ", elecHTverbruik)
        if re.match('(?=1-0:2.8.2)', inputString):
           global elecHTgeleverd
           elecHTgeleverd = inputString[10:16]
           print("elecHTgeleverd (kWh): ", elecHTgeleverd)

        if re.match('(?=1-0:1.7.0)', inputString):
           global elecACTverbruik
           elecACTverbruik = int(float(inputString[10:16])*1000)
           print("elecACTverbruik (W): ", elecACTverbruik)




        if re.match('(?=1-0:2.7.0)', inputString):
           global elecACTgeleverd
           elecACTgeleverd = int(float(inputString[10:16])*1000)
           print("elecACTgeleverd (W): ", elecACTgeleverd)
           
        if re.match('(?=0-1:24.2.1)', inputString):
           global gas
           gas = inputString[26:31]
           print("gas verbruik (M3): ", gas)

        # Check wanneer het uitroepteken ontvangen wordt (einde telegram)
        if re.match('(?=!)', inputString):
           checksum = True
           ser.close()
    
    #Optellen totaal elec verbruik en geleverd
    elecTOTverbruik = int(elecLTverbruik) + int(elecHTverbruik)
    print("elecTOTverbruik (kWh): ", elecTOTverbruik)
    elecTOTgeleverd = int(elecLTgeleverd) + int(elecHTgeleverd)
    print("elecTOTgeleverd (kWh): ", elecTOTgeleverd)
    
    #Uitlezen watersensor en berekenen totaal elec HT+LT
    #print("water verbruik (ltr): ", waterLtr)
       
    #Schrijf naar MySql database
    db_connection = mysql.connector.connect(
        host='192.168.178.20',
        port=3307,
        user='Arduino',
        passwd="#@Xymox123",
        db='Energielogger',
    )
    print(db_connection)
    db_cursor = db_connection.cursor()
    db_cursor.execute("INSERT INTO energiemeter (gas, waterLtr, elecLTverbruik, elecLTgeleverd, elecHTverbruik, elecHTgeleverd, elecTOTverbruik, elecTOTgeleverd, elecACTverbruik, elecACTgeleverd) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                                (gas, waterLtr, elecLTverbruik, elecLTgeleverd, elecHTverbruik, elecHTgeleverd, elecTOTverbruik, elecTOTgeleverd, elecACTverbruik, elecACTgeleverd))
    db_connection.commit()


#Dit is de oneindige loop()
while True:
    if ((time.time() - lastConnectionTime) >= postingInterval):
       lastConnectionTime = time.time()
       print("Tijdstip: ", time.asctime(time.localtime()))
       print("Loggen sec: ", time.localtime().tm_sec)
       decodeTelegramSql() #Inlezen en decoderen data via P1-port
       print("water verbruik (ltr): ", waterLtr)              
       
