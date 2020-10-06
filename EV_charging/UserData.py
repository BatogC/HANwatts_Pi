#Author: Pham Minh Nhat (M.N.Pham)
#HAN University of Applied Science
#This library provides functions to check User ID
#or add a new ID to the database

User = open("/home/pi/Documents/EV_charging/User.txt","a+")
UserList = User.readlines()

def CheckID(sampleID):
    for ID in UserList:
        if ((sampleID + '\n') == ID):
            User.close()
            return True
    User.close()
    return False

def AddID(newID):
    User.write(newID)
    User.close()