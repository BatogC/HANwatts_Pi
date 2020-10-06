import RPi.GPIO as GPIO
import serial
import MIC2
import UserData
import time
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import paho.mqtt.subscribe as subscribe

broker = 'Kalin-PC'

err_cnt = 0

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.bad_connection_flag = False
        client.connected_flag = True
        print("Connected OK")
        err_cnt = 0
        client.subscribe("clientID")
    else:
        print("Bad connection, RC = ", rc)
        client.bad_connection_flag = True
        
def on_disconnect(client, userdata, rc):
    client.connected_flag = False
    if rc != 0:
        print("Unexpected disconnection.")
        client.bad_connection_flag = True        

def Sub_callback(client, userdata, message):
    print("%s: %s" % (message.topic, message.payload))
    if (UserData.CheckID(message.payload) == True):
        publish.single("IDStatus", "True", hostname=broker)
        print("ID exists")
    else:
        publish.single("IDStatus", "False", hostname=broker)
        print("ID does not exist")
        
V1=0.0
V2=0.0
V3=0.0

#setup mqtt
client = mqtt.Client()
client.connected_flag = False
client.bad_connection_flag = False
client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.connect_async(broker, 1883, 60)
client.message_callback_add("clientID", Sub_callback)
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
print("Program was written by P.M.Nhat")
print("ver 1.6")
print("MODBUS converter: MAX485")
print("MODBUS slave: MIC2-Mk II")
print("Broker: "+broker)
#open .txt file
MIC2data = open("/home/pi/Documents/EV_charging/MIC2.txt","w")

while True:
    
    if (client.bad_connection_flag == True):
        err_cnt += 1
        if (err_cnt >= 10):
            client.loop_stop()
            print("Client can't connect to broker.\nRestarting client.\n")
            client.disconnect()            
            client.connect_async(broker, 1883, 60)
            client.loop_start() 
    
    V1,V2,V3 = MIC2.read_Phase_Voltage(control_pin, 0x01)
    I1,I2,I3 = MIC2.read_Phase_Current(control_pin, 0x01)
    current_time = time.ctime(time.time())
    MIC2data.write(current_time + """
V1: %.2f   V2: %.2f   V3: %.2f   I1: %.2f   I2: %.2f   I3: %.2f
"""%(V1, V2, V3, I1, I2, I3))
    print("sending result to broker...")
    print("""
V1: %.2f
V2: %.2f
V3: %.2f"""%(V1, V2, V3))
    print("""
I1: %.2f
I2: %.2f
I3: %.2f"""%(I1, I2, I3))
    publish.single("V1", V1, hostname=broker)
    publish.single("V2", V2, hostname=broker)
    publish.single("V3", V3, hostname=broker)
    publish.single("I1", I1, hostname=broker)
    publish.single("I2", I2, hostname=broker)
    publish.single("I3", I3, hostname=broker)
    
    time.sleep(10)
  
    
