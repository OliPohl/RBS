import os
import pymongo
from datetime import datetime, timedelta
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

class DatabaseHandler:
    def __init__(self, roomId: str, loudSeats: str, quietSeats: str):
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
        cur = self.mycol.find_one(self.roomId_query, {"entry": {"userId": userId}})
        results = list(cur)
        if len(results)==0:
            return False
        else:    
            return True
    
    
    def GetExitTimes(self):
        allEntries = self.mycol.find(self.roomId_query, {"entry": {"$all": [["userId", "entryTime", "exitTime"]]}})
        
        exitTimes = []
        for entry in allEntries:
            exitTime = entry[0][2].strftime("%H:%M")
            exitTimes.append(exitTime)
        
        return exitTimes
    
    
    #soll alle Objekte mit entry:userId,entryTime,exitTime zurückgeben und zählen
    def GetEntryCount(self):
        cur = self.mycol.find(self.roomId_query, {"entry": {"$all": [["userId", "entryTime", "exitTime"]]}})
        count = 0
        result = list(cur)
        for x in result:
            count += 1
        return count     
    
    
    def DeleteAllEntries(self):
        allEntries = self.mycol.find(self.roomId_query, {"entry": {"$all": [["userId", "entryTime", "exitTime"]]}})
        
        for entry in allEntries:
            self.DeleteEntry(entry[0])
        
        
    def DeleteExpiredEntries(self):
        cur = self.mycol.find(self.roomId_query, {"entry": 1, "_id": 0})
        results = dict(cur)
        for x in results.values():
            for y in x:
                exitTime = y["exitTime"]
                if datetime.now() >= exitTime:
                    self.DeleteEntry(y["userId"])

        
    def GetProperty(self, property: str):
        property += ": 1, _id: 0"
        return self.mycol.find_one(self.roomId_query, {property})
    
    
    def GetRoomId(self):
        return self.roomId
        
        
    def SetProperty(self, property: str, value):
        newValues = { "$set": {property: value}}
        self.mycol.update_one(self.roomId_query, newValues)



def main():
    databaseHandler = DatabaseHandler("C125", 7, 10)
    
    databaseHandler.AddEntry("John1232", datetime.now(), datetime.now() + timedelta(hours=1))
    databaseHandler.DeleteEntry("John1232")
    databaseHandler.Logout()


if __name__ == "__main__":
    main()