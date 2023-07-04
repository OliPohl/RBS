import os
import pymongo
from datetime import datetime, timedelta, timezone
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class DatabaseHandler:
    def __init__(self, roomId: str, loudSeats: str, quietSeats: str, xPos: str, yPos: str):
        self.roomId = roomId
        uri = "mongodb+srv://raumgestalter01:Projektmanagment2023@raumuebersicht.9ewq6ka.mongodb.net/?retryWrites=true&w=majority"
        # Create a new client and connect to the server
        client = MongoClient(uri, server_api=ServerApi('1'))
        # Send a ping to confirm a successful connection
        try:
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        self.dblist = client.list_database_names()
        if "Raumuebersicht" in self.dblist:
            print("The database exists.")
        self.mydb = client["Raumuebersicht"]
        self.mycol = self.mydb["raeume"]
        self.roomProperties = {
                "_id" : self.roomId,
                "isActive": "True",
                "loudSeats": loudSeats,
                "quietSeats": quietSeats,
                "x": xPos,
                "y": yPos,
                "roomState": "Empty",
                "entry": []
            }
        collist = self.mydb.list_collection_names()
        if "raeume" in collist:
            print("The collection exists.")
        self.roomId_query = { "_id": self.roomId }
        newvalues = { "$set": self.roomProperties }
        self.mycol.update_one(self.roomId_query, newvalues, upsert=True)



    def Logout(self):
        properties = {
                "_id" : self.roomId,
                "isActive": "False",
                "loudSeats": "0",
                "quietSeats": "0",
                "roomState": "Empty",
                "entry": []
            }
        newvalues = { "$set": properties }
        self.mycol.update_one(self.roomId_query, newvalues, upsert=True)
        print("Failed to log out Room {roomId} from the database.".format(roomId=self.roomId))
        
        
    def AddEntry(self, userId: str, startTime: datetime, exitTime: datetime):
        entry = {
            "userId": userId,
            "entryTime": startTime,
            "exitTime": exitTime
        }
        newValues = { "$push": { "entry" : entry}}
        self.mycol.update_one(self.roomId_query, newValues)
        print("Added Entry for User {userId} with Entry Time: {startTime} and Exit Time: {exitTime}.".format(userId=userId, startTime=startTime, exitTime=exitTime))
        
        
    def DeleteEntry(self, userId: str):
        self.mycol.update_one(self.roomId_query, {"$pull": {"entry": {"userId": userId}}})
        #self.mycol.update_one(self.roomId, {"$unset": })
 

    def ScanUserId(self, userId: str):
        cur = self.mycol.find(self.roomId_query, {"entry": 1, "_id": 0})

        results = list(cur)[0]["entry"]
        if results == []:
            return False
        
        for entry in results:
            if userId == entry["userId"]:
                return True
        return False
    
    
    def GetExitTimes(self):
        cur = self.mycol.find(self.roomId_query, {"entry": 1, "_id": 0})

        results = list(cur)[0]["entry"]
        if results == []:
            return []
        
        exitTimes = []
        for entry in results:
            exitTimes.append(entry["exitTime"])
            
        return exitTimes
    
    
    #soll alle Objekte mit entry:userId,entryTime,exitTime zurückgeben und zählen
    def GetEntryCount(self):
        cur = self.mycol.find(self.roomId_query, {"entry": 1, "_id": 0})

        results = list(cur)[0]["entry"]
        if results == []:
            return 0
        
        count = 0
        for entry in results:
            count += 1
        
        return count
    
    
    def DeleteAllEntries(self):
        cur = self.mycol.find(self.roomId_query, {"entry": 1, "_id": 0})

        results = list(cur)[0]["entry"]
        if results == []:
            return
        
        for entry in results:
            self.DeleteEntry(entry["userId"])
        
        
    def DeleteExpiredEntries(self):
        cur = self.mycol.find(self.roomId_query, {"entry": 1, "_id": 0})

        results = list(cur)[0]["entry"]
        if results == []:
            return
        
        for entry in results:
            if datetime.now(timezone(timedelta(hours=2))) >= entry["exitTime"]:
                self.DeleteEntry(entry["userId"])


        
    def GetProperty(self, property: str):
        # property += ": 1, _id: 0"

        dict = self.mycol.find_one(self.roomId_query, {property: 1,"_id": 0})
        return dict[property]
    
    
    def GetRoomId(self):
        return self.roomId
        
        
    def SetProperty(self, property: str, value):
        newValues = { "$set": {property: value}}
        self.mycol.update_one(self.roomId_query, newValues)



def main():
    databaseHandler = DatabaseHandler("C125", 7, 10)
    
    databaseHandler.AddEntry("John1232", datetime.now(timezone(timedelta(hours=2))), datetime.now(timezone(timedelta(hours=2))) + timedelta(minutes=15))
    databaseHandler.AddEntry("Tom1232", datetime.now(timezone(timedelta(hours=2))), datetime.now(timezone(timedelta(hours=2))) + timedelta(minutes=30))
    databaseHandler.AddEntry("jimmy", datetime.now(timezone(timedelta(hours=2))), datetime.now(timezone(timedelta(hours=2))) + timedelta(minutes=450))
    databaseHandler.DeleteExpiredEntries()
        
    databaseHandler.Logout()


if __name__ == "__main__":
    main()