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
path = "/home/pi/Documents/sql_databases/new_user_table.sqlite3"
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
#print(dataRef[3])
#print(type(dataRef[3]))

if dataRef is None:
    print("compare works")
else:
    print("can't compare")

socketId = 6
cur.execute("SELECT socketId FROM users WHERE socketId=? LIMIT 1", (socketId,))    
socketFree =  cur.fetchone()
if socketFree is not None:
    socketFree = socketFree[0]
print(socketFree)
print(type(socketFree))
if socketFree == socketId:
    print("socket compare works")
else:
    print("socket can't compare")

data = json.loads( "{\"UserId\":\"28 b3 cx\",\"t2\":1234,\"t3\":1234.5,\"t4\":true,\"t5\":false,\"t6\":null, \"t7\" : \"\\\"quoted\\\"\" } ")
UserId = str(data.get("UserId")).upper()  
print(UserId)

x = ('UserId', 'Charger', 'StartTime')
y = "default"

#thisdict = dict.fromkeys(x, y)
newdict = {'UserId': "BB 77 E3 59", 'Charger': 2, 'StartTime': 1603900707}

print(json.dumps(newdict))
print(newdict)
    
input()