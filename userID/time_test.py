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

# con = None
# path = "/home/pi/Documents/sql_databases/new_user_table.sqlite3"
# con = lite.connect(path)
# cur = con.cursor()
# #data = json.loads(message.payload)
#     #index = []
#     #for i in range(len(data)):
#     #    if (data[i] == ';'):
#     #       index.append(i)
# UserId = "No ID"
# 
# #PendingCharger = data.get("Charger")
# #StartTime = data.get("StartTime")
#     
# cur.execute("SELECT name, uidTag, LastStartOrStop, socketId FROM users WHERE uidTag=? LIMIT 1", (UserId,))
# dataRef = cur.fetchone()
# print(dataRef)
# #print(dataRef[3])
# #print(type(dataRef[3]))
# 
# if dataRef is None:
#     print("compare works")
# else:
#     print("can't compare")
# 
# socketId = 6
# cur.execute("SELECT socketId FROM users WHERE socketId=? LIMIT 1", (socketId,))    
# socketFree =  cur.fetchone()
# if socketFree is not None:
#     socketFree = socketFree[0]
# print(socketFree)
# print(type(socketFree))
# if socketFree == socketId:
#     print("socket compare works")
# else:
#     print("socket can't compare")
# 
# data1 = json.loads( "{\"UserId\":\"28 b3 cx\",\"t2\":1234,\"t3\":1234.5,\"t4\":true,\"t5\":false,\"t6\":null, \"t7\" : \"\\\"quoted\\\"\" } ")
# UserId = str(data1.get("UserId")).upper()  
# print(UserId)
# 
# x = ('UserId', 'Charger', 'StartTime')
# y = "default"
# 
# #thisdict = dict.fromkeys(x, y)
# newdict = {'UserId': "BB 77 E3 59", 'Charger': 2, 'StartTime': 1603900707}

data = "231.79%230.78%231.00%0.00%0.00%0.00%0.00%231.46%50.01%1601895079%2%No ID%"

index = []
for i in range(len(data)):
    if (data[i] == '%'):
        index.append(i)
V1 = float(data[:index[0]])
V2 = float(data[index[0]+1:index[1]])
V3 = float(data[index[1]+1:index[2]])
I1 = float(data[index[2]+1:index[3]])
I2 = float(data[index[3]+1:index[4]])
I3 = float(data[index[4]+1:index[5]])
P = float(data[index[5]+1:index[6]])
E = float(data[index[6]+1:index[7]])
F = float(data[index[7]+1:index[8]])
Time = int(data[index[8]+1:index[9]])
SocketID = int(data[index[9]+1:index[10]])
UserID = data[index[10]+1:index[11]]

x = ('UserID', 'SocketID', 'V1', 'V2', 'V3', 'I1', 'I2', 'I3', 'P', 'E', 'F', 'Time')

thisdict = dict.fromkeys(x)
thisdict["V1"] = V1
thisdict["V2"] = V2
thisdict["V3"] = V3
thisdict["I1"] = I1
thisdict["I2"] = I2
thisdict["I3"] = I3
thisdict["P"] = P
thisdict["E"] = E
thisdict["F"] = F
thisdict["Time"] = Time
thisdict["SocketID"] = SocketID
thisdict["UserID"] = UserID

print(json.dumps(thisdict))
print(thisdict)
    
input()