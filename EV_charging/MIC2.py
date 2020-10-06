#Author: Pham Minh Nhat (M.N.Pham)
#HAN University of Applied Science
#Version: 2.0
#Add functions for MIC1 energy meter, uncomment them to use.
#----------------------------------------------------------
#CAUTION: Code for MIC1 have NOT been tested. In case there
#are errors, please fix them regarding to the MODBUS manual
#of the energy meter.
#----------------------------------------------------------
#In case of using another MODBUS energy meter, please
#change the register address due to the datasheet of the
#device.

#This library must be installed together with packages and
#modules below.

import struct
import crcmod
import serial
import RPi.GPIO as GPIO
from time import sleep

#UART configuration
#8-bit data, no parity, 1 stop bit, 19200 BAUD
ser = serial.Serial("/dev/ttyS0", 19200)

#This function send request to the MIC2 and wait for the value of Phase Voltage (V1, V2, V3)
#control is the control pin of the MODBUS-TTL converter
#add is the ID of the MODBUS slave. add = 0x01 by default
def read_Phase_Voltage(control, add = 0x01):
    #Calculate CRC16-MODBUS
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
    #For MIC2-Mk II:
    crc_Tx = ".%4x"%(crc16(serial.to_bytes([add, 0x03, 0x40, 0x02, 0x00, 0x06])))
    #For MIC:
    #crc_Tx = ".%4x"%(crc16(serial.to_bytes([add, 0x03, 0x01, 0x31, 0x00, 0x03])))
    
    #The crc_Tx must include 4 hexadecimal characters.
    #If crc_Tx =  10, function hex() will return 0xa, which is not expected
    #Therefore, String format operator was used
    
    #Send request
    GPIO.output(control, GPIO.HIGH)
    #For MIC2-Mk II:
    ser.write(serial.to_bytes([add, 0x03, 0x40, 0x02, 0x00, 0x06, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    #For MIC:
    #ser.write(serial.to_bytes([add, 0x03, 0x01, 0x31, 0x00, 0x03, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
    #There is a delay caused by the converter. The program must wait before reading the result
    sleep(0.004)
    
    #Receive data
    GPIO.output(control, GPIO.LOW)
    cnt = 0
    data_left = ser.inWaiting()
    while (data_left == 0):
        #wait for data
        cnt=cnt+1
        if (cnt < 50000): #wait for maximum 5 seconds
            sleep(0.0001)
            data_left = ser.inWaiting()
        else:
            print("Transmitting error: Time out")
            return 999, 999, 999
    
    received_data = ser.read()
    sleep(0.01)
    data_left = ser.inWaiting()
    received_data += ser.read(data_left)
    #Check the CRC code
    #For MIC2-Mk II:
    crc_cal = hex(crc16(received_data[:15]))
    #For MIC:
    #crc_cal = hex(crc16(received_data[:9]))
    
    #print (crc_cal) #use for debugging only
    
    #For MIC2-Mk II:
    crc_Rx = hex(struct.unpack('H',received_data[15:])[0])
    #For MIC:
    #crc_Rx = hex(struct.unpack('H',received_data[9:])[0])
    
    #print (crc_Rx) #use for degugging only
    
    if crc_cal == crc_Rx:
        #For MIC2-Mk II:
        V1 = struct.unpack('f', received_data[6:2:-1])[0]
        V2 = struct.unpack('f', received_data[10:6:-1])[0]
        V3 = struct.unpack('f', received_data[14:10:-1])[0]
        #For MIC:
        #V1 = struct.unpack('f', received_data[4:2:-1])[0]
        #V2 = struct.unpack('f', received_data[6:4:-1])[0]
        #V3 = struct.unpack('f', received_data[8:6:-1])[0]
        return V1, V2, V3
    else:
        print("Transmitting error: Incorrect CRC")
        return 999, 999, 999
    
#This function send request to the MIC2 and wait for the value of Phase Current (I1, I2, I3)
#control is the control pin of the MODBUS-TTL converter
#add is the ID of the MODBUS slave. add = 0x01 by default
def read_Phase_Current(control, add = 0x01):
    #Calculate CRC16-MODBUS
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
    crc_Tx = ".%4x"%(crc16(serial.to_bytes([add, 0x03, 0x40, 0x12, 0x00, 0x06])))
    #The crc_Tx must include 4 hexadecimal characters.
    #If crc_Tx =  10, function hex() will return 0xa, which is not expected
    #Therefore, String format operator was used
    
    #Send request
    GPIO.output(control, GPIO.HIGH)
    ser.write(serial.to_bytes([add, 0x03, 0x40, 0x12, 0x00, 0x06, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
    #There is a delay caused by the converter. The program must wait before reading the result
    sleep(0.004)
    
    #Receive data
    GPIO.output(control, GPIO.LOW)
    cnt = 0
    data_left = ser.inWaiting()
    while (data_left == 0):
        #wait for data
        cnt=cnt+1
        if (cnt < 50000): #wait for maximum 5 seconds
            sleep(0.0001)
            data_left = ser.inWaiting()
        else:
            print("Transmitting error: Time out")
            return 999, 999, 999
    received_data = ser.read()
    sleep(0.01)
    data_left = ser.inWaiting()
    received_data += ser.read(data_left)
    
    #Check the CRC code
    crc_cal = hex(crc16(received_data[:15]))
    crc_Rx = hex(struct.unpack('H',received_data[15:])[0])
    
    if crc_cal == crc_Rx:
        I1 = struct.unpack('f', received_data[6:2:-1])[0]
        I2 = struct.unpack('f', received_data[10:6:-1])[0]
        I3 = struct.unpack('f', received_data[14:10:-1])[0]
        
        return I1, I2, I3
    else:
        print("Transmitting error: Incorrect CRC")
        return 999, 999, 999
        
#This function send request to the MIC2 and wait for the value of Phase Power (P1, P2, P3)
#control is the control pin of the MODBUS-TTL converter
#add is the ID of the MODBUS slave. add = 0x01 by default
def read_Phase_Power(control, add = 0x01):
    #Calculate CRC16-MODBUS
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
    crc_Tx = ".%4x"%(crc16(serial.to_bytes([add, 0x03, 0x40, 0x1c, 0x00, 0x06])))
    #The crc_Tx must include 4 hexadecimal characters.
    #If crc_Tx =  10, function hex() will return 0xa, which is not expected
    #Therefore, String format operator was used
    
    #Send request
    GPIO.output(control, GPIO.HIGH)
    ser.write(serial.to_bytes([add, 0x03, 0x40, 0x1c, 0x00, 0x06, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
    #There is a delay caused by the converter. The program must wait before reading the result
    sleep(0.004)
    
    #Receive data
    GPIO.output(control, GPIO.LOW)
    cnt = 0
    data_left = ser.inWaiting()
    while (data_left == 0):
        #wait for data
        cnt=cnt+1
        if (cnt < 50000): #wait for maximum 5 seconds
            sleep(0.0001)
            data_left = ser.inWaiting()
        else:
            print("Transmitting error: Time out")
            return 999, 999, 999
    received_data = ser.read()
    sleep(0.01)
    data_left = ser.inWaiting()
    received_data += ser.read(data_left)
    
    #Check the CRC code
    crc_cal = hex(crc16(received_data[:15]))
    crc_Rx = hex(struct.unpack('H',received_data[15:])[0])
    
    if crc_cal == crc_Rx:
        P1 = struct.unpack('f', received_data[6:2:-1])[0]
        P2 = struct.unpack('f', received_data[10:6:-1])[0]
        P3 = struct.unpack('f', received_data[14:10:-1])[0]
        
        return P1, P2, P3
    else:
        print("Transmitting error: Incorrect CRC")
        return 999, 999, 999
        
#This function send request to the MIC2 and wait for the value of Phase Reactive Power (Q1, Q2, Q3)
#control is the control pin of the MODBUS-TTL converter
#add is the ID of the MODBUS slave. add = 0x01 by default
def read_Phase_RPower(control, add = 0x01):
    #Calculate CRC16-MODBUS
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
    crc_Tx = ".%4x"%(crc16(serial.to_bytes([add, 0x03, 0x40, 0x24, 0x00, 0x06])))
    #The crc_Tx must include 4 hexadecimal characters.
    #If crc_Tx =  10, function hex() will return 0xa, which is not expected
    #Therefore, String format operator was used
    
    #Send request
    GPIO.output(control, GPIO.HIGH)
    ser.write(serial.to_bytes([add, 0x03, 0x40, 0x24, 0x00, 0x06, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
    #There is a delay caused by the converter. The program must wait before reading the result
    sleep(0.004)
    
    #Receive data
    GPIO.output(control, GPIO.LOW)
    cnt = 0
    data_left = ser.inWaiting()
    while (data_left == 0):
        #wait for data
        cnt=cnt+1
        if (cnt < 50000): #wait for maximum 5 seconds
            sleep(0.0001)
            data_left = ser.inWaiting()
        else:
            print("Transmitting error: Time out")
            return 999, 999, 999
    received_data = ser.read()
    sleep(0.01)
    data_left = ser.inWaiting()
    received_data += ser.read(data_left)
    
    #Check the CRC code
    crc_cal = hex(crc16(received_data[:15]))
    crc_Rx = hex(struct.unpack('H',received_data[15:])[0])
    
    if crc_cal == crc_Rx:
        Q1 = struct.unpack('f', received_data[6:2:-1])[0]
        Q2 = struct.unpack('f', received_data[10:6:-1])[0]
        Q3 = struct.unpack('f', received_data[14:10:-1])[0]
        
        return Q1, Q2, Q3
    else:
        print("Transmitting error: Incorrect CRC")
        return 999, 999, 999
        
#This function send request to the MIC2 and wait for the value of Phase Apparent Power (S1, S2, S3)
#control is the control pin of the MODBUS-TTL converter
#add is the ID of the MODBUS slave. add = 0x01 by default
def read_Phase_APower(control, add = 0x01):
    #Calculate CRC16-MODBUS
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
    crc_Tx = ".%4x"%(crc16(serial.to_bytes([add, 0x03, 0x40, 0x2c, 0x00, 0x06])))
    #The crc_Tx must include 4 hexadecimal characters.
    #If crc_Tx =  10, function hex() will return 0xa, which is not expected
    #Therefore, String format operator was used
    
    #Send request
    GPIO.output(control, GPIO.HIGH)
    ser.write(serial.to_bytes([add, 0x03, 0x40, 0x2c, 0x00, 0x06, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
    #There is a delay caused by the converter. The program must wait before reading the result
    sleep(0.004)
    
    #Receive data
    GPIO.output(control, GPIO.LOW)
    cnt = 0
    data_left = ser.inWaiting()
    while (data_left == 0):
        #wait for data
        cnt=cnt+1
        if (cnt < 50000): #wait for maximum 5 seconds
            sleep(0.0001)
            data_left = ser.inWaiting()
        else:
            print("Transmitting error: Time out")
            return 999, 999, 999
    received_data = ser.read()
    sleep(0.01)
    data_left = ser.inWaiting()
    received_data += ser.read(data_left)
    
    #Check the CRC code
    crc_cal = hex(crc16(received_data[:15]))
    crc_Rx = hex(struct.unpack('H',received_data[15:])[0])
    
    if crc_cal == crc_Rx:
        S1 = struct.unpack('f', received_data[6:2:-1])[0]
        S2 = struct.unpack('f', received_data[10:6:-1])[0]
        S3 = struct.unpack('f', received_data[14:10:-1])[0]
        
        return S1, S2, S3
    else:
        print("Transmitting error: Incorrect CRC")
        return 999, 999, 999
    
#This function send request to the MIC2 and wait for the value of Energy (E)
#control is the control pin of the MODBUS-TTL converter
#add is the ID of the MODBUS slave. add = 0x01 by default
def read_Energy(control, add = 0x01):
    #Calculate CRC16-MODBUS
    crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
    crc_Tx = ".%4x"%(crc16(serial.to_bytes([add, 0x03, 0x40, 0x50, 0x00, 0x02])))
    #The crc_Tx must include 4 hexadecimal characters.
    #If crc_Tx =  10, function hex() will return 0xa, which is not expected
    #Therefore, String format operator was used
    
    #Send request
    GPIO.output(control, GPIO.HIGH)
    ser.write(serial.to_bytes([add, 0x03, 0x40, 0x50, 0x00, 0x02, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
    #There is a delay caused by the converter. The program must wait before reading the result
    sleep(0.004)
    
    #Receive data
    GPIO.output(control, GPIO.LOW)
    cnt = 0
    data_left = ser.inWaiting()
    while (data_left == 0):
        #wait for data
        cnt=cnt+1
        if (cnt < 50000): #wait for maximum 5 seconds
            sleep(0.0001)
            data_left = ser.inWaiting()
        else:
            print("Transmitting error: Time out")
            return 999, 999, 999
    received_data = ser.read()
    sleep(0.01)
    data_left = ser.inWaiting()
    received_data += ser.read(data_left)
    
    #Check the CRC code
    crc_cal = hex(crc16(received_data[:7]))
    crc_Rx = hex(struct.unpack('H',received_data[7:])[0])
    
    if crc_cal == crc_Rx:
        E = struct.unpack('I', received_data[6:2:-1])[0]        
        return E
    else:
        print("Transmitting error: Incorrect CRC")
        return 999
        
