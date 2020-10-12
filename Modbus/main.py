import RPi.GPIO as GPIO
import serial
import MIC
import time
#import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe
import sqlite3 as lite
import sys
import os
import json

broker = "localhost"
#broker = "tcp://127.0.0.1"
#broker = "broker.hivemq.com"
#path = "./modbusData.db" #Use internal memory
path = "/media/usb/modbusData.db" #Use external memory
con = lite.connect(path)
cur = con.cursor()

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
publish.single("HANevse/testmain", "Hello from main", qos= 2, retain=True, hostname=broker, auth={'username':"hanwatts", 'password':"controlsystem"})
#publish.single("HANevse/testmain", "Hello from main", hostname=broker)

print("Program was written by P.M.Nhat and C.Batog")
print("ver 2.5")
print("MODBUS converter: MAX485")
print("MODBUS slave: MIC1")

#Declare slave(s)
#meter1 = MIC.MIC2(0x01, control_pin)

meter1 = MIC.MIC1(0x01, control_pin)
meter2 = MIC.MIC1(0x02, control_pin)
meter3 = MIC.MIC1(0x03, control_pin)
meter4 = MIC.MIC1(0x04, control_pin)
meter5 = MIC.MIC1(0x05, control_pin)

#count to send new data after 1 min
time_send = 1

