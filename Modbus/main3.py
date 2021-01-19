## Program that manages the Modbus network on the Pi side


import RPi.GPIO as GPIO
import serial
import MIC3 as MIC
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
#import paho.mqtt.subscribe as subscribe
import sqlite3 as lite
import sys
import os
import json

## MQTT broker

#broker = "localhost"
#broker = "tcp://127.0.0.1"
broker = "broker.hivemq.com"

##Path for modbus database

#path = "./modbusData.db" #Use internal memory
path_local = "/media/DATABASE/modbusData.db" #Use external memory
path = "/mnt/dav/Data/modbusData.db" #Use cloud storage

##Path for users database
path_local_user = "/media/DATABASE/usertable.sqlite3" #Use external memory
path_user = "/mnt/dav/Data/usertable.sqlite3" #Use cloud storage

con_user_local = lite.connect(path_local_user)
cur_user_local = con_user_local.cursor()

## Initial DB connection check
try:
    con_user = lite.connect(path_user)
    cur_user = con_user.cursor()
except Exception as e:
    print (e)

con_local = lite.connect(path_local)
cur_local = con_local.cursor()

try:
    con = lite.connect(path)
    cur = con.cursor()
    cur.execute("SELECT * FROM Grid ORDER BY rowid DESC LIMIT 1")
    dataRef1 = cur.fetchone()
    print(dataRef1)
except Exception as e:
    print (e)


err_cnt = 0

## Executes on MQTT client connect to broker and sets flags
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        #print("Connection start")
        client.bad_connection_flag = False
        client.connected_flag = True        
        err_cnt = 0

        client.publish("HANevse/testmodbus", "Hello from Modbus function", 1, False)
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

client = mqtt.Client()
#client.username_pw_set(username="hanwatts", password="controlsystem")
client.connected_flag = False
client.bad_connection_flag = False
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect_async(broker, 1883, 60)
client.loop_start()
#Pin definitions
control_pin = 18

#Use BCM pin numbering
GPIO.setmode(GPIO.BCM)

#Turn off warnings
GPIO.setwarnings(False)

#Control pin as an output
GPIO.setup(control_pin, GPIO.OUT)

#Announcement
#client.username_pw_set(username="hanwatts", password="controlsystem")
#auth={'username':"hanwatts", 'password':"controlsystem"}
#publish.single("HANevse/testmain", "Hello from main", qos= 2, retain=True, hostname=broker, auth={'username':"hanwatts", 'password':"controlsystem"})
#publish.single("HANevse/testmain", "Hello from main", hostname=broker)

print("Program was written by P.M.Nhat and C.Batog")
print("ver 2.5")
print("MODBUS converter: MAX485")
print("MODBUS slave: MIC1")

#Declare slave(s)
#meter1 = MIC.MIC2(0x01, control_pin)
## Initializes meter
meter1 = MIC.MIC1(0x01, control_pin)
meter2 = MIC.MIC1(0x02, control_pin)
meter3 = MIC.MIC1(0x03, control_pin)
meter4 = MIC.MIC1(0x04, control_pin)
meter5 = MIC.MIC1(0x05, control_pin)

#count to send new data after 1 min
time_send = 1

