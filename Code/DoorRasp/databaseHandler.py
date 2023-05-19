class DatabaseHandler:
    def __init__(self, roomId, loudSeats, quietSeats):
        # Login to the Database
        self.roomId = roomId
        self.roomProperties = {"isActive" : True, "loudSeats" : loudSeats, "quietSeats": quietSeats}
        
        database = open("localDatabase.txt", "r+")
        try:
            databaseContent = eval(database.read())
            if databaseContent[self.roomId]['isActive']:
                print("### Exception: {roomId} is currently active. Overwriting room data. If any errors occur, make sure there is no other room logged in with the same ID.".format(roomId=self.roomId))
        except:
            databaseContent = {}
        
        # Logging into room
        databaseContent[self.roomId] = self.roomProperties
        database.seek(0)
        database.write(str(databaseContent))
        database.truncate() 
        
        
        # Check if room is now logged in and max seats are changed
        database.seek(0)
        databaseContent = eval(database.read())
        
        if self.roomId not in databaseContent:
            raise Exception("Unable to log into {roomId}. Make sure the RaspberryPi has a connection to the database.".format(roomId=self.roomId))
        
        print("Successfully logged into Database:\n---\nRoom ID: {roomId}\nLoud Seats: {loudSeats}\nQuiet Seats: {quietSeats}\n---".format(roomId=self.roomId, loudSeats=loudSeats, quietSeats=quietSeats))






def main():
    databaseHandler = DatabaseHandler("C127", 7, 10)


if __name__ == "__main__":
    main()