# Raspberry Pi code

The Raspberry Pi subsystem software:	
The folder Modbus contains Modbus network-related files, while the userID contains the MQTT network and users database-related files.
The programs are written in Python 3.7.
## Welcome to the project!

#### ```/Modbus``` folder:  
This is the source folder that contains the firmware files for the Modbus part of the Pi. The 'main3.py' is the main script run at boot.
'MIC3.py' is the updated Python 3.7 library that contains the MIC1 and MIC2 energy meter classes and member functions needed by 'main3.py'.

#### ```/userID``` folder:
This is the source folder that contains the firmware files for the MQTT and user DB part of the Pi. The 'SQLfunction.py' is the main script run at boot.

## Executing the scripts

These programs are to be run from bash with 'python3 <filename>'. They are normally run at boot concurrently from their respective .sh scripts.
