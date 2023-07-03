import os
import time

class RfidManager:
    def __init__(self) -> None:
        self.userId = None
        
        if os.name == "nt":
            self.isWindows = True
            return
        self.isWindows = False
        
        import RPi.GPIO as GPIO
        from mfrc522 import SimpleMFRC522
        GPIO.setwarnings(False)
        self.rfid = SimpleMFRC522()


    def ScanId(self):
        self.userId = None

        timeEnd = time.time() + 5
        
        while time.time() < timeEnd:
            if self.isWindows:
                self.userId = "6339848505320"

                print("No RFID Scanner found. \n Posting user ID: " + self.userId)
                return
                
            id,text = self.rfid.read()
            self.userId = self.CheckID(id)
            
            print("Scanned user ID: " + self.userId)
            
            if id != None:
                return
        
        if self.userId == None:
            self.userId = "0"
        
            
    
    def CheckId(self, userId: str):
        if len(userId) < 10:
            return "0"
        return userId
    
    
    def CheckPermission(self, userId: str):
        adminList = self.GetAdminList()
        
        for id in adminList:
            if id == userId:
                return True
        return False
    
    
    def AddPermission(self, userId: str):
        adminList = self.GetAdminList()
        
        adminList.append(userId)
        
        with open("administrators.txt", "w") as output:
            output.write(str(adminList))
        print(userId + " was successfully added to the Administrator list.")
    
    
    def GetAdminList(self):
        if not os.path.isfile("administrators.txt"):
            open("administrators.txt", "x")
        adminList = open("administrators.txt", "r")
        
        data = adminList.read()
        if data:
            return eval(data)
        else:
            return []


def main():
    rfidManager = RfidManager()
    rfidManager.ScanId()
    
    if rfidManager.userId == 0:
        print("User Id not found.")
        return
    
    if not rfidManager.CheckPermission(rfidManager.userId):
        print("User is currently not an Administrator. Adding " + rfidManager.userId + " to the Administrator list.")
        rfidManager.AddPermission(rfidManager.userId)
        return
    print("User already in Administrator List.")


if __name__ == "__main__":
    main()