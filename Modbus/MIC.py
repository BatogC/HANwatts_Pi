import struct
import crcmod
import serial
import RPi.GPIO as GPIO
from time import sleep

#This library is made for reading MIC/MIC2 energy meter with a MAX485 module
#MIC2 only read data from registers. This is not the correct value.
#To calculate correct value, PT1, PT2, CT1 need to be read. Please take MIC1 as an example

#UART configuration
#MIC2: 8-bit data, no parity, 1 stop bit, 19200 BAUD
#ser = serial.Serial("/dev/ttyS0", 9200)

#MIC1: 8-bit data, no parity, 1 stop bit, 38400 BAUD
ser = serial.Serial("/dev/ttyS0", 38400)

#return code:
Data_error  = -3
CRC_error   = -2
Trans_error = -1
No_error    = 0

class MIC2:
    def __init__(self, Id, Control):
        self.__Control = Control
        self.__Address = Id
        self.__V1 = 0
        self.__V2 = 0
        self.__V3 = 0
        self.__I1 = 0
        self.__I2 = 0
        self.__I3 = 0
        self.__P1 = 0
        self.__P2 = 0
        self.__P3 = 0
        self.__F  = 0
        
    def readPhaseVoltage(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x40, 0x02, 0x00, 0x06])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x40, 0x02, 0x00, 0x06, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.004)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
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
                return Trans_error
    
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
        
        if (ord(received_data[0]) != self.__Address):
            print("Transmitting error: Data corrupted")
            return Data_error
        
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:15]))
        
        #print (crc_cal) #use for debugging only
    
        crc_Rx = hex(struct.unpack('H',received_data[15:])[0])
    
        #print (crc_Rx) #use for degugging only
    
        if crc_cal == crc_Rx:
            self.__V1 = struct.unpack('f', received_data[6:2:-1])[0]
            self.__V2 = struct.unpack('f', received_data[10:6:-1])[0]
            self.__V3 = struct.unpack('f', received_data[14:10:-1])[0]
            return No_error
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error
            
    def readPhaseCurrent(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x40, 0x12, 0x00, 0x06])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x40, 0x12, 0x00, 0x06, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.004)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
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
                return Trans_error
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
        
        if (ord(received_data[0]) != self.__Address):
            print("Transmitting error: Data corrupted")
            return Data_error
    
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:15]))
        crc_Rx = hex(struct.unpack('H',received_data[15:])[0])
    
        if crc_cal == crc_Rx:
            self.__I1 = struct.unpack('f', received_data[6:2:-1])[0]
            self.__I2 = struct.unpack('f', received_data[10:6:-1])[0]
            self.__I3 = struct.unpack('f', received_data[14:10:-1])[0]      
            return No_error
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error
            
    def readPhasePower(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x40, 0x1c, 0x00, 0x06])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x40, 0x1c, 0x00, 0x06, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.004)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
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
                return Trans_error
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
        
        if (ord(received_data[0]) != self.__Address):
            print("Transmitting error: Data corrupted")
            return Data_error
    
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:15]))
        crc_Rx = hex(struct.unpack('H',received_data[15:])[0])
    
        if crc_cal == crc_Rx:
            self.__P1 = struct.unpack('f', received_data[6:2:-1])[0]
            self.__P2 = struct.unpack('f', received_data[10:6:-1])[0]
            self.__P3 = struct.unpack('f', received_data[14:10:-1])[0]       
            return No_error
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error

    def readFrequency(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x40, 0x00, 0x00, 0x02])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x40, 0x00, 0x00, 0x02, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.004)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
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
                return Trans_error
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
        
        if (ord(received_data[0]) != self.__Address):
            print("Transmitting error: Data corrupted")
            return Data_error
    
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:7]))
        crc_Rx = hex(struct.unpack('H',received_data[7:])[0])
    
        if crc_cal == crc_Rx:
            self.__F = struct.unpack('f', received_data[6:2:-1])[0]    
            return No_error
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error
#---------------------------------END OF MIC2------------------------------------
#--------------------------------------------------------------------------------
  
