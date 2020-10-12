import time
import sqlite3 as lite
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import json

con = None
broker = "broker.hivemq.com"
#broker = "192.168.43.249"
#broker = "localhost"

#path = "./userList" #Use internal memory
path = "/media/usb/userList" #Use external memory

err_cnt = 0

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        #print("Connection start")
        client.bad_connection_flag = False
        client.connected_flag = True        
        err_cnt = 0


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
  111!!!  cur.execute('SELECT * FROM list')   What table should it send?  -Answer = none, this will be removed
  #probably "SELECT * from car_of_user"
    dataSend = json.dumps( cur.fetchall() )
    #print(dataSend)
    #dataSend = ""

    #for element in data:
     #   print(element)
     #   dataSend += (str(element[0])+'%'+element[1]+'%'+element[2]+'%'+str(element[3])+'%'+element[4]+'%'+str(element[5])+'%'+element[6]+'%'+str(element[7])+'%'+str(element[8])+'%')
    
    client.publish("HANevse/UserList2", dataSend, 2, True)
    #publish.single("HANevse/UserList", dataSend, hostname=broker)
    print(dataSend)

def Update_callback(client, userdata, message):
    con = lite.connect(path)
    cur = con.cursor()
    data = json.loads(message.payload)
    
    #for i in range(len(data)):
     #   if (data[i] == '%'):
     #       index.append(i)
    #UserId = int(data[:index[0]])
    #PendingCharger = int(data[index[0]+1:index[1]])
    #StartTime = int(data[index[1]+1:index[2]])
    UserId = int(data[0])
    PendingCharger = int(data[1])
    StartTime = int(data[2])       !!! What is the equivalent of PendingCharger in new table? #mailed = if the owner used charger for over 4 hours he gets message
 111!!!   cur.execute("""UPDATE list SET PendingCharger=?, StartTime=? WHERE Id=?""", (PendingCharger, StartTime, UserId))
    #cur.execute("UPDATE list SET PendingCharger=? WHERE Id=?", (PendingCharger, UserId))
    #cur.execute("UPDATE list SET StartTime=? WHERE Id=?", (StartTime, UserId))
    con.commmit()

def photonMeasure_callback(client, userdata, message):
    con = lite.connect(path)
    cur = con.cursor()
    data = json.loads(message.payload) 
    #data = data.decode('UTF-8')
    #print(data)
    #index = []
    #for i in range(len(data)):
    #    if (data[i] == '%'):
    #        index.append(i)
    #V1 = float(data[:index[0]])
    #V2 = float(data[index[0]+1:index[1]])
    #V3 = float(data[index[1]+1:index[2]])
    #I1 = float(data[index[2]+1:index[3]])
    #I2 = float(data[index[3]+1:index[4]])
    #I3 = float(data[index[4]+1:index[5]])
    #P = float(data[index[5]+1:index[6]])
    #E = float(data[index[6]+1:index[7]])
    #F = float(data[index[7]+1:index[8]])
    #Time = int(data[index[8]+1:index[9]])
    #SocketID = int(data[index[9]+1:index[10]])
    # UserID = data[index[10]+1:index[11]]
    V1 = float(data[0])
    V2 = float(data[1])
    V3 = float(data[2])
    I1 = float(data[3])
    I2 = float(data[4])
    I3 = float(data[5])
    P = float(data[6])
    E = float(data[7])
    F = float(data[8])
    Time = int(data[9])
    SocketID = int(data[10])
    UserID = data[11]
    cur.execute("INSERT INTO measurements(userID, socketId, phase_voltage_L1, phase_voltage_L2, phase_voltage_L3, current_L1, current_L2, current_L3, active_power, energy, frequency, createdAt) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                (UserID, SocketID, V1, V2, V3, I1, I2, I3, P, E, F, Time))
    con.commit()
    

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

client.publish("HANevse/testsql", "Hello from sql", 2, True)
#publish.single("HANevse/testsql", "Hello from sql", hostname=broker)
   
while True:
    time.sleep(1)
    if (client.bad_connection_flag == True):
        err_cnt += 1
        if (err_cnt >= 10):
            client.loop_stop()
            client.disconnect()
            current_time = time.ctime(time.time())
            print(current_time, "- Client can't connect to broker.\nRestarting client.\n")            
            time.sleep(10)
            client.connect_async(broker, 1883, 60)
            client.loop_start()



