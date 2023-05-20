import os


class DatabaseHandler:
    def __init__(self, roomId: str, loudSeats: int, quietSeats: int):
        self.roomId = roomId
        self.roomProperties = {"isActive" : True, "loudSeats" : loudSeats, "quietSeats" : quietSeats, "roomState" : "Empty"}
        
        if not os.path.isfile("localDatabase.txt"):
            open("localDatabase.txt", "x")
        self.database = open("localDatabase.txt", "r+")
        
        # Check if Romm exists in database
        self.database.seek(0)
        self.databaseContent = {}
        
        databaseString = self.database.read()
        if databaseString:
            self.databaseContent = eval(databaseString)

        if self.databaseContent.get(self.roomId, {}).get("isActive"):
            print("### Exception: {roomId} is currently active. Room data is being overwritten to ensure consistency. If you encounter any issues, please verify that there are no other rooms logged in with the same ID.".format(roomId=self.roomId))
        
        
        # Logging into room
        self.databaseContent.setdefault(self.roomId, {}).update(self.roomProperties)
        self.database.seek(0)
        self.database.write(str(self.databaseContent))
        self.database.truncate()
        
        
        # Check if room is now logged in and max seats are changed
        self.database.seek(0)
        self.databaseContent = eval(self.database.read())
        
        if self.roomId in self.databaseContent:
            roomData = self.databaseContent[self.roomId]
            for entry in self.roomProperties:
                if roomData.get(entry) != self.roomProperties[entry]:
                    raise Exception("Room data mismatch for {roomId}. Please ensure that the RaspberryPi is connected to the database and there are no conflicting room properties.".format(roomId=self.roomId))
        else:
            raise Exception("Room with ID {roomId} doesn't exist in the database. Please ensure that the RaspberryPi is connected to the database.".format(roomId=self.roomId))
        
        print("Successfully logged into Database:\n---\nRoom ID: {roomId}\nLoud Seats: {loudSeats}\nQuiet Seats: {quietSeats}\nRoom State: {roomState}\n---".format(roomId=self.roomId, loudSeats=self.databaseContent[self.roomId]["loudSeats"], quietSeats=self.databaseContent[self.roomId]["quietSeats"], roomState=self.databaseContent[self.roomId]["roomState"]))



    def Logout(self):
        self.database.seek(0)
        self.databaseContent = eval(self.database.read())
        
        # changing room status to inactive
        self.databaseContent.setdefault(self.roomId, {}).update({"isActive": False})
        self.database.seek(0)
        self.database.write(str(self.databaseContent))
        self.database.truncate()
        
        # checking if status has changed
        self.database.seek(0)
        self.databaseContent = eval(self.database.read())
        
        if self.roomId in self.databaseContent:
            roomData = self.databaseContent[self.roomId]
            if roomData.get("isActive"):
                print("Failed to log out Room {roomId} from the database.".format(roomId=self.roomId))
            else:
                print("Room {roomId} has successfully logged out of the database.".format(roomId=self.roomId))
            
        self.database.close
        
        
    
    def GetProperty(self, property: str):
        self.database.seek(0)
        self.databaseContent = eval(self.database.read())
        
        if self.roomId in self.databaseContent:
            roomData = self.databaseContent[self.roomId]
            return roomData.get(property)

        print("Could not find room {roomId} in Database.".format(roomId=self.roomId))
        
        
        
    def SetProperty(self, property: str, value):
        self.database.seek(0)
        self.databaseContent = eval(self.database.read())
        
        self.databaseContent.setdefault(self.roomId, {}).update({"property": value})
        self.database.seek(0)
        self.database.write(str(self.databaseContent))
        self.database.truncate()
        
        self.database.seek(0)
        self.databaseContent = eval(self.database.read())
        
        if self.roomId in self.databaseContent:
            roomData = self.databaseContent[self.roomId]
            if roomData.get("property") == value:
                print("Successfully changed {property} to {value} roomstate for room {roomId}.".format(roomId=self.roomId, property=property, value=self.databaseContent[self.roomId][property]))
                return
        
        print("Failed to change property for room {roomId}.".format(roomId=self.roomId))



def main():
    databaseHandler = DatabaseHandler("C127", 7, 10)
    
    databaseHandler.Logout()


if __name__ == "__main__":
    main()