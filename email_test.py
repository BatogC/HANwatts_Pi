import smtplib, ssl
import sqlite3 as lite


port = 465  # For SSL
smtp_server = "smtp.gmail.com"
sender_email = "tpi97364@gmail.com"  # Enter your address
receiver_email = ""  # Enter receiver address
password = "controlsystem" #input("Type your password and press enter: ")
message = """\
Subject: Unplug car

Please unplug your car from the EV charger. 4 hours have passed since it was plugged in.

This message was sent automatically. Please do not reply."""

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message)
    
print("Sent mail")

con = None

#path = "./userList" #Use internal memory - old DB
path_local = "/media/DATABASE/check_usertable.sqlite3" #Use external memory = new_user_table
path = "/mnt/dav/Data/check_usertable.sqlite3" #Use cloud storage

try:
    con = lite.connect(path)
except:
    path = path_local
    con = lite.connect(path)
    
cur = con.cursor()
cur.execute("SELECT * FROM measurements ORDER BY rowid DESC LIMIT 1")
dataRef1 = cur.fetchone()
print(dataRef1)

cur.execute("SELECT LastStartOrStop, socketId FROM users WHERE uidTag=? LIMIT 1", (UserId,))
dataUser = cur.fetchone() # returns a tuple
dataSend = str(socketId) + ";"
    
cur.execute("SELECT socketId FROM users WHERE socketId=? LIMIT 1", (socketId,))
socketUsed = cur.fetchone()
#The socketUsed can be either None or the socket number, so parsing it can give error without check
    
