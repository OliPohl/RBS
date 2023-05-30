import os


class DatabaseHandler:
    def __init__(self, roomId: str, loudSeats: int, quietSeats: int):
        self.roomId = roomId
        self.roomProperties = {
            "isActive": True,
            "loudSeats": loudSeats,
            "quietSeats": quietSeats,
            "roomState": "Empty",
            "Entry": []
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
        
        
    def AddEntry(self, userId: str, entryTime: str, exitTime: str):
        entry = {
            "UserId": userId,
            "EntryTime": entryTime,
            "ExitTime": exitTime
        }
        self.databaseContent[self.roomId]["Entry"].append(entry)
        self.UpdateDatabase("Entry", self.databaseContent[self.roomId]["Entry"])
        print("Added entry for User {userId} with Entry Time: {entryTime} and Exit Time: {exitTime}.".format(userId=userId, entryTime=entryTime, exitTime=exitTime))
        
        
    def DeleteEntry(self, userId: str):
        entries = self.databaseContent[self.roomId]["Entry"]
        removed_entries = [entry for entry in entries if entry["UserId"] == userId]
        entries[:] = [entry for entry in entries if entry["UserId"] != userId]
        self.UpdateDatabase("Entry", entries)
        
        if removed_entries:
            print("Deleted all entries for User {userId}.".format(userId=userId))
            return
        
        print("No entries found for User {userId}.".format(userId=userId))


    def ScanUserId(self, userId: str):
        entries = self.databaseContent[self.roomId]["Entry"]
        user_entries = [entry for entry in entries if entry["UserId"] == userId]
        if len(user_entries) > 0:
            return True
        return False
    
    
    def GetEntryExitTimes(self):
        entries = self.databaseContent[self.roomId]["Entry"]
        entry_exit_times = [(entry["EntryTime"], entry["ExitTime"]) for entry in entries]
        return entry_exit_times
    
    
    def DeleteAllEntries(self):
        self.databaseContent[self.roomId]["Entry"] = []
        self.UpdateDatabase("Entry", [])
        print("Deleted all entries for Room {roomId}.".format(roomId=self.roomId))


        
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
        return self.databaseContent.get(property)
        
        
    def SetProperty(self, property: str, value):
        self.databaseContent = self.UpdateDatabase(property, value)
        
        if self.databaseContent.get(self.roomId, {}).get(property) == value:
            print("Successfully changed {property} to {value} roomstate for room {roomId}.".format(roomId=self.roomId, property=property, value=self.databaseContent[self.roomId][property]))
            return
        
        print("Failed to change property for room {roomId}.".format(roomId=self.roomId))



def main():
    databaseHandler = DatabaseHandler("C127", 7, 10)
    
    databaseHandler.AddEntry("John123", "2023-05-30 10:00:00", "2023-05-30 12:00:00")
    
    databaseHandler.Logout()


if __name__ == "__main__":
    main()