class MIC1:
    def __init__(self, Id, Control):
        self.__Control = Control
        self.__Address = Id
        self.__PT1 = 1.0
        self.__PT2 = 1.0
        self.__CT1 = 1.0
        self.__V1 = 0.0
        self.__V2 = 0.0
        self.__V3 = 0.0
        self.__I1 = 0.0
        self.__I2 = 0.0
        self.__I3 = 0.0
        self.__P1 = 0.0
        self.__P2 = 0.0
        self.__P3 = 0.0
        self.__Q1 = 0.0
        self.__Q2 = 0.0
        self.__Q3 = 0.0
        self.__S1 = 0.0
        self.__S2 = 0.0
        self.__S3 = 0.0
        self.__PF1 = 0.0
        self.__PF2 = 0.0
        self.__PF3 = 0.0
        self.__F  = 0.0
    
    def readPT1(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x01, 0x05, 0x00, 0x02])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x01, 0x05, 0x00, 0x02, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.01)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
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
                return Trans_error
    
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
        
        #Check if the data is correct
        if (ord(received_data[0]) != self.__Address):
            print("Transmitting error: Data corrupted")
            return Data_error
        if (len(received_data) != 9):
            print("Transmitting error: Data corrupted")
            return Data_error
        
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:7]))

        #DEBUG ONLY-----------------------------------------------
        #retval = ""
        #for character in received_data:
        #    retval += ('0123456789ABCDEF'[int(ord(character)/16)])
        #    retval += ('0123456789ABCDEF'[int(ord(character)%16)])
        #    retval += ':'
        #print (retval[:-1])
        #print (crc_cal) #use for debugging only
        #---------------------------------------------------------
    
        crc_Rx = hex(struct.unpack('H',received_data[7:])[0])
    
        #print (crc_Rx) #use for degugging only
    
        if crc_cal == crc_Rx:
            self.__PT1 = float(struct.unpack('I', received_data[6:2:-1])[0])
            return No_error
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error
    
    def readPT2(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x01, 0x07, 0x00, 0x01])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x01, 0x07, 0x00, 0x01, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.01)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
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
                return Trans_error
    
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
        
        #Check if the data is correct
        if (ord(received_data[0]) != self.__Address):
            print("Transmitting error: Data corrupted")
            return Data_error
        if (len(received_data) != 7):
            print("Transmitting error: Data corrupted")
            return Data_error
        
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:5]))

        #DEBUG ONLY-----------------------------------------------
        #retval = ""
        #for character in received_data:
        #    retval += ('0123456789ABCDEF'[int(ord(character)/16)])
        #    retval += ('0123456789ABCDEF'[int(ord(character)%16)])
        #    retval += ':'
        #print (retval[:-1])
        #print (crc_cal) #use for debugging only
        #---------------------------------------------------------
    
        crc_Rx = hex(struct.unpack('H',received_data[5:])[0])
    
        #print (crc_Rx) #use for degugging only
    
        if crc_cal == crc_Rx:
            self.__PT2 = float(struct.unpack('H', received_data[4:2:-1])[0])
            return No_error
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error
    
    def readCT1(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x01, 0x08, 0x00, 0x01])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x01, 0x08, 0x00, 0x01, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.01)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
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
                return Trans_error
    
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
        
        #Check if the data is correct
        if (ord(received_data[0]) != self.__Address):
            print("Transmitting error: Data corrupted")
            return Data_error
        if (len(received_data) != 7):
            print("Transmitting error: Data corrupted")
            return Data_error
        
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:5]))

        #DEBUG ONLY-----------------------------------------------
        #retval = ""
        #for character in received_data:
        #    retval += ('0123456789ABCDEF'[int(ord(character)/16)])
        #    retval += ('0123456789ABCDEF'[int(ord(character)%16)])
        #    retval += ':'
        #print (retval[:-1])
        #print (crc_cal) #use for debugging only
        #---------------------------------------------------------
    
        crc_Rx = hex(struct.unpack('H',received_data[5:])[0])
    
        #print (crc_Rx) #use for degugging only
    
        if crc_cal == crc_Rx:
            self.__CT1 = float(struct.unpack('H', received_data[4:2:-1])[0])
            return No_error
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error
    
    def readPhaseVoltage(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x01, 0x31, 0x00, 0x03])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x01, 0x31, 0x00, 0x03, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.01)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
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
                return Trans_error
    
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
        
        #Check if the data is correct
        if (ord(received_data[0]) != self.__Address):
            print("Transmitting error: Data corrupted")
            return Data_error
        if (len(received_data) != 11):
            print("Transmitting error: Data corrupted")
            return Data_error
        
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:9]))

        #DEBUG ONLY-----------------------------------------------
        #retval = ""
        #for character in received_data:
        #    retval += ('0123456789ABCDEF'[int(ord(character)/16)])
        #    retval += ('0123456789ABCDEF'[int(ord(character)%16)])
        #    retval += ':'
        #print (retval[:-1])
        #print (crc_cal) #use for debugging only
        #---------------------------------------------------------
    
        crc_Rx = hex(struct.unpack('H',received_data[9:])[0])
    
        #print (crc_Rx) #use for degugging only
    
        if crc_cal == crc_Rx:
            self.__V1 = float(struct.unpack('H', received_data[4:2:-1])[0])*(self.__PT1/self.__PT2)/10
            self.__V2 = float(struct.unpack('H', received_data[6:4:-1])[0])*(self.__PT1/self.__PT2)/10
            self.__V3 = float(struct.unpack('H', received_data[8:6:-1])[0])*(self.__PT1/self.__PT2)/10
            return No_error
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error
            
    def readPhaseCurrent(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x01, 0x39, 0x00, 0x03])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x01, 0x39, 0x00, 0x03, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.01)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
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
                return Trans_error
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
        
        if (ord(received_data[0]) != self.__Address):
            print("Transmitting error: Data corrupted")
            return Data_error
        if (len(received_data) != 11):
            print("Transmitting error: Data corrupted")
            return Data_error
    
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:9]))
        crc_Rx = hex(struct.unpack('H',received_data[9:])[0])
    
        if crc_cal == crc_Rx:
            self.__I1 = float(struct.unpack('H', received_data[4:2:-1])[0])*(self.__CT1/5)/1000
            self.__I2 = float(struct.unpack('H', received_data[6:4:-1])[0])*(self.__CT1/5)/1000
            self.__I3 = float(struct.unpack('H', received_data[8:6:-1])[0])*(self.__CT1/5)/1000   
            return No_error
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error
            
    def readPhasePower(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x01, 0x3E, 0x00, 0x03])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x01, 0x3E, 0x00, 0x03, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.01)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
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
                return Trans_error
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
        
        if (ord(received_data[0]) != self.__Address):
            print("Transmitting error: Data corrupted")
            return Data_error
        if (len(received_data) != 11):
            print("Transmitting error: Data corrupted")
            return Data_error
        
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:9]))
        crc_Rx = hex(struct.unpack('H',received_data[9:])[0])
    
        if crc_cal == crc_Rx:
            self.__P1 = float(struct.unpack('h', received_data[4:2:-1])[0])*(self.__PT1/self.__PT2)*(self.__CT1/5)
            self.__P2 = float(struct.unpack('h', received_data[6:4:-1])[0])*(self.__PT1/self.__PT2)*(self.__CT1/5)
            self.__P3 = float(struct.unpack('h', received_data[8:6:-1])[0])*(self.__PT1/self.__PT2)*(self.__CT1/5)    
            return No_error
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error

        
    def readReactivePower(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x01, 0x42, 0x00, 0x03])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x01, 0x42, 0x00, 0x03, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.01)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
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
                return Trans_error
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
        
        if (ord(received_data[0]) != self.__Address):
            print("Transmitting error: Data corrupted")
            return Data_error
        if (len(received_data) != 11):
            print("Transmitting error: Data corrupted")
            return Data_error
        
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:9]))
        crc_Rx = hex(struct.unpack('H',received_data[9:])[0])
    
        if crc_cal == crc_Rx:
            self.__Q1 = float(struct.unpack('h', received_data[4:2:-1])[0])*(self.__PT1/self.__PT2)*(self.__CT1/5)
            self.__Q2 = float(struct.unpack('h', received_data[6:4:-1])[0])*(self.__PT1/self.__PT2)*(self.__CT1/5)
            self.__Q3 = float(struct.unpack('h', received_data[8:6:-1])[0])*(self.__PT1/self.__PT2)*(self.__CT1/5)    
            return No_error
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error
        
        
    def readApparentPower(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x01, 0x46, 0x00, 0x03])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x01, 0x46, 0x00, 0x03, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.01)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
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
                return Trans_error
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
        
        if (ord(received_data[0]) != self.__Address):
            print("Transmitting error: Data corrupted")
            return Data_error
        if (len(received_data) != 11):
            print("Transmitting error: Data corrupted")
            return Data_error
        
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:9]))
        crc_Rx = hex(struct.unpack('H',received_data[9:])[0])
    
        if crc_cal == crc_Rx:
            self.__S1 = float(struct.unpack('h', received_data[4:2:-1])[0])*(self.__PT1/self.__PT2)*(self.__CT1/5)
            self.__S2 = float(struct.unpack('h', received_data[6:4:-1])[0])*(self.__PT1/self.__PT2)*(self.__CT1/5)
            self.__S3 = float(struct.unpack('h', received_data[8:6:-1])[0])*(self.__PT1/self.__PT2)*(self.__CT1/5)    
            return No_error
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error
        
    def readPowerFactor(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x01, 0x4A, 0x00, 0x03])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x01, 0x4A, 0x00, 0x03, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait before reading the result
        sleep(0.01)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
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
                return Trans_error
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
        
        if (ord(received_data[0]) != self.__Address):
            print("Transmitting error: Data corrupted")
            return Data_error
        if (len(received_data) != 11):
            print("Transmitting error: Data corrupted")
            return Data_error
        
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:9]))
        crc_Rx = hex(struct.unpack('H',received_data[9:])[0])
    
        if crc_cal == crc_Rx:
            self.__PF1 = float(struct.unpack('h', received_data[4:2:-1])[0])/1000
            self.__PF2 = float(struct.unpack('h', received_data[6:4:-1])[0])/1000
            self.__PF3 = float(struct.unpack('h', received_data[8:6:-1])[0])/1000    
            return No_error
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error 
            
    def readFrequency(self):
        #Calculate CRC16-MODBUS
        crc16 = crcmod.mkCrcFun(0x18005, rev=True, initCrc = 0xFFFF, xorOut = 0x0000)
        crc_Tx = ".%4x"%(crc16(serial.to_bytes([self.__Address, 0x03, 0x01, 0x30, 0x00, 0x01])))
        #The crc_Tx must include 4 hexadecimal characters.
        #If crc_Tx =  10, function hex() will return 0xa, which is not expected
        #Therefore, String format operator was used
    
        #Send request
        GPIO.output(self.__Control, GPIO.HIGH)
        ser.write(serial.to_bytes([self.__Address, 0x03, 0x01, 0x30, 0x00, 0x01, int(crc_Tx[3:],16), int(crc_Tx[1:3],16)]))
    
        #There is a delay caused by the converter. The program must wait hbefore reading the result
        sleep(0.01)
    
        #Receive data
        GPIO.output(self.__Control, GPIO.LOW)
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
                return Trans_error
        received_data = ser.read()
        sleep(0.01)
        data_left = ser.inWaiting()
        received_data += ser.read(data_left)
        
        #DEBUG ONLY-----------------------------------------------
        #retval = ""
        #for character in received_data:
        #    retval += ('0123456789ABCDEF'[int(ord(character)/16)])
        #    retval += ('0123456789ABCDEF'[int(ord(character)%16)])
        #    retval += ':'
        #print (retval[:-1])
        #print (crc_cal) #use for debugging only
        #---------------------------------------------------------

        if (ord(received_data[0]) != self.__Address):
            print("Transmitting error: Data corrupted")
            return Data_error
        if (len(received_data) != 7):
            print("Transmitting error: Data corrupted")
            return Data_error
    
        #Check the CRC code
        crc_cal = hex(crc16(received_data[:5]))
        crc_Rx = hex(struct.unpack('H',received_data[5:])[0])
        
        if crc_cal == crc_Rx:
            self.__F = float(struct.unpack('H', received_data[4:2:-1])[0])/100    
            return No_error
        else:
            print("Transmitting error: Incorrect CRC")
            return CRC_error
#---------------------------------END OF MIC1------------------------------------
#--------------------------------------------------------------------------------
