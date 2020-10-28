import time
import sqlite3 as lite
import paho.mqtt.client as mqtt
#import paho.mqtt.publish as publish
#import paho.mqtt.subscribe as subscribe
import json

con = None
broker = "broker.hivemq.com"
#broker = "192.168.43.249"
#broker = "localhost"

#path = "./userList" #Use internal memory
#path = "/media/DATABASE/userList" #Use external memory
path = "/home/pi/Documents/sql_databases/new_user_table.sqlite3"

err_cnt = 0

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        #print("Connection start")
        client.bad_connection_flag = False
        client.connected_flag = True        
        err_cnt = 0

        client.publish("HANevse/testsql", "Hello from SQLfunction",1 ,False)
        client.subscribe([("HANevse/getUsers", 2), ("HANevse/UpdateUser", 2), ("HANevse/photonMeasure", 2)])
        print("Connected OK")
    else:
        print("Bad connection, RC = ", rc)
        client.bad_connection_flag = True
        
def on_disconnect(client, userdata, rc):
    client.connected_flag = False
    if rc != 0:
        print("Unexpected disconnection.")
        client.bad_connection_flag = True
    else:
        print("Normal disconnection.")

def SendUser_callback(client, userdata, message):
    #print(message.payload)
    con = lite.connect(path)
    cur = con.cursor()
    cur.execute('SELECT * from list')

    data = cur.fetchall()
    dataSend = ""

    for element in data:
        print(element)
        dataSend += (str(element[0])+'%'+element[1]+'%'+element[2]+'%'+str(element[3])+'%'+element[4]+'%'+str(element[5])+'%'+element[6]+'%'+str(element[7])+'%'+str(element[8])+'%')
    
    client.publish("HANevse/UserList", dataSend, 2, True)
    #publish.single("HANevse/UserList", dataSend, hostname=broker)
    #print(dataSend)

def Update_callback(client, userdata, message):
    con = lite.connect(path)
    cur = con.cursor()
    data = json.loads(message.payload)
    
    UserId = str(data.get("UserId")).upper()
    socketId = int(data.get("Charger"))
    StartTime = int(data.get("StartTime"))
    
    cur.execute("SELECT LastStartOrStop, socketId FROM users WHERE uidTag=? LIMIT 1", (UserId,))
    dataUser = cur.fetchone() # returns a tuple
    dataSend = str(socketId) + ";"
    
    cur.execute("SELECT socketId FROM users WHERE socketId=? LIMIT 1", (socketId,))
    socketUsed = cur.fetchone()
    #The socketUsed can be either None or the socket number, so parsing it can give error without check
    if socketUsed is not None:
        socketUsed = socketUsed[0]
        
    #This is the filter for checking and preparing the answer to the EV charger
    if dataUser is not None: # if user ID is in list                       
        if ((StartTime - dataUser[0]) >= 20): # if last swipe is over 20s ago
            if (socketUsed == socketId): #if this socket is used now
                if (socketId == dataUser[1]): # if user already uses this socket
                    dataSend += "4" # successfully stop charging
                    cur.execute("UPDATE users SET socketId=?, LastStartOrStop=? WHERE uidTag=?", (None, StartTime, UserId))
                else:
                    dataSend += "3" # socket is occupied by another user 
            else: #if this socket is free
                if dataUser[1] is None: #if user was not using any socket
                    dataSend += "1" # successfully start new charge
                    cur.execute("UPDATE users SET socketId=?, LastStartOrStop=? WHERE uidTag=?", (socketId, StartTime, UserId))
                else:
                    dataSend += "6" # user already at another socket
        else: #if swiped less than 20s ago
            if (socketUsed == socketId): #if this socket is used now
                if (socketId == dataUser[1]): # if user already uses this socket
                    dataSend += "5" # you just started using this socket less than 20s ago
                else:
                    dataSend += "3" # socket is occupied by another user
            else: #if this socket is free
                if dataUser[1] is None: #if user was not using any socket
                    dataSend += "2" #charger is free, but you already swiped less than 20s ago
                else:
                    dataSend += "6"  # user already at another socket
    else:
        dataSend += "7" #user not in the userlist
    
    
    #cur.execute("UPDATE list SET PendingCharger=? WHERE Id=?", (PendingCharger, UserId))
    #cur.execute("UPDATE list SET StartTime=? WHERE Id=?", (StartTime, UserId))
    con.commit()
    
    client.publish("HANevse/allowUser", dataSend, 2, True)

def new_photonMeasure_callback(client, userdata, message):
    con = lite.connect(path)
    cur = con.cursor()
    data = json.loads(message.payload)    
    
    #V1 = float(data.get("V1"))
    #V2 = float(data.get("V2"))
    #V3 = float(data.get("V3"))
    #I1 = float(data.get("I1"))
    #I2 = float(data.get("I2"))
    #I3 = float(data.get("I3"))
    #P = float(data.get("P"))
    #E = float(data.get("E"))
    #F = float(data.get("F"))
    #Time = int(data.get("Time"))
    #SocketID = int(data.get("SocketID"))
    #UserID = str(data.get("UserID"))
    #cur.execute("INSERT INTO measurements(userID, socketId, phase_voltage_L1, phase_voltage_L2, phase_voltage_L3, current_L1, current_L2, current_L3, active_power, energy, frequency, createdAt) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
    #            (UserID, SocketID, V1, V2, V3, I1, I2, I3, P, E, F, Time))
    # Or skip all .get() and do them in execute
    cur.execute("INSERT INTO measurements(userID, socketId, phase_voltage_L1, phase_voltage_L2, phase_voltage_L3, current_L1, current_L2, current_L3, active_power, energy, frequency, createdAt) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                (str(data["UserID"]), int(data["ScoketID"]), float(data["V1"]), float(data["V2"]), float(data["V3"]), float(data["I1"]), float(data["I2"]), float(data["I3"]), float(data["P"]), float(data["E"]), float(data["F"]), time.strftime('%Y-%m-%d %T', time.localtime(int(data["Time"]) )) ))
    
    con.commit()


def photonMeasure_callback(client, userdata, message):
    con = lite.connect(path)
    cur = con.cursor()
    data = message.payload    
    data = data.decode('UTF-8')
    print(data)
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
    cur.execute("INSERT INTO photonMeasure(UIDtag, SocketID, V1, V2, V3, I1, I2, I3, P, E, F, Time) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                (UserID, SocketID, V1, V2, V3, I1, I2, I3, P, E, F, Time))
    con.commit()
    #print(V1)

#setup mqtt
client = mqtt.Client()
#client.username_pw_set(username="hanwatts", password="controlsystem")
client.connected_flag = False
client.bad_connection_flag = False
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect_async(broker, 1883, 60)

client.message_callback_add("HANevse/getUsers", SendUser_callback)
client.message_callback_add("HANevse/UpdateUser", Update_callback)
client.message_callback_add("HANevse/photonMeasure", photonMeasure_callback)
client.loop_start()


#client.publish("HANevse/testsql", "Hello from SQLfunction")
## publish.single gives connection error if ran too early
#publish.single("HANevse/testsql", "Hello from SQLfunction", hostname=broker)
   
while True:
    time.sleep(1)
    if (client.bad_connection_flag == True):
        err_cnt += 1
        if (err_cnt >= 10):
            client.loop_stop()
            client.disconnect()
            current_time = time.ctime()
            print(current_time, "- Client can't connect to broker.\nRestarting client.\n")            
            time.sleep(10)
            client.connect_async(broker, 1883, 60)
            client.loop_start()



