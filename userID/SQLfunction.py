## Program that manages the MQTT network on the Pi side


import time
import sqlite3 as lite
import paho.mqtt.client as mqtt
#import paho.mqtt.publish as publish
#import paho.mqtt.subscribe as subscribe
import json
import smtplib, ssl
import requests

## Const. for max time before email is sent to charging user
DISCONNECT_TIME = int(4 * 60 * 60) # 4 hours

email_cntr = 0
SSLport = 465  # For SSL
smtp_server = "smtp.gmail.com"
## Email sender address for Pi
sender_email = "tpi97364@gmail.com"  # Enter your address
## Holder for email addresses of receivers
receiver_email = ""  # Enter receiver address
## Pi email password
sender_password = "controlsystem" #input("Type your password and press enter: ")
## Default email message
email_message = """\
Subject: Unplug car

Please unplug your car from the EV charger. Over 4 hours have passed since it was plugged in.

This is an automatically generated email. A response to this email will not be read."""

email_context = ssl.create_default_context()

con = None

## MQTT broker address
broker = "broker.hivemq.com"
#broker = "192.168.43.249"
#broker = "localhost"

## Path to users database
#path = "./userList" #Use internal memory - old DB
path_local = "/media/DATABASE/usertable.sqlite3" #Use external memory = new_user_table
path = "/mnt/dav/Data/usertable.sqlite3" #Use cloud storage

con_local = lite.connect(path_local)
cur_local = con_local.cursor()

## Initial DB connection check
try:
    con = lite.connect(path)
    cur = con.cursor()
    cur.execute("SELECT * FROM measurements ORDER BY rowid DESC LIMIT 1")
    dataRef1 = cur.fetchone()
    print(dataRef1)
except Exception as e:
    print (e) 

err_cnt = 0

## Executes on MQTT client connect to broker, sets flags and subscribes
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        #print("Connection start")
        print(path)
        client.bad_connection_flag = False
        client.connected_flag = True        
        err_cnt = 0

        client.publish("HANevse/testsql", "Hello from SQLfunction",1 ,False)
#        client.subscribe([("HANevse/getUsers", 2), ("HANevse/UpdateUser", 2), ("HANevse/photonMeasure", 2)])
        client.subscribe([("HANevse/updateUser", 2), ("HANevse/photonMeasure", 2)])
        print("Connected OK")
    else:
        print("Bad connection, RC = ", rc)
        client.bad_connection_flag = True

## Executes on MQTT client disconnect and sets flags        
def on_disconnect(client, userdata, rc):
    client.connected_flag = False
    if rc != 0:
        print("Unexpected disconnection.")
        client.bad_connection_flag = True
    else:
        print("Normal disconnection.")

# def SendUser_callback(client, userdata, message):
#     #print(message.payload)
#     con = lite.connect(path)
#     cur = con.cursor()
#     cur.execute('select * from list')
# 
#     data = cur.fetchall()
#     dataSend = ""
# 
#     for element in data:
#         print(element)
#         dataSend += (str(element[0])+'%'+element[1]+'%'+element[2]+'%'+str(element[3])+'%'+element[4]+'%'+str(element[5])+'%'+element[6]+'%'+str(element[7])+'%'+str(element[8])+'%')
#     
#     client.publish("HANevse/UserList", dataSend, 2, True)
#     #publish.single("HANevse/UserList", dataSend, hostname=broker)
#     #print(dataSend)

