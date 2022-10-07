import serial 
import MySQLdb
import time

dbConn = MySQLdb.connect("localhost","root","#@Xymox123","Energielogger") or die ("could not connect to database")
#open a cursor to the database
cursor = dbConn.cursor()

#device = 'COM18' #this will have to be changed to the serial port you are using
#try:
#  print "Trying...",device 
#  arduino = serial.Serial(device, 9600) 
#except: 
#  print "Failed to connect on",device    

while True:
    try:
      time.sleep(2)
      #data = arduino.readline()  #read the data from the arduino
      #print data
      #pieces = data.split(" ")  #split the data by the tab
      #Here we are going to insert the data into the Database
      try:
        cursor.execute("INSERT INTO energiemeter (humidity,temperature) VALUES (%s,%s)", (pieces[0],pieces[1]))
	#cursor.execute("INSERT INTO energiemeter(GAS,WATER,ElecLTverbruikt,ElecLTgeleverd) VALUES(1.1, 2.2, 3.3, 4.4)")
		#query = "INSERT INTO energiemeter(GAS,WATER,ElecLTverbruikt,ElecLTgeleverd) VALUES(%s, %s, %s, %s)"
		#values = ("1.1","2.2","3.3","4.4")
		#cursor.execute(query, values)
		
		dbConn.commit() #commit the insert
        cursor.close()  #close the cursor
      except MySQLdb.IntegrityError:
        print "failed to insert data"
#      finally:
#        cursor.close()  #close just incase it failed
    except:
      print "Failed to get data from Arduino!"

            
            


  