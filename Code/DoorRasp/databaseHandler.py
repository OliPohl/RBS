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

#         if not os.path.isfile("localDatabase.txt"):
#             open("localDatabase.txt", "x")
#         self.database = open("localDatabase.txt", "r+")
        
#         # Check if Room exists in the database      
#         self.databaseContent = self.GetDatabaseContent()

#         if self.databaseContent.get(self.roomId, {}).get("isActive"):
#             print("### Exception: {roomId} is currently active. Room data is being overwritten to ensure consistency. If you encounter any issues, please verify that there are no other rooms logged in with the same ID.".format(roomId=self.roomId))
        
#         # Logging into room
#         for entry in self.roomProperties:
#             self.databaseContent = self.UpdateDatabase(entry, self.roomProperties[entry])
        
#         # Check for Information mismatch
#         for entry in self.roomProperties:
#             if self.databaseContent.get(self.roomId, {}).get(entry) != self.roomProperties[entry]:
#                 raise Exception("Room data mismatch for {roomId}. Please ensure that the RaspberryPi is connected to the database and there are no conflicting room properties.".format(roomId=self.roomId))
                
#         print("Successfully logged into Database:\n---\nRoom ID: {roomId}\nLoud Seats: {loudSeats}\nQuiet Seats: {quietSeats}\nRoom State: {roomState}\n---".format(roomId=self.roomId, loudSeats=self.databaseContent[self.roomId]["loudSeats"], quietSeats=self.databaseContent[self.roomId]["quietSeats"], roomState=self.databaseContent[self.roomId]["roomState"]))



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
    
#     def GetExitTimes(self):
#         entries = self.GetProperty("entry")
        
#         if entries == []:
#            return []
       
#         exitTimes = []
#         for entry in entries:
#             exitTimes.append(entry["exitTime"])
#         return exitTimes
    
    #soll alle Objekte mit entry:userId,entryTime,exitTime zurückgeben und zählen
    def GetEntryCount(self):
        cur = self.mycol.find(self.roomId_query, {"entry": {"$all": [["userId", "entryTime", "exitTime"]]}})
        count = 0
        result = list(cur)
        for x in result:
            count += 1
        return count     
    
    
#     def DeleteAllEntries(self):
#         self.UpdateDatabase("entry", [])
#         print("Deleted all entries for Room {roomId}.".format(roomId=self.roomId))
        
        
    def DeleteExpiredEntries(self):
        cur = self.mycol.find(self.roomId_query, {"entry": {"$all": [["userId", "entryTime", "exitTime"]]}})
        results = list(cur)
        for x in results:
            exitTime = results[x][2]
            if datetime.now() >= exitTime:
                self.DeleteEntry(results[x][0])
#         for entry in entries:
#             timeDelta = datetime.combine(datetime.today(), datetime.strptime(entry["exitTime"], '%H:%M').time()) - datetime.combine(datetime.today(), datetime.now().time())
#             minuteDelta = timeDelta.seconds // 60
#             if minuteDelta <= 0 or minuteDelta > 100:
#                 self.DeleteEntry(entry["userId"])
                

        
#     def GetDatabaseContent(self):
#         self.database.seek(0)
#         databaseString = self.database.read()
#         if databaseString:
#             return eval(databaseString)
#         else:
#             return {}
        
        
#     def UpdateDatabase(self, property: str, value):
#         self.databaseContent = self.GetDatabaseContent()
#         self.databaseContent.setdefault(self.roomId, {}).update({property: value})
#         self.database.seek(0)
#         self.database.write(str(self.databaseContent))
#         self.database.truncate()
#         return self.GetDatabaseContent()

        
    def GetProperty(self, property: str):
        #self.databaseContent = self.GetDatabaseContent()
        property += ": 1, _id: 0"
        return self.mycol.find_one(self.roomId_query, {property})
    
    
    def GetRoomId(self):
        return self.roomId
        
        
    def SetProperty(self, property: str, value):
        newValues = { "$set": {property: value}}
        self.mycol.update_one(self.roomId_query, newValues)
#         self.databaseContent = self.UpdateDatabase(property, value)
#         if self.databaseContent.get(self.roomId, {}).get(property) == value:
#             print("Successfully changed {property} to {value} roomstate for room {roomId}.".format(roomId=self.roomId, property=property, value=self.databaseContent[self.roomId][property]))
#             return
#         else:
#             print("Failed to change property for room {roomId}.".format(roomId=self.roomId))



def main():
    databaseHandler = DatabaseHandler("C125", 7, 10)
    
    databaseHandler.AddEntry("John1232", datetime.now(), datetime.now() + timedelta(hours=1))
    databaseHandler.DeleteEntry("John1232")
    databaseHandler.Logout()


if __name__ == "__main__":
    main()