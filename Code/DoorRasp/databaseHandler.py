import os
from datetime import datetime


class DatabaseHandler:
    def __init__(self, roomId: str, loudSeats: int, quietSeats: int):
        self.roomId = roomId
        self.roomProperties = {
            "isActive": True,
            "loudSeats": loudSeats,
            "quietSeats": quietSeats,
            "roomState": "Empty",
            "entry": []
        }
        
        if not os.path.isfile("localDatabase.txt"):
            open("localDatabase.txt", "x")
        self.database = open("localDatabase.txt", "r+")
        
        # Check if Room exists in the database      
        self.databaseContent = self.GetDatabaseContent()

        if self.databaseContent.get(self.roomId, {}).get("isActive"):
            print("### Exception: {roomId} is currently active. Room data is being overwritten to ensure consistency. If you encounter any issues, please verify that there are no other rooms logged in with the same ID.".format(roomId=self.roomId))
        
        # Logging into room
        for entry in self.roomProperties:
            self.databaseContent = self.UpdateDatabase(entry, self.roomProperties[entry])
        
        # Check for Information mismatch
        for entry in self.roomProperties:
            if self.databaseContent.get(self.roomId, {}).get(entry) != self.roomProperties[entry]:
                raise Exception("Room data mismatch for {roomId}. Please ensure that the RaspberryPi is connected to the database and there are no conflicting room properties.".format(roomId=self.roomId))
                
        print("Successfully logged into Database:\n---\nRoom ID: {roomId}\nLoud Seats: {loudSeats}\nQuiet Seats: {quietSeats}\nRoom State: {roomState}\n---".format(roomId=self.roomId, loudSeats=self.databaseContent[self.roomId]["loudSeats"], quietSeats=self.databaseContent[self.roomId]["quietSeats"], roomState=self.databaseContent[self.roomId]["roomState"]))



    def Logout(self):
        self.databaseContent = self.UpdateDatabase("isActive", False)
        
        if not self.databaseContent.get(self.roomId, {}).get("isActive"):
            self.DeleteAllEntries()
            self.database.close
            print("Room {roomId} has successfully logged out of the database.".format(roomId=self.roomId))
            return

        print("Failed to log out Room {roomId} from the database.".format(roomId=self.roomId))
        
        
    def AddEntry(self, userId: str, startTime: str, exitTime: str):
        entries = self.GetProperty("entry")
        
        entry = {
            "userId": userId,
            "entryTime": startTime,
            "exitTime": exitTime
        }
        
        entries.append(entry)
        self.UpdateDatabase("entry", entries)
        print("Added Entry for User {userId} with Entry Time: {startTime} and Exit Time: {exitTime}.".format(userId=userId, startTime=startTime, exitTime=exitTime))
        
        
    def DeleteEntry(self, userId: str):
        entries = self.GetProperty("entry")
        
        if entries == []:
            return
        
        updatedEntries = []
        for entry in entries:
            if entry["userId"] != userId:
                updatedEntries.append(entry)
        
        self.UpdateDatabase("entry", updatedEntries)


    def ScanUserId(self, userId: str):
        entries = self.GetProperty("entry")
        
        if entries == []:
           return False
        
        for entry in entries:
            if entry["UserId"] == userId:
                return True
        return False

    
    
    def GetExitTimes(self):
        entries = self.GetProperty("entry")
        
        if entries == []:
           return []
       
        exitTimes = []
        for entry in entries:
            exitTimes.append(entry["exitTime"])
        return exitTimes
    
    
    def GetEntryCount(self):
        entries = self.GetProperty("entry")
        return len(entries)
    
    
    def DeleteAllEntries(self):
        self.UpdateDatabase("entry", [])
        print("Deleted all entries for Room {roomId}.".format(roomId=self.roomId))
        
        
    def DeleteExpiredEntries(self):
        entries = self.GetProperty("entry")
        
        print("Entries in DeleteExpiredEntries(): " + str(entries))
        if entries == []:
            return
        
        for entry in entries:
            timeDelta = datetime.combine(datetime.today(), datetime.strptime(entry["exitTime"], '%H:%M').time()) - datetime.combine(datetime.today(), datetime.now().time())
            minuteDelta = timeDelta.seconds // 60
            if minuteDelta <= 0 or minuteDelta > 100:
                self.DeleteEntry(entry["userId"])
                

        
    def GetDatabaseContent(self):
        self.database.seek(0)
        databaseString = self.database.read()
        if databaseString:
            return eval(databaseString)
        else:
            return {}
        
        
    def UpdateDatabase(self, property: str, value):
        self.databaseContent = self.GetDatabaseContent()
        self.databaseContent.setdefault(self.roomId, {}).update({property: value})
        self.database.seek(0)
        self.database.write(str(self.databaseContent))
        self.database.truncate()
        return self.GetDatabaseContent()

        
    def GetProperty(self, property: str):
        self.databaseContent = self.GetDatabaseContent()
        return self.databaseContent.get(self.roomId, {}).get(property)
    
    
    def GetRoomId(self):
        return self.roomId
        
        
    def SetProperty(self, property: str, value):
        self.databaseContent = self.UpdateDatabase(property, value)
        
        if self.databaseContent.get(self.roomId, {}).get(property) == value:
            print("Successfully changed {property} to {value} roomstate for room {roomId}.".format(roomId=self.roomId, property=property, value=self.databaseContent[self.roomId][property]))
            return
        
        print("Failed to change property for room {roomId}.".format(roomId=self.roomId))



def main():
    databaseHandler = DatabaseHandler("C125", 7, 10)
    
    databaseHandler.AddEntry("John1232", "15:00", "15:24")
    
    databaseHandler.Logout()


if __name__ == "__main__":
    main()