import mysql.connector
import json
import requests
import time
import schedule

postingInterval = 10
lastConnectionTime = time.time()
cvStatus = 0
boilerStatus = 0
retourTemp = 0
kamerTemp = 0
kamerHum = 0


def writeMysql():   #Schrijf naar mySQL DB
  db_connection = mysql.connector.connect(
        host='192.168.178.20',
        port=3307,
        user='Arduino',
        passwd="#@Xymox123",
        db='Energielogger',
    )
  print(db_connection)
  db_cursor = db_connection.cursor()
  db_cursor.execute("INSERT INTO cvlogger (cvStatus, boilerStatus, retourTemp, kamerTemp, kamerHum) VALUES(%s, %s, %s, %s, %s)", (cvStatus, boilerStatus, retourTemp, kamerTemp, kamerHum))
  db_connection.commit()
  db_cursor.execute("SELECT * FROM cvlogger")
  for row in db_cursor.fetchall():
      print(row)

print("CV-logger gestart...")

while True:
    if ((time.time() - lastConnectionTime) >= postingInterval):
       lastConnectionTime = time.time()
       print("Loggen sec: ", time.localtime().tm_sec)

       #cvStatus
       response = requests.get('http://192.168.178.144:8080/bridge/zones/zn1/status')
       if response.status_code == 200:
          cvStatusTxt = response.json().get('value')
          print('CVstatusTxt: ', cvStatusTxt)
       if cvStatusTxt == "idle" and cvStatus == 1:
          cvStatus = 0
          print('CV gaat UIT')
          writeMysql()
       if cvStatusTxt == "heat request" and cvStatus == 0:
          cvStatus = 1
          print('CV gaat AAN')
          writeMysql()
       print("CVstatus: ", cvStatus)


       #boilerStatus
       response = requests.get('http://192.168.178.144:8080/bridge/gateway/ui/icons')
       if response.status_code == 200:
          boilerStatusTxt = response.json().get('value')
          print('BoilerStatusTxt: ', boilerStatusTxt)
       if boilerStatusTxt == ['', '', '', ''] and boilerStatus == 1:
          boilerStatus = 0
          print('Boiler gaat UIT')
          writeMysql()
       if boilerStatusTxt == ['', 'dhw on', '', ''] and boilerStatus == 0:
          boilerStatus = 1
          print('Boiler gaat AAN')
          writeMysql()
       print("BoilerStatus ", boilerStatus)

       #retourTemp
       response = requests.get("http://192.168.178.144:8080/bridge//heatSources/returnTemperature");
       if response.status_code == 200:
          retourTemp = response.json().get('value')
          print('Retour Temp: ', retourTemp)

       #kamerTemp
       response = requests.get("http://192.168.178.144:8080/bridge/system/sensors/temperatures/indoorAirDigital");
       if response.status_code == 200:
          kamerTemp = response.json().get('value')
          print('Kamer Temp: ', kamerTemp)

       #kamerHum
       response = requests.get("http://192.168.178.144:8080/bridge/system/sensors/humidity/indoor_h1");
       if response.status_code == 200:
          kamerHum = response.json().get('value')
          print('Kamer Hum: ', kamerHum)
