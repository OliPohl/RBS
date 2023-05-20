import os


class DatabaseHandler:
    def __init__(self, roomId: str, loudSeats: int, quietSeats: int):
        self.roomId = roomId
        self.roomProperties = {"isActive" : True, "loudSeats" : loudSeats, "quietSeats" : quietSeats, "roomState" : "Empty"}
        
        if not os.path.isfile("localDatabase.txt"):
            open("localDatabase.txt", "x")
        self.database = open("localDatabase.txt", "r+")
        
        # Check if Romm exists in database      
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
        self.databaseContent = self.GetDatabaseContent()
        self.databaseContent = self.UpdateDatabase("isActive", False)
        
        if not self.databaseContent.get(self.roomId, {}).get("isActive"):
            self.database.close
            print("Room {roomId} has successfully logged out of the database.".format(roomId=self.roomId))
            return

        print("Failed to log out Room {roomId} from the database.".format(roomId=self.roomId))
        
        
        
    def GetDatabaseContent(self):
        self.database.seek(0)
        databaseString = self.database.read()
        if databaseString:
            return eval(databaseString)
        else:
            return {}
        
        
    
    def UpdateDatabase(self, property: str, value):
        self.databaseContent.setdefault(self.roomId, {}).update({property: value})
        self.database.seek(0)
        self.database.write(str(self.databaseContent))
        self.database.truncate()
        return self.GetDatabaseContent()

        
        
    def GetProperty(self, property: str):
        self.databaseContent = self.GetDatabaseContent()
        return self.databaseContent.get(property)
        
        
        
    def SetProperty(self, property: str, value):
        self.databaseContent = self.GetDatabaseContent()
        self.databaseContent = self.UpdateDatabase(property, value)
        
        if self.databaseContent.get(self.roomId, {}).get(property) == value:
            print("Successfully changed {property} to {value} roomstate for room {roomId}.".format(roomId=self.roomId, property=property, value=self.databaseContent[self.roomId][property]))
            return
        
        print("Failed to change property for room {roomId}.".format(roomId=self.roomId))



def main():
    databaseHandler = DatabaseHandler("C127", 7, 10)
    
    databaseHandler.Logout()


if __name__ == "__main__":
    main()