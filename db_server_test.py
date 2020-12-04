import time
import sqlite3 as lite
import json

#const. for max time before email is sent to charging user
DISCONNECT_TIME = int(4 * 60 * 60) # 4 hours

current_time = int(time.time())
print(time.strftime('%Y-%m-%d %T', time.localtime(current_time)) )
#print(current_time[4:])
#print(type(current_time))
print(time.time() )
#if (int(time.time()) > 1602071734):
#    print("works")
#else:
#    print("doesn't work")
#input()

con = None
#path = "/home/pi/Documents/sql_databases/new_user_table.sqlite3"
path = "/mnt/dav/Data/usertable.sqlite3"
path_local = "/media/DATABASE/usertable.sqlite3"

con = lite.connect(path)


#con = lite.connect(path)
cur = con.cursor()

#UserId = "66 FB 67 D9"
UserId = "97 2D 39 5D" #real user in all tables

#PendingCharger = data.get("Charger")
#StartTime = data.get("StartTime")

cur.execute("SELECT name, rowid FROM users WHERE uidTag = ? ", (UserId,) )
dataRef = cur.fetchone()
print(dataRef)

cur.execute("SELECT carId FROM car_of_user WHERE userId = ? ", (dataRef[1],) )
dataCar = cur.fetchone()
print(dataCar)

cur.execute("SELECT brand || ' ' || type FROM cars WHERE id = ? ", (dataCar[0],) )
dataCar = cur.fetchone()
print(dataCar)
#cur.execute("SELECT name, uidTag, LastStartOrStop, socketId FROM users WHERE uidTag=? LIMIT 1", (UserId,))

# cur.execute("SELECT email, rowid FROM users WHERE LastStartOrStop >= ? AND email <> '' AND mailed < 1 AND socketId > 0", ((str(int(time.time()) - DISCONNECT_TIME)),) )
# dataRef = cur.fetchall()
# print(dataRef)
# for element in dataRef:
#     print(element)
#     cur.execute("UPDATE users SET mailed=? WHERE rowid=?", (1, element[1]))
# 
# cur.execute("UPDATE users SET mailed=0 WHERE LastStartOrStop > ? AND mailed > 0 AND socketId IS NULL", ((str(int(time.time()) - DISCONNECT_TIME)),) ) 
cur.execute("SELECT socketId FROM users WHERE socketId IS NOT NULL")
data = cur.fetchall()    
print(data)
print(len(data))

con.commit()
#print(dataRef[0][0])

#(str(int(time.time()) - DISCONNECT_TIME))

# cur.execute("UPDATE users SET socketId=?, LastStartOrStop=? WHERE uidTag=?", (1, current_time, UserId))
#  
# cur.execute("SELECT name, uidTag, LastStartOrStop, socketId FROM users WHERE uidTag=? LIMIT 1", (UserId,))
# dataRef = cur.fetchone()
# 
# con.commit()
# 
# print(dataRef)
#  
# #dataRef = cur.fetchone()
# #print(dataRef)
# 
# f = open("/mnt/dav/Data/textfile.txt", "w")
# f.write("Now the file has more content+!\n")
# f.close()
# 
# #open and read the file after the appending:
# f = open("/mnt/dav/Data/textfile.txt", "r")
# print(f.read())
# f.close()

con.close()