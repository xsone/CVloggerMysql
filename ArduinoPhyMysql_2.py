import mysql.connector as mysql

db = mysql.connect(
    host = "localhost",
    user = "root",
    passwd = "#@Xymox123",
    database = "Energielogger"
)

cursor = db.cursor()
## defining the Query
query ="INSERT INTO students(GAS, WATER, ElecLTverbruikt, ElecLTgeleverd) VALUES (%s, %s, %s, %s)"
##cursor.execute("INSERT INTO energiemeter(GAS,WATER,ElecLTverbruikt,ElecLTgeleverd) VALUES(1.1, 2.2, 3.3, 4.4)")
## There is no need to insert the value of rollno 
## because in our table rollno is autoincremented #started from 1
## storing values in a variable
values = ("1.1", "2.2", "3.3", "4.4")

## executing the query with values
cursor.execute(query, values)

## to make final output we have to run 
## the 'commit()' method of the database object
db.commit()

print(cursor.rowcount, "record inserted")