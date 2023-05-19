import os
import numpy as np


class DatabaseHandler():
    def __init__(self, roomId, loudMaxSeats, quietMaxSeats):
        # Login to the Database
        self.roomId = roomId
        self.loudMaxSeats = loudMaxSeats
        self.quietMaxSeats = quietMaxSeats
        
        # Check if room is currently logged in
        if(False):
            print("### Exception: {roomId} is currently active. Overwriting room data. If any errors occour make sure there is no other room logged in with the same ID.".format(roomId=self.roomId))
            
        # log into room
        
        
        # Check if room is now logged in and max seats are changed
        if(False):
            raise Exception("Unable to log into {roomId}. Make sure the RaspberryPi has a connection to the database.".format(roomId=self.roomId))
        
        return print("Sucessfully logged into Database: \n --- \n Room ID: {roomId} \n Maximum seats loud: {loudMaxSeats} \n Maximum seats quiet: {quietMaxSeats} \n --- ".format(roomId=self.roomId, loudMaxSeats=self.loudMaxSeats, quietMaxSeats=self.quietMaxSeats))
    
    






def main():
    databaseHandler = DatabaseHandler("C127", 7, 10)


if __name__ == "__main__":
    main()