# send data to <mongodb location>
# In development: mongodb
# Version 0.01

import pymongo
from pymongo import MongoClient
import iptools
import json
import sys

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
        except Exception as e:
            print(f"{e.message} - Error occured.")
            sys.exit(1)

    @staticmethod
    def sendResults(__results, __destCollection):
        """upload the __results to __destCollection mongodb object."""
        try:
            __uploadResult = __destCollection.insert_one(__results)
        except pymongo.errors.ServerSelectionTimeoutError as e:
            print("Server connection timeout error when uploadint data.")
            sys.exit(1)

        return __uploadResult

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
        if iptools.ipv4.validate_ip(__mongoUri):
            __srv = ""
        else:
            __srv = "+srv"

        if __mongoLoginCredentials == "":
            __mongoConnectionString = f"mongodb{__srv}://{__mongoUri}/"
        else:
            __mongoConnectionString = f"mongodb{__srv}://{__mongoLoginCredentials}@{__mongoUri}/"
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
            print("mongo.cfg configuration error.")
            sys.exit(1)
        except pymongo.errors.ServerSelectionTimeoutError as e:
            print("Server connection timeout error.")
            sys.exit(1)

        return __mongoClient[__mongoDatabase]

    def createCollection(self, __mongoConnection, __collectionName="certCollection"):
        """create a collection within the DB."""
        return __mongoConnection[__collectionName]

    def __init__(self):
        """Initialize the sendDataMongoDB class."""
        self.initialized = True
        self.version = "0.01"
