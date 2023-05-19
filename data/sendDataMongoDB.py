# Class:            sendDataMongoDB
# Last updated:     2023/05/18
# Author:           TheScriptGuy (https://github.com/TheScriptGuy)
# Version:          0.11
# Description:      Send json list to mongoDB based on configuration in mongo.cfg

import pymongo
from pymongo import MongoClient
import json
import sys
import os
from datetime import datetime
from bson.objectid import ObjectId


class sendDataMongoDB:
    """sendDataMongoDB class"""

    @staticmethod
    def loadConfigurationFile(__fileName="mongo.cfg"):
        """Loads the json formatted configuration file."""
        try:
            with open(__fileName) as fileNameMongo:
                __mongoConfig = fileNameMongo.read()
            __mongoConfigJson = json.loads(__mongoConfig)
            return __mongoConfigJson
        except FileNotFoundError:
            print(f"Cannot find file {__fileName}.")
            sys.exit(1)
        except json.decoder.JSONDecodeError as e:
            print(f"Error with mongo.cfg config file - {e}")
            sys.exit(1)
        except Exception as e:
            print(f"{e} - Error occured.")
            sys.exit(1)

    @staticmethod
    def sendJsonScriptDataToFile(__fileName, __jsonScriptData):
        """Send script data to __filename."""
        with open(__fileName, "a") as fileJsonScriptData:
            while len(__jsonScriptData) > 0:
                jsonScriptDataItem = __jsonScriptData.pop(0)
                jsonScriptDataItem["queryStatistics"]["scriptStartTime"] = jsonScriptDataItem["queryStatistics"]["scriptStartTime"].strftime('%Y-%m-%dT%H:%M:%S.%f')
                jsonScriptDataItem["queryStatistics"]["scriptEndTime"] = jsonScriptDataItem["queryStatistics"]["scriptEndTime"].strftime('%Y-%m-%dT%H:%M:%S.%f')

                for iResult in jsonScriptDataItem["certResults"]:
                    iResult["startTime"] = iResult["startTime"].strftime('%Y-%m-%dT%H:%M:%S.%f')
                    iResult["endTime"] = iResult["endTime"].strftime('%Y-%m-%dT%H:%M:%S.%f')

                if "_id" in jsonScriptDataItem:
                    jsonScriptDataItem["_id"] = str(jsonScriptDataItem["_id"])

                fileJsonScriptData.write(json.dumps(jsonScriptDataItem) + "\n")

    @staticmethod
    def getJsonScriptDataFromFile(__fileName):
        """Load the contents of __filename into a list."""
        jsonLinesFile = []
        # Check to see if there's a certificateData.json file. If yes, upload its data first.
        try:
            with open("certificateData.json", "r") as fileJsonScriptData:
                while True:
                    fileLine = fileJsonScriptData.readline().replace("\n", "")
                    if not fileLine:
                        break

                    jsonLine = json.loads(fileLine)
                    jsonLine["queryStatistics"]["scriptStartTime"] = datetime.fromisoformat(jsonLine["queryStatistics"]["scriptStartTime"])
                    jsonLine["queryStatistics"]["scriptEndTime"] = datetime.fromisoformat(jsonLine["queryStatistics"]["scriptEndTime"])

                    for iResult in jsonLine["certResults"]:
                        iResult["startTime"] = datetime.fromisoformat(iResult["startTime"])
                        iResult["endTime"] = datetime.fromisoformat(iResult["endTime"])

                    if "_id" in jsonLine:
                        jsonLine["_id"] = ObjectId(jsonLine["_id"])

                    jsonLinesFile.append(jsonLine)

        except FileNotFoundError:
            # File not found error - just ignore.
            pass

        return jsonLinesFile

    def sendResults(self, __results, __destCollection):
        """upload the __results to __destCollection mongodb object."""
        try:
            # First check to see if we need to attempt to upload previous data that was not uploaded.
            previousJsonScriptData = self.getJsonScriptDataFromFile("certificateData.json")
            previousUploadResult = []
            __uploadResult = []

            while len(previousJsonScriptData) > 0:
                jsonScriptDataItem = previousJsonScriptData.pop(0)
                previousUploadResultItem = __destCollection.insert_one(jsonScriptDataItem)
                previousUploadResult.append(previousUploadResultItem)

            if os.path.isfile("certificateData.json"):
                os.remove("certificateData.json")

            if len(previousJsonScriptData) > 0:
                # Didn't finish uploading all the data. Save it to file.
                self.sendJsonScriptDataToFile("certificateData.json", previousJsonScriptData)
                previousJsonScriptData = []

            __mongoResult = __destCollection.insert_one(__results)
            __uploadResult.append(__mongoResult)
        except pymongo.errors.ServerSelectionTimeoutError:
            # Get time of error
            errTime = str(datetime.utcnow())
            print(f"{errTime} - Server connection timeout error when uploading data. Saving to certificateData.json")

            # Save test data to file.
            self.sendJsonScriptDataToFile("certificateData.json", [__results])
            sys.exit(1)

        except pymongo.errors.OperationFailure as e:
            # Get time of error
            errTime = str(datetime.utcnow())
            print(f"{errTime} - Mongo operation error - {e}. Saving to certificateData.json")

            # Save test data to file.
            self.sendJsonScriptDataToFile("certificateData.json", [__results])
            sys.exit(1)

        return previousUploadResult + __uploadResult

    @staticmethod
    def connectionString(__destination):
        """Define the connection string to be used to connect to a MongoDB."""
        # The bare minimum for the URI string is having a hostname/IP address to connect to.
        # If this is blank, make sure we exit.
        if "uri" in __destination:
            __mongoUri = __destination["uri"]
        else:
            print("MongoDB uri not provided in mongo.cfg file.")
            sys.exit(1)

        if "username" in __destination:
            __mongoUsername = __destination["username"]
        else:
            __mongoUsername = ""

        if "password" in __destination:
            __mongoPassword = __destination["password"]
        else:
            __mongoPassword = ""

        # Builds the login credentials to be used.
        if __mongoUsername == "":
            __mongoLoginCredentials = ""
        else:
            if __mongoPassword == "":
                __mongoLoginCredentials = __mongoUsername
            else:
                __mongoLoginCredentials = f"{__mongoUsername}:{__mongoPassword}"

        # Check to see if __mongoUri is an IP address or not.
        if "cluster" in __destination and __destination["cluster"] is True:
            __srv = "+srv"
        else:
            __srv = ""

        # Check to see if TLS is defined for secure connection.
        if "tls" in __destination and __destination["tls"] is True:
            __tls = "&tls=true"
        else:
            __tls = ""

        # Get the collection name. If it's empty, use the default.
        if "collectionName" in __destination and __destination["collectionName"] != "":
            __collectionName = __destination["collectionName"]
        else:
            __collectionName = "certdataGlobal"

        if __mongoLoginCredentials == "":
            __mongoConnectionString = f"mongodb{__srv}://{__mongoUri}/{__tls}"
        else:
            __mongoConnectionString = f"mongodb{__srv}://{__mongoLoginCredentials}@{__mongoUri}/{__collectionName}{__tls}"
        return __mongoConnectionString

    def createDB(self, __destination):
        """create a destination database to upload the data to."""
        # Defaults to certificateDataDB if not defined.
        if "databaseName" in __destination:
            __mongoDatabase = __destination["databaseName"]
        else:
            __mongoDatabase = "certificateDataDB"

        __mongoConnectionString = self.connectionString(__destination)

        try:
            __mongoClient = MongoClient(__mongoConnectionString)
        except pymongo.errors.ConfigurationError as e:
            print(f"mongo.cfg configuration error. {e}")
            sys.exit(1)
        except pymongo.errors.ServerSelectionTimeoutError:
            print("Server connection timeout error.")
            sys.exit(1)

        return __mongoClient[__mongoDatabase]

    def createCollection(self, __mongoConnection, __mongoConfiguration):
        """create a collection within the DB."""
        # First check to see see if collectionName is defined in mongo.cfg
        if "collectionName" in __mongoConfiguration:
            # Retrieve the collectionName value from the dict __mongoConfiguration
            __collectionName = __mongoConfiguration["collectionName"]
        else:
            # Set it to certCollection if there is nothing defined.
            __collectionName = "certCollection"

        return __mongoConnection[__collectionName]

    def uploadDataToMongoDB(self, __jsonScriptData):
        """Upload the data to MongoDB"""
        # Load the configuration file (mongo.cfg)
        mongoConnectJson = self.loadConfigurationFile()

        # Create the connection request.
        connection = self.createDB(mongoConnectJson)

        # Create the collection in the database.
        collection = self.createCollection(connection, mongoConnectJson)

        # Convert the startTime and endTime fields info ISODate format.
        jsonScriptData = __jsonScriptData
        jsonScriptData["queryStatistics"]["scriptStartTime"] = datetime.fromisoformat(jsonScriptData["queryStatistics"]["scriptStartTime"])
        jsonScriptData["queryStatistics"]["scriptEndTime"] = datetime.fromisoformat(jsonScriptData["queryStatistics"]["scriptEndTime"])

        for iResult in jsonScriptData["certResults"]:
            iResult["startTime"] = datetime.fromisoformat(iResult["startTime"])
            iResult["endTime"] = datetime.fromisoformat(iResult["endTime"])

        uploadResult = self.sendResults(__jsonScriptData, collection)

        return uploadResult

    def __init__(self):
        """Initialize the sendDataMongoDB class."""
        self.initialized = True
        self.version = "0.11"