## Callback function that parses RFID swipe message from Photon and checks in the DB what to publish as answer
# Publish output is structured as "1;2" where 1=socket number and 2=answer to Photon
def update_callback(client, userdata, message):
    try:
        con = lite.connect(path)
        cur = con.cursor()
    except Exception as e:
        print (e)
    con_local = lite.connect(path_local)
    cur_local = con_local.cursor()
    data = json.loads(message.payload)
    print(data)
    
    UserId = str(data.get("UserId")).upper()
    socketId = int(data.get("Charger"))
    StartTime = int(data.get("StartTime"))
    #print(UserId)
    try:
        cur.execute("SELECT LastStartOrStop, socketId, verified FROM users WHERE uidTag=? LIMIT 1", (UserId,))
        dataUser = cur.fetchone() # returns a tuple
    except Exception as e:
        print (e)
        cur_local.execute("SELECT LastStartOrStop, socketId, verified FROM users WHERE uidTag=? LIMIT 1", (UserId,))
        dataUser = cur_local.fetchone() # returns a tuple
    
    dataSend = str(socketId) + ";"
    try:
        cur.execute("SELECT socketId FROM users WHERE socketId=? LIMIT 1", (socketId,))
        socketUsed = cur.fetchone()
    except Exception as e:
        print (e)
        cur_local.execute("SELECT socketId FROM users WHERE socketId=? LIMIT 1", (socketId,))
        socketUsed = cur_local.fetchone()
    #The socketUsed can be either None or the socket number, so parsing it can give error without check
    if socketUsed is not None:
        socketUsed = socketUsed[0]
        
    #This is the filter for checking and preparing the answer to the EV charger
    if dataUser is not None: # if user ID is in list
        if (dataUser[2] == "true"):
            if ((StartTime - dataUser[0]) >= 20): # if last swipe is over 20s ago
                if (socketUsed == socketId): #if this socket is used now
                    if (socketId == dataUser[1]): # if user already uses this socket
                        dataSend += "4" # successfully stop charging
                        try:
                            cur.execute("UPDATE users SET socketId=?, LastStartOrStop=? WHERE uidTag=?", (None, StartTime, UserId))             
                        except Exception as e:
                            print (e)
                        finally:
                            cur_local.execute("UPDATE users SET socketId=?, LastStartOrStop=? WHERE uidTag=?", (None, StartTime, UserId))
                    else:
                        dataSend += "3" # socket is occupied by another user 
                else: #if this socket is free
                    if dataUser[1] is None: #if user was not using any socket
                        dataSend += "1" # successfully start new charge
                        try:
                            cur.execute("UPDATE users SET socketId=?, LastStartOrStop=? WHERE uidTag=?", (socketId, StartTime, UserId))
                        except Exception as e:
                            print (e)
                        finally:
                            cur_local.execute("UPDATE users SET socketId=?, LastStartOrStop=? WHERE uidTag=?", (socketId, StartTime, UserId))
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
             dataSend += "7" #user not verified by admin           
    else:
        dataSend += "8" #user not in the userlist
    try:
        con.commit()
    except Exception as e:
        print (e)
    con_local.commit()
    
    client.publish("HANevse/allowUser", dataSend, 0, False)

# def Update_callback(client, userdata, message):
#     con = lite.connect(path)
#     cur = con.cursor()
#     data = message.payload
#     index = []
#     for i in range(len(data)):
#         if (data[i] == '%'):
#             index.append(i)
#     UserId = int(data[:index[0]])
#     PendingCharger = int(data[index[0]+1:index[1]])
#     StartTime = int(data[index[1]+1:index[2]])
#     cur.execute("UPDATE list SET PendingCharger=? WHERE Id=?", (PendingCharger, UserId))
#     cur.execute("UPDATE list SET StartTime=? WHERE Id=?", (StartTime, UserId))
#     con.commmit()


