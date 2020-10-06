import random
import time
from azure.iot.device import IoTHubDeviceClient, Message

CONNECTION_STRING = "HostName=UbidotsHub.azure-devices.net;DeviceId=RaspberryPi;SharedAccessKey=oHGIIT8hYTL6Ii0WRPhDihh4KfKS3kYokSd94w5JCVQ="

TEMPERATURE=20.0
HUMIDITY=60
MSG_TXT='{{"temperature":{temperature},"humidity":{humidity}}}'

def iothub_client_init():
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client
    
def iothub_client_telemetry_sample_run():
    try:
        client = iothub_client_init()
        print("IoT Hub device sending periodicn messages, press Ctrl-C to exit")
        
        while True:
            temperature = TEMPERATURE + (random.random()*15)
            humidity = HUMIDITY + (random.random()*20)
            msg_txt_formatted = MSG_TXT.format(temperature=temperature, humidity=humidity)
            message = Message(msg_txt_formatted)
            
            print("Sending message: {}".format(message))
            client.send_message(message)
            print("Message sent")
            time.sleep(1)
    except KeyboardInterrupt:
        print("IoTHubClient sample stopped")
            
if(__name__=='__main__'):
    print("IoT Hub Quickstart#1-SImulated device")
    iothub_client_telemetry_sample_run()