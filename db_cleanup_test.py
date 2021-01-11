import time
import sqlite3 as lite
#import json

current_time = int(time.time())
print(time.strftime('%Y-%m-%d %T', time.localtime(current_time)) )
#print(current_time[4:])
#print(type(current_time))
print(time.time() )


con = None
#path = "/home/pi/Documents/sql_databases/new_user_table.sqlite3"
path = "/home/pi/Documents/modbusData.db"
# path_local = "/media/DATABASE/usertable.sqlite3"

con = lite.connect(path)


#con = lite.connect(path)
cur = con.cursor()

#UserId = "66 FB 67 D9"
# UserId = "97 2D 39 5D" #real user in all tables
# 
# cur.execute("SELECT name, rowid FROM users WHERE uidTag = ? ", ("NO ID",) )
# dataUser = cur.fetchone()
# print(dataUser)
Table_NAME = "meter5"
Table_ColumnName = "No"
Value = 40000

cur.execute("DELETE FROM Grid WHERE No < 50000")
#try:
#    print(dataUser[1])
        
#     except:
#         print("WARNING: Unauthorized user charging at socket " + str(SocketID))
#         dataUser = ('unknown', 31)
con.commit()
con.close()