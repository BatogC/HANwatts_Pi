import paho.mqtt.publish as publish
import time

while True:
    print("sending 0...")
    publish.single("ledStatus", "0", hostname="Kalin-PC")
    time.sleep(2)
    print("sending 1...")
    publish.single("ledStatus", "1", hostname="Kalin-PC")
    time.sleep(2)