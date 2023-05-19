class DatabaseHandler:
    def __init__(self, roomId, loudMaxSeats, quietMaxSeats):
        # Login to the Database
        self.roomId = roomId
        self.roomProperties = {"isActive" : True, "loudMaxSeats" : loudMaxSeats, "quietMaxSeats": quietMaxSeats}
        
        database = open("localDatabase.txt", "r+")
        databaseContent = database.read()
        
        # Check if room is currently logged in
        if self.roomId in databaseContent:
            print("### Exception: {roomId} is currently active. Overwriting room data. If any errors occur, make sure there is no other room logged in with the same ID.".format(roomId=self.roomId))


        # Log into the room by writing roomId
        database.write(f"{self.roomId} = {self.roomProperties}\n")
        
        # read database to check if successfull
        databaseContent = database.read()
        
        # Check if room is now logged in and max seats are changed
        if self.roomId in databaseContent:
            raise Exception("Unable to log into {roomId}. Make sure the RaspberryPi has a connection to the database.".format(roomId=self.roomId))
        
        print("Successfully logged into Database:\n---\nRoom ID: {roomId}\nMaximum seats loud: {loudMaxSeats}\nMaximum seats quiet: {quietMaxSeats}\n---".format(roomId=self.roomId, loudMaxSeats=self.loudMaxSeats, quietMaxSeats=self.quietMaxSeats))






def main():
    databaseHandler = DatabaseHandler("C127", 7, 10)


if __name__ == "__main__":
    main()