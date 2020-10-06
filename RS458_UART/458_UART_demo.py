import RPi.GPIO as GPIO
import serial
import struct
import crcmod
from time import sleep

def read_Phase_Voltage(control, add = 0x01):

  #Calculate CRC16-MODBUS
  crc16 = crcmod.mkCrcFun(0x18005, rev = True, initCrc = 0xFFFF, xorOut = 0x0000)
  crc_Tx = ".%4x"%(crc16(serial.to_bytes([add,0x03,0x40,0x02,0x00,0x06])))
  #if the value is 10 for example, hex() returns 0xa, which is not expected (I want 0x0a).
  #Hence, I used String Formatting Operator.
  print (crc_Tx)
  #Send request
  GPIO.output(control, GPIO.HIGH)
  ser.write(serial.to_bytes([add,0x03,0x40,0x02,0x00,0x06,int(crc_Tx[3:],16),int(crc_Tx[1:3],16)]))

  #Wait for the converter to finish converting
  sleep(0.004)
        
  #Receive data
  GPIO.output(control, GPIO.LOW)
  
  #Wait for data
  cnt = 0
  data_left = ser.inWaiting()
  while (data_left == 0):
    cnt=cnt+1
    if (cnt < 50000):
      sleep(0.0001)
      data_left = ser.inWaiting()
    else:
      print("TransmittingError: Time out")
      return 999, 999, 999
      
  received_data = ser.read()
  sleep(0.03)
  data_left = ser.inWaiting()
  received_data += ser.read(data_left) 
  
  print(received_data)

  crc_cal = hex(crc16(received_data[:15]))
  crc_Rx = hex(struct.unpack('H',received_data[15:])[0])

  if crc_cal == crc_Rx:
    V1=struct.unpack('f',received_data[6:2:-1])[0]
    V2=struct.unpack('f',received_data[10:6:-1])[0]
    V3=struct.unpack('f',received_data[14:10:-1])[0]

    print("\nFinished transmitting")
    return V1, V2, V3
  else:
    print("Transmitting error: Incorrect CRC")
    return 999, 999, 999

#Pin definiyions
control_pin = 18

#Use BCM pin numbering
GPIO.setmode(GPIO.BCM)

#Turn off warnings
GPIO.setwarnings(False)

#Control pin as an output
GPIO.setup(control_pin, GPIO.OUT)

#Announcement
print("Program was written by P.M.Nhat")
print("ver 0.3")
print("Component: RS458 to UART converter")

#open .txt file
file=open("/home/pi/Documents/RS458_UART/RS458.txt","w")

#UART configuration
#8-bit data, no parity, 1 stop bit, 19200 BAUD
ser = serial.Serial("/dev/ttyS0", 19200)

V1,V2,V3 = read_Phase_Voltage(control_pin,0x01)
print (V1)
print (V2)
print (V3)
    
for hexchar in map(hex,bytearray(received_data)):
    file.write(hexchar+' ')

#close file
file.close()
print("Finished\n")
