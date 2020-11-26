import time
import sqlite3 as lite
import json

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
path = "/run/user/1000/gvfs/dav:host=192.168.110.5,ssl=false,user=CristianBatog,prefix=%2FHANWattsFolder/Data/new_user_table.sqlite3"

con = lite.connect(path)
cur = con.cursor()
#data = json.loads(message.payload)
    #index = []
    #for i in range(len(data)):
    #    if (data[i] == ';'):
    #       index.append(i)
UserId = "No ID"

#PendingCharger = data.get("Charger")
#StartTime = data.get("StartTime")
    
cur.execute("SELECT name, uidTag, LastStartOrStop, socketId FROM users WHERE uidTag=? LIMIT 1", (UserId,))
dataRef = cur.fetchone()
print(dataRef)