## New Callback for Photon measurements that parses, checks DB for user data like name and carname, then logs into 'measurements'
def new_photonMeasure_callback(client, userdata, message):
    try:
        con = lite.connect(path)
        cur = con.cursor()
    except Exception as e:
        print (e)
    con_local = lite.connect(path_local)
    cur_local = con_local.cursor()
    data = json.loads(message.payload)    
    print(data)
    V1 = float(data.get("V1"))
    V2 = float(data.get("V2"))
    V3 = float(data.get("V3"))
    I1 = float(data.get("I1"))
    I2 = float(data.get("I2"))
    I3 = float(data.get("I3"))
    #P = float(data.get("P"))
    #E = float(data.get("E"))
    F = float(data.get("F"))
    Time = int(data.get("Time"))
    SocketID = int(data.get("SocketID"))
    UserID = str(data.get("UserID")).upper()
    
    try:
        cur.execute("SELECT name, rowid FROM users WHERE uidTag = ? ", (UserID,) )
        dataUser = cur.fetchone()
    except Exception as e:
        print (e)
        cur_local.execute("SELECT name, rowid FROM users WHERE uidTag = ? ", (UserID,) )
        dataUser = cur_local.fetchone()
        
    try:
        dataUser[1]
    except Exception as e:
        print (e)
        print("WARNING: Unauthorized user " + UserID + " charging at socket " + str(SocketID))
        dataUser = ('unknown', 31)                
    try:
        cur.execute("SELECT carId FROM car_of_user WHERE userId = ? ", (dataUser[1],) )
        if (cur.fetchone() is None):
            carId = 404
        else:
            carId = cur.fetchone()[0]        
    except Exception as e:
        print (e)
        cur_local.execute("SELECT carId FROM car_of_user WHERE userId = ? ", (dataUser[1],) )
        if (cur.fetchone() is None):
            carId = 404
        else:
            carId = cur_local.fetchone()[0]
    
    try:
        cur.execute("SELECT brand || ' ' || type FROM cars WHERE id = ? ", (carId,) )
        carName = cur.fetchone()[0]
    except Exception as e:
        print (e)
        cur_local.execute("SELECT brand || ' ' || type FROM cars WHERE id = ? ", (carId,) )
        carName = cur_local.fetchone()[0]
    try:    
        cur.execute("INSERT INTO measurements(userId, userName, carId, carName, socketId, V1, V2, V3, I1, I2, I3, F, Time) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (UserID, dataUser[0], carId, carName, SocketID, V1, V2, V3, I1, I2, I3, F, Time))
        con.commit()
    except Exception as e:
        print (e)
    finally:
        cur_local.execute("INSERT INTO measurements(userId, userName, carId, carName, socketId, V1, V2, V3, I1, I2, I3, F, Time) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (UserID, dataUser[0], carId, carName, SocketID, V1, V2, V3, I1, I2, I3, F, Time))
    
    con_local.commit()
    #-#Insert with P and E measurements
    #cur.execute("INSERT INTO measurements(userId, userName, carId, carName, socketId, V1, V2, V3, I1, I2, I3, P, E, F, Time) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
    #            (UserID, dataUser[0], carId, carName, SocketID, V1, V2, V3, I1, I2, I3, P, E, F, Time))
    
    # Or skip all .get() and do it in cur.execute     
    #cur.execute("INSERT INTO measurements(userId, socketId, V1, V2, V3, I1, I2, I3, P, E, F, Time) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
    #            (str(data["UserID"]).upper(), int(data["SocketID"]), float(data["V1"]), float(data["V2"]), float(data["V3"]), float(data["I1"]), float(data["I2"]), float(data["I3"]), float(data["P"]), float(data["E"]), float(data["F"]), int(data["Time"]) ))
    
   #for readable timestamp use this at end of INSERT: time.strftime('%Y-%m-%d %T', time.localtime(int(data["Time"]) ))
    
    

## Old Photon measurements callback that parses '%' separated values
def old_photonMeasure_callback(client, userdata, message):
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

## Function to send admin email if one user has been plugged in at a socket for over 4 hours
# still in beta mode and needs improvements
def send_admin():
    try:
        con = lite.connect(path)
        cur = con.cursor()
        cur.execute("SELECT rowid FROM measurements WHERE Time <= ? AND Time >= ? LIMIT 1", ((str(int(time.time()) - DISCONNECT_TIME)),(str(int(time.time()) - DISCONNECT_TIME - 29)),) )
        dataRef = cur.fetchone()
        if dataRef is None:
            pass
        else:
            cur.execute("SELECT rowid FROM measurements WHERE Time >= ? LIMIT 1", ((str(int(time.time()) - 60)),) )
            dataRef = cur.fetchone()
            if dataRef is None:
                pass
            else:
                with smtplib.SMTP_SSL(smtp_server, SSLport, context=email_context) as server:
                    server.login(sender_email, sender_password)                    
                    server.sendmail(sender_email, "nguyenxuan.trung@han.nl", email_message)
    except Exception as e:
        print (e)
        con_local = lite.connect(path_local)
        cur_local = con_local.cursor()
        cur_local.execute("SELECT rowid FROM measurements WHERE Time <= ? AND Time >= ? LIMIT 1", ((str(int(time.time()) - DISCONNECT_TIME)),(str(int(time.time()) - DISCONNECT_TIME - 29)),) )
        dataRef = cur_local.fetchone()
        if dataRef is None:
            pass
        else:
            cur_local.execute("SELECT rowid FROM measurements WHERE Time >= ? LIMIT 1", ((str(int(time.time()) - 60)),) )
            dataRef = cur_local.fetchone()
            if dataRef is None:
                pass
            else:
                with smtplib.SMTP_SSL(smtp_server, SSLport, context=email_context) as server:
                    server.login(sender_email, sender_password)                    
                    server.sendmail(sender_email, "nguyenxuan.trung@han.nl", email_message)
            
#     if dataRef is None:
#         pass
#     else:
#         try:
#             cur.execute("SELECT rowid FROM measurements WHERE Time >= ? LIMIT 1", ((str(int(time.time()) - 60)),) )
#             dataRef = cur.fetchone()
#         except Exception as e:
#             print (e)
#             cur_local.execute("SELECT rowid FROM measurements WHERE Time >= ? LIMIT 1", ((str(int(time.time()) - 60)),) )
#             dataRef = cur_local.fetchone()
#             
#         if dataRef is None:
#             pass
#         else:
#             with smtplib.SMTP_SSL(smtp_server, SSLport, context=email_context) as server:
#                 server.login(sender_email, sender_password)                    
#                 server.sendmail(sender_email, "nguyenxuan.trung@han.nl", email_message)

# Function (executed every 5min) that checks in DB for users charging for over 4 hours ands sends them email to d/c
def send_email():
    
    con_local = lite.connect(path_local)
    cur_local = con_local.cursor()
    try:
        con = lite.connect(path)
        cur = con.cursor()
        cur.execute("SELECT email, rowid FROM users WHERE LastStartOrStop <= ? AND email <> '' AND mailed < 1 AND socketId IS NOT NULL", ((str(int(time.time()) - DISCONNECT_TIME)),) )
        dataRef = cur.fetchall()
    except Exception as e:
        print (e)        
        cur_local.execute("SELECT email, rowid FROM users WHERE LastStartOrStop <= ? AND email <> '' AND mailed < 1 AND socketId IS NOT NULL", ((str(int(time.time()) - DISCONNECT_TIME)),) )
        dataRef = cur_local.fetchall()
        
    if dataRef is None:
        return
    url = "http://www.kite.com"
    timeout = 5
    try:
        request = requests.get(url, timeout=timeout)
        print("Connected to the Internet")
    except (requests.ConnectionError, requests.Timeout) as exception:
        return
    with smtplib.SMTP_SSL(smtp_server, SSLport, context=email_context) as server:
        server.login(sender_email, sender_password)
        for element in dataRef:            
            server.sendmail(sender_email, element[0], email_message)
            try:
                cur.execute("UPDATE users SET mailed = 1 WHERE rowid=?", (element[1],))
            except Exception as e:
                print (e)
            cur_local.execute("UPDATE users SET mailed = 1 WHERE rowid=?", (element[1],))
    #cur.execute("UPDATE users SET mailed = 0 WHERE LastStartOrStop > ? AND mailed > 0 AND socketId IS NULL", ((str(int(time.time()) - DISCONNECT_TIME)),) ) 
    try:
        cur.execute("UPDATE users SET mailed = 0 WHERE mailed > 0 AND socketId IS NULL") 
        con.commit()
    except Exception as e:
        print (e)
    cur_local.execute("UPDATE users SET mailed = 0 WHERE mailed > 0 AND socketId IS NULL") 
    con_local.commit()

#setup mqtt
client = mqtt.Client()
#client.username_pw_set(username="hanwatts", password="controlsystem")
client.connected_flag = False
client.bad_connection_flag = False
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect_async(broker, 1883, 60)


send_admin()
send_email()

#client.message_callback_add("HANevse/getUsers", SendUser_callback)
client.message_callback_add("HANevse/updateUser", update_callback)
client.message_callback_add("HANevse/photonMeasure", new_photonMeasure_callback)
client.loop_start()


#client.publish("HANevse/testsql", "Hello from SQLfunction")
#- publish.single gives connection error if ran too early
#publish.single("HANevse/testsql", "Hello from SQLfunction", hostname=broker)

#-# Main loop that checks if MQTT client disconnectd to send_email() should be run   
while True:
    time.sleep(1)
    if (client.bad_connection_flag == True):
        err_cnt += 1
        if (err_cnt >= 20):
            client.loop_stop()
            client.disconnect()
            current_time = time.ctime(time.time())
            print(current_time, "- Client can't connect to broker.\nRestarting client.\n")            
            time.sleep(300)
            client.connect_async(broker, 1883, 60)
            client.loop_start()
    email_cntr += 1
    if (email_cntr > 301):
        email_cntr = 0
        send_email()
        