while True:
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
        S1: %.2f   S2: %.2f   S3: %.2f
        """%(meter1._MIC1__PF1, meter1._MIC1__PF2, meter1._MIC1__PF3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read FREQUENCY
        reading = meter1.readFrequency()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        F: %.2f
        """%(meter1._MIC1__F)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        cur.execute("INSERT INTO meter1(Time, V1, V2, V3, I1, I2, I3, P1, P2, P3, Q1, Q2, Q3, S1, S2, S3, PF1, PF2, PF3, F) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (int(round(time.time())),
                     meter1._MIC1__V1, meter1._MIC1__V2, meter1._MIC1__V3,
                     meter1._MIC1__I1, meter1._MIC1__I2, meter1._MIC1__I3,
                     meter1._MIC1__P1, meter1._MIC1__P2, meter1._MIC1__P3,
                     meter1._MIC1__Q1, meter1._MIC1__Q2, meter1._MIC1__Q3,
                     meter1._MIC1__S1, meter1._MIC1__S2, meter1._MIC1__S3,
                     meter1._MIC1__PF1, meter1._MIC1__PF2, meter1._MIC1__PF3,
                     meter1._MIC1__F))
        con.commit()
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
        S1: %.2f   S2: %.2f   S3: %.2f
        """%(meter2._MIC1__PF1, meter2._MIC1__PF2, meter2._MIC1__PF3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))            
        #Read FREQUENCY
        reading = meter2.readFrequency()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        F: %.2f
        """%(meter2._MIC1__F)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        cur.execute("INSERT INTO meter2(Time, V1, V2, V3, I1, I2, I3, P1, P2, P3, Q1, Q2, Q3, S1, S2, S3, PF1, PF2, PF3, F) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (int(round(time.time())),
                     meter2._MIC1__V1, meter2._MIC1__V2, meter2._MIC1__V3,
                     meter2._MIC1__I1, meter2._MIC1__I2, meter2._MIC1__I3,
                     meter2._MIC1__P1, meter2._MIC1__P2, meter2._MIC1__P3,
                     meter2._MIC1__Q1, meter2._MIC1__Q2, meter2._MIC1__Q3,
                     meter2._MIC1__S1, meter2._MIC1__S2, meter2._MIC1__S3,
                     meter2._MIC1__PF1, meter2._MIC1__PF2, meter2._MIC1__PF3,
                     meter2._MIC1__F))
        con.commit()
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
        S1: %.2f   S2: %.2f   S3: %.2f
        """%(meter3._MIC1__PF1, meter3._MIC1__PF2, meter3._MIC1__PF3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read FREQUENCY
        reading = meter3.readFrequency()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        F: %.2f
        """%(meter3._MIC1__F)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        cur.execute("INSERT INTO meter3(Time, V1, V2, V3, I1, I2, I3, P1, P2, P3, Q1, Q2, Q3, S1, S2, S3, PF1, PF2, PF3, F) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (int(round(time.time())),
                     meter3._MIC1__V1, meter3._MIC1__V2, meter3._MIC1__V3,
                     meter3._MIC1__I1, meter3._MIC1__I2, meter3._MIC1__I3,
                     meter3._MIC1__P1, meter3._MIC1__P2, meter3._MIC1__P3,
                     meter3._MIC1__Q1, meter3._MIC1__Q2, meter3._MIC1__Q3,
                     meter3._MIC1__S1, meter3._MIC1__S2, meter3._MIC1__S3,
                     meter3._MIC1__PF1, meter3._MIC1__PF2, meter3._MIC1__PF3,
                     meter3._MIC1__F))
        con.commit()
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
        S1: %.2f   S2: %.2f   S3: %.2f
        """%(meter4._MIC1__PF1, meter4._MIC1__PF2, meter4._MIC1__PF3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read FREQUENCY
        reading = meter4.readFrequency()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        F: %.2f
        """%(meter4._MIC1__F)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        cur.execute("INSERT INTO meter4(Time, V1, V2, V3, I1, I2, I3, P1, P2, P3, Q1, Q2, Q3, S1, S2, S3, PF1, PF2, PF3, F) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (int(round(time.time())),
                     meter4._MIC1__V1, meter4._MIC1__V2, meter4._MIC1__V3,
                     meter4._MIC1__I1, meter4._MIC1__I2, meter4._MIC1__I3,
                     meter4._MIC1__P1, meter4._MIC1__P2, meter4._MIC1__P3,
                     meter4._MIC1__Q1, meter4._MIC1__Q2, meter4._MIC1__Q3,
                     meter4._MIC1__S1, meter4._MIC1__S2, meter4._MIC1__S3,
                     meter4._MIC1__PF1, meter4._MIC1__PF2, meter4._MIC1__PF3,
                     meter4._MIC1__F))
        con.commit()
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
        S1: %.2f   S2: %.2f   S3: %.2f
        """%(meter5._MIC1__PF1, meter5._MIC1__PF2, meter5._MIC1__PF3)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        #Read FREQUENCY
        reading = meter5.readFrequency()
        if (reading == 0):
            current_time = time.ctime(time.time())
            Message = current_time + """
        F: %.2f
        """%(meter5._MIC1__F)
            print(Message)
        else:
            print("Measuring failed. Error code: " + str(reading))
        cur.execute("INSERT INTO meter5(Time, V1, V2, V3, I1, I2, I3, P1, P2, P3, Q1, Q2, Q3, S1, S2, S3, PF1, PF2, PF3, F) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (int(round(time.time())),
                     meter5._MIC1__V1, meter5._MIC1__V2, meter5._MIC1__V3,
                     meter5._MIC1__I1, meter5._MIC1__I2, meter5._MIC1__I3,
                     meter5._MIC1__P1, meter5._MIC1__P2, meter5._MIC1__P3,
                     meter5._MIC1__Q1, meter5._MIC1__Q2, meter5._MIC1__Q3,
                     meter5._MIC1__S1, meter5._MIC1__S2, meter5._MIC1__S3,
                     meter5._MIC1__PF1, meter5._MIC1__PF2, meter5._MIC1__PF3,
                     meter5._MIC1__F))
        con.commit()
    else:
        print(">>Reading PT1, PT2, CT1 failed")
    #Send data to broker after every 2*30=60s
    if ((time_send%2)==0):
        dataSend = ""
        cur.execute("SELECT * FROM meter1 ORDER BY No DESC LIMIT 1")
        data = cur.fetchone()
        dataSend += (str(data[2])+'%'+str(data[3])+'%'+str(data[4])+'%'+str(data[5])+'%'+str(data[6])+'%'+str(data[7])+'%'+str(data[8])+'%'+str(data[9])+'%'+str(data[10])+'%'+str(data[20])+'%'+str(data[1])+'%')   
        cur.execute("SELECT * FROM meter2 ORDER BY No DESC LIMIT 1")
        data = cur.fetchone()
        dataSend += (str(data[2])+'%'+str(data[3])+'%'+str(data[4])+'%'+str(data[5])+'%'+str(data[6])+'%'+str(data[7])+'%'+str(data[8])+'%'+str(data[9])+'%'+str(data[10])+'%'+str(data[20])+'%'+str(data[1])+'%')
        cur.execute("SELECT * FROM meter3 ORDER BY No DESC LIMIT 1")
        data = cur.fetchone()
        dataSend += (str(data[2])+'%'+str(data[3])+'%'+str(data[4])+'%'+str(data[5])+'%'+str(data[6])+'%'+str(data[7])+'%'+str(data[8])+'%'+str(data[9])+'%'+str(data[10])+'%'+str(data[20])+'%'+str(data[1])+'%')
        cur.execute("SELECT * FROM meter4 ORDER BY No DESC LIMIT 1")
        data = cur.fetchone()
        dataSend += (str(data[2])+'%'+str(data[3])+'%'+str(data[4])+'%'+str(data[5])+'%'+str(data[6])+'%'+str(data[7])+'%'+str(data[8])+'%'+str(data[9])+'%'+str(data[10])+'%'+str(data[20])+'%'+str(data[1])+'%')
        cur.execute("SELECT * FROM meter5 ORDER BY No DESC LIMIT 1")
        data = cur.fetchone()
        dataSend += (str(data[2])+'%'+str(data[3])+'%'+str(data[4])+'%'+str(data[5])+'%'+str(data[6])+'%'+str(data[7])+'%'+str(data[8])+'%'+str(data[9])+'%'+str(data[10])+'%'+str(data[20])+'%'+str(data[1])+'%')

        ##This works perfectly with json instead of '%'
        #first
        #dataSend = [[data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[1]]]
        #all next appends
        #dataSend.append([data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10], data[11], data[1]])
        #lastly
        #dataSend = json.dumps(dataSend)
        
    #Examples of sent messages
    #0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%1602066287%
    #0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%0%   #Meter2 always shows time=0 for some reason?
    #229.6%228.9%229.6%5.97%6.03%6.0%1350.0%1350.0%1350.0%50.0%1602066318%
    #0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%1602066318%
    #229.7%228.9%229.6%6.42%6.03%6.0%1440.0%1350.0%1350.0%50.0%1602066319%
        
    #0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%1602067570%
    #0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%0.0%0%
    #230.3%229.3%230.1%13.86%13.86%13.86%3180.0%3150.0%3180.0%50.0%1602067568%
    #0.0  %0.0  %0.0  %0.0  %0.0  %0.0  %0.0   %0.0   %0.0   %0.0 %1602067611%
    #230.4%229.3%230.1%14.91%13.89%13.86%3420.0%3180.0%3180.0%50.0%1602067569%
      
        print("loop executed")
        publish.single("HANevse/test2", "loop executed", qos= 2, retain=True, hostname=broker, auth={'username':"hanwatts", 'password':"controlsystem"})
        publish.single("HANevse/EnergyMeter", dataSend, qos= 2, retain=True, hostname=broker, auth={'username':"hanwatts", 'password':"controlsystem"})
        
    time_send += 1
    #time.sleep(30)
    time.sleep(1)