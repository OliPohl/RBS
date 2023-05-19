class DatabaseHandler:
    def __init__(self, roomId: str, loudSeats: int, quietSeats: int):
        self.roomId = roomId
        self.roomProperties = {"isActive" : True, "loudSeats" : loudSeats, "quietSeats": quietSeats}
        
        self.database = open("localDatabase.txt", "r+")
        
        # Check if Romm exists in database
        try:
            self.databaseContent = eval(self.database.read())
            if self.databaseContent.get(self.roomId, {}).get('isActive'):
                print("### Exception: {roomId} is currently active. Room data is being overwritten to ensure consistency. If you encounter any issues, please verify that there are no other rooms logged in with the same ID.".format(roomId=self.roomId))
        except:
            self.databaseContent = {}
        
        
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
        
        print("Successfully logged into Database:\n---\nRoom ID: {roomId}\nLoud Seats: {loudSeats}\nQuiet Seats: {quietSeats}\n---".format(roomId=self.roomId, loudSeats=self.databaseContent[self.roomId]["loudSeats"], quietSeats=self.databaseContent[self.roomId]["quietSeats"]))






def main():
    databaseHandler = DatabaseHandler("C127", 7, 10)


if __name__ == "__main__":
    main()