#-# Main loop to check if MQTT client is connected, then take and log measurements from each meter, then send Current sepoint for Photons
while True:
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
    try:
        con = lite.connect(path)
        cur = con.cursor()
    except Exception as e:
        print (e)
    
    print("E1:")
    #Read PT1, PT2, CT1:
    readingPT1 = meter1.readPT1()
    readingPT2 = meter1.readPT2()
    readingCT1 = meter1.readCT1()
    #If there is no error, then continue
    if((readingPT1+readingPT2+readingCT1)==0):
        #Read PHASE VOLTAGE
        reading = meter1.readPhaseVoltage()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        V1: %.2f   V2: %.2f   V3: %.2f
        """%(meter1._MIC1__V1, meter1._MIC1__V2, meter1._MIC1__V3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read PHASE CURRENT
        reading = meter1.readPhaseCurrent()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        I1: %.2f   I2: %.2f   I3: %.2f
        """%(meter1._MIC1__I1, meter1._MIC1__I2, meter1._MIC1__I3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read PHASE POWER
        reading = meter1.readPhasePower()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        P1: %.2f   P2: %.2f   P3: %.2f
        """%(meter1._MIC1__P1, meter1._MIC1__P2, meter1._MIC1__P3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read REACTIVE POWER
        reading = meter1.readReactivePower()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        Q1: %.2f   Q2: %.2f   Q3: %.2f
        """%(meter1._MIC1__Q1, meter1._MIC1__Q2, meter1._MIC1__Q3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read APPARENT POWER
        reading = meter1.readApparentPower()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        S1: %.2f   S2: %.2f   S3: %.2f
        """%(meter1._MIC1__S1, meter1._MIC1__S2, meter1._MIC1__S3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read POWER FACTOR
        reading = meter1.readPowerFactor()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        PF1: %.2f   PF2: %.2f   PF3: %.2f
        """%(meter1._MIC1__PF1, meter1._MIC1__PF2, meter1._MIC1__PF3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read FREQUENCY
        reading = meter1.readFrequency()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        F: %.3f
        """%(meter1._MIC1__F)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        try:
            cur.execute("INSERT INTO Demonstration(Time, V1, V2, V3, I1, I2, I3, P1, P2, P3, Q1, Q2, Q3, S1, S2, S3, PF1, PF2, PF3, F) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (int(round(time.time())),
                         meter1._MIC1__V1, meter1._MIC1__V2, meter1._MIC1__V3,
                         meter1._MIC1__I1, meter1._MIC1__I2, meter1._MIC1__I3,
                         meter1._MIC1__P1, meter1._MIC1__P2, meter1._MIC1__P3,
                         meter1._MIC1__Q1, meter1._MIC1__Q2, meter1._MIC1__Q3,
                         meter1._MIC1__S1, meter1._MIC1__S2, meter1._MIC1__S3,
                         meter1._MIC1__PF1, meter1._MIC1__PF2, meter1._MIC1__PF3,
                         meter1._MIC1__F))
            con.commit()
        except  Exception as e:
             print (e)
        cur_local.execute("INSERT INTO Demonstration(Time, V1, V2, V3, I1, I2, I3, P1, P2, P3, Q1, Q2, Q3, S1, S2, S3, PF1, PF2, PF3, F) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (int(round(time.time())),
                     meter1._MIC1__V1, meter1._MIC1__V2, meter1._MIC1__V3,
                     meter1._MIC1__I1, meter1._MIC1__I2, meter1._MIC1__I3,
                     meter1._MIC1__P1, meter1._MIC1__P2, meter1._MIC1__P3,
                     meter1._MIC1__Q1, meter1._MIC1__Q2, meter1._MIC1__Q3,
                     meter1._MIC1__S1, meter1._MIC1__S2, meter1._MIC1__S3,
                     meter1._MIC1__PF1, meter1._MIC1__PF2, meter1._MIC1__PF3,
                     meter1._MIC1__F))
        con_local.commit()
    else:
        print(">>Reading PT1, PT2, CT1 failed")
    #Read meter 2----------------------------------------------
    print("E2:")
    #Read PT1, PT2, CT1:
    readingPT1 = meter2.readPT1()
    readingPT2 = meter2.readPT2()
    readingCT1 = meter2.readCT1()
    #If there is no error, then continue
    if((readingPT1+readingPT2+readingCT1)==0):
        #Read PHASE VOLTAGE
        reading = meter2.readPhaseVoltage()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        V1: %.2f   V2: %.2f   V3: %.2f
        """%(meter2._MIC1__V1, meter2._MIC1__V2, meter2._MIC1__V3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read PHASE CURRENT
        reading = meter2.readPhaseCurrent()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        I1: %.2f   I2: %.2f   I3: %.2f
        """%(meter2._MIC1__I1, meter2._MIC1__I2, meter2._MIC1__I3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read PHASE POWER
        reading = meter2.readPhasePower()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        P1: %.2f   P2: %.2f   P3: %.2f
        """%(meter2._MIC1__P1, meter2._MIC1__P2, meter2._MIC1__P3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read REACTIVE POWER
        reading = meter2.readReactivePower()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        Q1: %.2f   Q2: %.2f   Q3: %.2f
        """%(meter2._MIC1__Q1, meter2._MIC1__Q2, meter2._MIC1__Q3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read APPARENT POWER
        reading = meter2.readApparentPower()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        S1: %.2f   S2: %.2f   S3: %.2f
        """%(meter2._MIC1__S1, meter2._MIC1__S2, meter2._MIC1__S3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read POWER FACTOR
        reading = meter2.readPowerFactor()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        PF1: %.2f   PF2: %.2f   PF3: %.2f
        """%(meter2._MIC1__PF1, meter2._MIC1__PF2, meter2._MIC1__PF3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))            
        #Read FREQUENCY
        reading = meter2.readFrequency()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        F: %.3f
        """%(meter2._MIC1__F)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        try:
            cur.execute("INSERT INTO Reserve(Time, V1, V2, V3, I1, I2, I3, P1, P2, P3, Q1, Q2, Q3, S1, S2, S3, PF1, PF2, PF3, F) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (int(round(time.time())),
                         meter2._MIC1__V1, meter2._MIC1__V2, meter2._MIC1__V3,
                         meter2._MIC1__I1, meter2._MIC1__I2, meter2._MIC1__I3,
                         meter2._MIC1__P1, meter2._MIC1__P2, meter2._MIC1__P3,
                         meter2._MIC1__Q1, meter2._MIC1__Q2, meter2._MIC1__Q3,
                         meter2._MIC1__S1, meter2._MIC1__S2, meter2._MIC1__S3,
                         meter2._MIC1__PF1, meter2._MIC1__PF2, meter2._MIC1__PF3,
                         meter2._MIC1__F))
            con.commit()
        except  Exception as e:
            print (e)
        cur_local.execute("INSERT INTO Reserve(Time, V1, V2, V3, I1, I2, I3, P1, P2, P3, Q1, Q2, Q3, S1, S2, S3, PF1, PF2, PF3, F) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (int(round(time.time())),
                     meter2._MIC1__V1, meter2._MIC1__V2, meter2._MIC1__V3,
                     meter2._MIC1__I1, meter2._MIC1__I2, meter2._MIC1__I3,
                     meter2._MIC1__P1, meter2._MIC1__P2, meter2._MIC1__P3,
                     meter2._MIC1__Q1, meter2._MIC1__Q2, meter2._MIC1__Q3,
                     meter2._MIC1__S1, meter2._MIC1__S2, meter2._MIC1__S3,
                     meter2._MIC1__PF1, meter2._MIC1__PF2, meter2._MIC1__PF3,
                     meter2._MIC1__F))
        con_local.commit()
    else:
        print(">>Reading PT1, PT2, CT1 failed")
    #Read meter 3----------------------------------------------
    print("E3:")
    #Read PT1, PT2, CT1:
    readingPT1 = meter3.readPT1()
    readingPT2 = meter3.readPT2()
    readingCT1 = meter3.readCT1()
    #If there is no error, then continue
    if((readingPT1+readingPT2+readingCT1)==0):
        #Read PHASE VOLTAGE
        reading = meter3.readPhaseVoltage()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        V1: %.2f   V2: %.2f   V3: %.2f
        """%(meter3._MIC1__V1, meter3._MIC1__V2, meter3._MIC1__V3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read PHASE CURRENT
        reading = meter3.readPhaseCurrent()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        I1: %.2f   I2: %.2f   I3: %.2f
        """%(meter3._MIC1__I1, meter3._MIC1__I2, meter3._MIC1__I3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read PHASE POWER
        reading = meter3.readPhasePower()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        P1: %.2f   P2: %.2f   P3: %.2f
        """%(meter3._MIC1__P1, meter3._MIC1__P2, meter3._MIC1__P3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read REACTIVE POWER
        reading = meter3.readReactivePower()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        Q1: %.2f   Q2: %.2f   Q3: %.2f
        """%(meter3._MIC1__Q1, meter3._MIC1__Q2, meter3._MIC1__Q3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read APPARENT POWER
        reading = meter3.readApparentPower()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        S1: %.2f   S2: %.2f   S3: %.2f
        """%(meter3._MIC1__S1, meter3._MIC1__S2, meter3._MIC1__S3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read POWER FACTOR
        reading = meter3.readPowerFactor()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        PF1: %.2f   PF2: %.2f   PF3: %.2f
        """%(meter3._MIC1__PF1, meter3._MIC1__PF2, meter3._MIC1__PF3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read FREQUENCY
        reading = meter3.readFrequency()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        F: %.3f
        """%(meter3._MIC1__F)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        try:
            cur.execute("INSERT INTO PV(Time, V1, V2, V3, I1, I2, I3, P1, P2, P3, Q1, Q2, Q3, S1, S2, S3, PF1, PF2, PF3, F) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (int(round(time.time())),
                         meter3._MIC1__V1, meter3._MIC1__V2, meter3._MIC1__V3,
                         meter3._MIC1__I1, meter3._MIC1__I2, meter3._MIC1__I3,
                         meter3._MIC1__P1, meter3._MIC1__P2, meter3._MIC1__P3,
                         meter3._MIC1__Q1, meter3._MIC1__Q2, meter3._MIC1__Q3,
                         meter3._MIC1__S1, meter3._MIC1__S2, meter3._MIC1__S3,
                         meter3._MIC1__PF1, meter3._MIC1__PF2, meter3._MIC1__PF3,
                         meter3._MIC1__F))
            con.commit()
        except  Exception as e:
             print (e)
        cur_local.execute("INSERT INTO PV(Time, V1, V2, V3, I1, I2, I3, P1, P2, P3, Q1, Q2, Q3, S1, S2, S3, PF1, PF2, PF3, F) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (int(round(time.time())),
                     meter3._MIC1__V1, meter3._MIC1__V2, meter3._MIC1__V3,
                     meter3._MIC1__I1, meter3._MIC1__I2, meter3._MIC1__I3,
                     meter3._MIC1__P1, meter3._MIC1__P2, meter3._MIC1__P3,
                     meter3._MIC1__Q1, meter3._MIC1__Q2, meter3._MIC1__Q3,
                     meter3._MIC1__S1, meter3._MIC1__S2, meter3._MIC1__S3,
                     meter3._MIC1__PF1, meter3._MIC1__PF2, meter3._MIC1__PF3,
                     meter3._MIC1__F))
        con_local.commit()
    else:
        print(">>Reading PT1, PT2, CT1 failed")
    #Read meter 4----------------------------------------------
    print("E4:")
    #Read PT1, PT2, CT1:
    readingPT1 = meter4.readPT1()
    readingPT2 = meter4.readPT2()
    readingCT1 = meter4.readCT1()
    #If there is no error, then continue
    if((readingPT1+readingPT2+readingCT1)==0):
        #Read PHASE VOLTAGE
        reading = meter4.readPhaseVoltage()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        V1: %.2f   V2: %.2f   V3: %.2f
        """%(meter4._MIC1__V1, meter4._MIC1__V2, meter4._MIC1__V3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read PHASE CURRENT
        reading = meter4.readPhaseCurrent()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        I1: %.2f   I2: %.2f   I3: %.2f
        """%(meter4._MIC1__I1, meter4._MIC1__I2, meter4._MIC1__I3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read PHASE POWER
        reading = meter4.readPhasePower()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        P1: %.2f   P2: %.2f   P3: %.2f
        """%(meter4._MIC1__P1, meter4._MIC1__P2, meter4._MIC1__P3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read REACTIVE POWER
        reading = meter4.readReactivePower()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        Q1: %.2f   Q2: %.2f   Q3: %.2f
        """%(meter4._MIC1__Q1, meter4._MIC1__Q2, meter4._MIC1__Q3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read APPARENT POWER
        reading = meter4.readApparentPower()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        S1: %.2f   S2: %.2f   S3: %.2f
        """%(meter4._MIC1__S1, meter4._MIC1__S2, meter4._MIC1__S3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read POWER FACTOR
        reading = meter4.readPowerFactor()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        PF1: %.2f   PF2: %.2f   PF3: %.2f
        """%(meter4._MIC1__PF1, meter4._MIC1__PF2, meter4._MIC1__PF3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read FREQUENCY
        reading = meter4.readFrequency()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        F: %.3f
        """%(meter4._MIC1__F)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        try:
            cur.execute("INSERT INTO Battery(Time, V1, V2, V3, I1, I2, I3, P1, P2, P3, Q1, Q2, Q3, S1, S2, S3, PF1, PF2, PF3, F) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (int(round(time.time())),
                         meter4._MIC1__V1, meter4._MIC1__V2, meter4._MIC1__V3,
                         meter4._MIC1__I1, meter4._MIC1__I2, meter4._MIC1__I3,
                         meter4._MIC1__P1, meter4._MIC1__P2, meter4._MIC1__P3,
                         meter4._MIC1__Q1, meter4._MIC1__Q2, meter4._MIC1__Q3,
                         meter4._MIC1__S1, meter4._MIC1__S2, meter4._MIC1__S3,
                         meter4._MIC1__PF1, meter4._MIC1__PF2, meter4._MIC1__PF3,
                         meter4._MIC1__F))
            con.commit()
        except  Exception as e:
             print (e)
        cur_local.execute("INSERT INTO Battery(Time, V1, V2, V3, I1, I2, I3, P1, P2, P3, Q1, Q2, Q3, S1, S2, S3, PF1, PF2, PF3, F) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (int(round(time.time())),
                     meter4._MIC1__V1, meter4._MIC1__V2, meter4._MIC1__V3,
                     meter4._MIC1__I1, meter4._MIC1__I2, meter4._MIC1__I3,
                     meter4._MIC1__P1, meter4._MIC1__P2, meter4._MIC1__P3,
                     meter4._MIC1__Q1, meter4._MIC1__Q2, meter4._MIC1__Q3,
                     meter4._MIC1__S1, meter4._MIC1__S2, meter4._MIC1__S3,
                     meter4._MIC1__PF1, meter4._MIC1__PF2, meter4._MIC1__PF3,
                     meter4._MIC1__F))
        con_local.commit()
    else:
        print(">>Reading PT1, PT2, CT1 failed")
    #Read meter 5----------------------------------------------
    print("E5:")
    #Read PT1, PT2, CT1:
    readingPT1 = meter5.readPT1()
    readingPT2 = meter5.readPT2()
    readingCT1 = meter5.readCT1()
    #If there is no error, then continue
    if((readingPT1+readingPT2+readingCT1)==0):
        #Read PHASE VOLTAGE
        reading = meter5.readPhaseVoltage()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        V1: %.2f   V2: %.2f   V3: %.2f
        """%(meter5._MIC1__V1, meter5._MIC1__V2, meter5._MIC1__V3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read PHASE CURRENT
        reading = meter5.readPhaseCurrent()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        I1: %.2f   I2: %.2f   I3: %.2f
        """%(meter5._MIC1__I1, meter5._MIC1__I2, meter5._MIC1__I3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read PHASE POWER
        reading = meter5.readPhasePower()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        P1: %.2f   P2: %.2f   P3: %.2f
        """%(meter5._MIC1__P1, meter5._MIC1__P2, meter5._MIC1__P3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read REACTIVE POWER
        reading = meter5.readReactivePower()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        Q1: %.2f   Q2: %.2f   Q3: %.2f
        """%(meter5._MIC1__Q1, meter5._MIC1__Q2, meter5._MIC1__Q3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read APPARENT POWER
        reading = meter5.readApparentPower()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        S1: %.2f   S2: %.2f   S3: %.2f
        """%(meter5._MIC1__S1, meter5._MIC1__S2, meter5._MIC1__S3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read POWER FACTOR
        reading = meter5.readPowerFactor()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        PF1: %.2f   PF2: %.2f   PF3: %.2f
        """%(meter5._MIC1__PF1, meter5._MIC1__PF2, meter5._MIC1__PF3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read FREQUENCY
        reading = meter5.readFrequency()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        F: %.3f
        """%(meter5._MIC1__F)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        try:
            cur.execute("INSERT INTO Grid(Time, V1, V2, V3, I1, I2, I3, P1, P2, P3, Q1, Q2, Q3, S1, S2, S3, PF1, PF2, PF3, F) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (int(round(time.time())),
                         meter5._MIC1__V1, meter5._MIC1__V2, meter5._MIC1__V3,
                         meter5._MIC1__I1, meter5._MIC1__I2, meter5._MIC1__I3,
                         meter5._MIC1__P1, meter5._MIC1__P2, meter5._MIC1__P3,
                         meter5._MIC1__Q1, meter5._MIC1__Q2, meter5._MIC1__Q3,
                         meter5._MIC1__S1, meter5._MIC1__S2, meter5._MIC1__S3,
                         meter5._MIC1__PF1, meter5._MIC1__PF2, meter5._MIC1__PF3,
                         meter5._MIC1__F))
            con.commit()
        except  Exception as e:
             print (e)
        cur_local.execute("INSERT INTO Grid(Time, V1, V2, V3, I1, I2, I3, P1, P2, P3, Q1, Q2, Q3, S1, S2, S3, PF1, PF2, PF3, F) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (int(round(time.time())),
                     meter5._MIC1__V1, meter5._MIC1__V2, meter5._MIC1__V3,
                     meter5._MIC1__I1, meter5._MIC1__I2, meter5._MIC1__I3,
                     meter5._MIC1__P1, meter5._MIC1__P2, meter5._MIC1__P3,
                     meter5._MIC1__Q1, meter5._MIC1__Q2, meter5._MIC1__Q3,
                     meter5._MIC1__S1, meter5._MIC1__S2, meter5._MIC1__S3,
                     meter5._MIC1__PF1, meter5._MIC1__PF2, meter5._MIC1__PF3,
                     meter5._MIC1__F))
        con_local.commit()
    else:
        print(">>Reading PT1, PT2, CT1 failed")
    #Send data to broker after every 2*30=60s
    if ((time_send%2)==0):
#         dataSend = ""
#         cur.execute("SELECT * FROM meter1 ORDER BY No DESC LIMIT 1")
#         data = cur.fetchone()
#         dataSend += (str(data[2])+'%'+str(data[3])+'%'+str(data[4])+'%'+str(data[5])+'%'+str(data[6])+'%'+str(data[7])+'%'+str(data[8])+'%'+str(data[9])+'%'+str(data[10])+'%'+str(data[20])+'%'+str(data[1])+'%')   
#         cur.execute("SELECT * FROM meter2 ORDER BY No DESC LIMIT 1")
#         data = cur.fetchone()
#         dataSend += (str(data[2])+'%'+str(data[3])+'%'+str(data[4])+'%'+str(data[5])+'%'+str(data[6])+'%'+str(data[7])+'%'+str(data[8])+'%'+str(data[9])+'%'+str(data[10])+'%'+str(data[20])+'%'+str(data[1])+'%')
#         cur.execute("SELECT * FROM meter3 ORDER BY No DESC LIMIT 1")
#         data = cur.fetchone()
#         dataSend += (str(data[2])+'%'+str(data[3])+'%'+str(data[4])+'%'+str(data[5])+'%'+str(data[6])+'%'+str(data[7])+'%'+str(data[8])+'%'+str(data[9])+'%'+str(data[10])+'%'+str(data[20])+'%'+str(data[1])+'%')
#         cur.execute("SELECT * FROM meter4 ORDER BY No DESC LIMIT 1")
#         data = cur.fetchone()
#         dataSend += (str(data[2])+'%'+str(data[3])+'%'+str(data[4])+'%'+str(data[5])+'%'+str(data[6])+'%'+str(data[7])+'%'+str(data[8])+'%'+str(data[9])+'%'+str(data[10])+'%'+str(data[20])+'%'+str(data[1])+'%')
#         cur.execute("SELECT * FROM meter5 ORDER BY No DESC LIMIT 1")
#         data = cur.fetchone()
#         dataSend += (str(data[2])+'%'+str(data[3])+'%'+str(data[4])+'%'+str(data[5])+'%'+str(data[6])+'%'+str(data[7])+'%'+str(data[8])+'%'+str(data[9])+'%'+str(data[10])+'%'+str(data[20])+'%'+str(data[1])+'%')

        #-#New setpoint message generator for Current and number of used sockets only:
        try:
            cur.execute("SELECT I1, I2, I3 FROM PV ORDER BY No DESC LIMIT 1")
            data = cur.fetchone()
            setPoint = (data[0]+data[1]+data[2])
        
#         dataSend = [[data[0], data[1], data[2]]]
#         dataSend = {
#             "I1":data[0],
#             "I2":data[1],
#             "I3":data[2],
#             }
            cur_user.execute("SELECT socketId FROM users WHERE socketId IS NOT NULL")
            data = cur_user.fetchall()
        except  Exception as e:
            print (e)
            cur_local.execute("SELECT I1, I2, I3 FROM PV ORDER BY No DESC LIMIT 1")
            data = cur_local.fetchone()
            setPoint = (data[0]+data[1]+data[2])
            cur_user_local.execute("SELECT socketId FROM users WHERE socketId IS NOT NULL")
            data = cur_user_local.fetchall()
#         dataSend.update({"Sockets": len(data)})
        try:
            setPoint = int(setPoint / len(data) )
        except:
            setPoint = 0
            
        dataSend = {
            "setPoint":setPoint,
            }
        dataSend = json.dumps(dataSend)
        
        
        
        #-#Sending all meter data works perfectly with json instead of '%'
        #-#first
        #dataSend = [[data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[20], data[1]]]
        #-#all next appends '+='
        #dataSend.append([data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[20], data[1]])
        #-#lastly
        #dataSend = json.dumps(dataSend)
        
    #Example of old sent message
    #0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%1602066287%
    #0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%0%   #Meter2 always shows time=0 because it isnt connected
    #229.6%228.9%229.6%5.97%6.03%6.0%1350.0%1350.0%1350.0%50.0%1602066318%
    #0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%1602066318%
    #229.7%228.9%229.6%6.42%6.03%6.0%1440.0%1350.0%1350.0%50.0%1602066319%
      
        print("loop executed")
        #publish.single("HANevse/test2", "loop executed", qos= 2, retain=True, hostname=broker, auth={'username':"hanwatts", 'password':"controlsystem"})
        #publish.single("HANevse/EnergyMeter", dataSend, qos= 2, retain=False, hostname=broker)#, auth={'username':"hanwatts", 'password':"controlsystem"})
        
        client.publish("HANevse/energyMeter", dataSend, 2, False)
    
    time_send += 1
    #time.sleep(30)
    time.sleep(1)
