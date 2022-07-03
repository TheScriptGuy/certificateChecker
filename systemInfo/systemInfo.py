# systemInfo class
import socket
from os import path
import json
import sys
import uuid


class systemInfo:
    """systemInfo class"""

    def generateUuid(self):
        """Generate a uuid."""
        return str(uuid.uuid4())

    def getHostname(self):
        """Get the hostname of the device performing the checks."""
        return socket.gethostname()

    def updateMyConfig(self):
        """Outputs the configuration file into the self.myConfigFile location."""
        __myConfigJson = self.myConfigJson

        with open(self.myConfigFile, 'w') as f_myConfig:
            f_myConfig.write(json.dumps(__myConfigJson, indent=4))

    def getDeviceId(self):
        """Get the uuid."""
        __myDeviceId = ""
        if "myDeviceId" in self.myConfigJson:
            __myDeviceId = self.myConfigJson["myDeviceId"]
        return __myDeviceId

    def getTag(self):
        """Get the tag(s)."""
        __myTags = []

        # First check to see if the myTags element is in the myConfigJson variable.
        if "myTags" in self.myConfigJson:
            __myTags = self.myConfigJson["myTags"]

        # Return the value of __myTags
        return __myTags

    def setTag(self, __tagName):
        """Set the tag for data aggregation purposes."""
        # Separate out all the tags using commas
        __newTagName = __tagName.rstrip().split(',')

        # Remove any potential duplicate tags.
        __newTagName = list(dict.fromkeys(__newTagName))

        # Update the class's myConfigJson variable.
        self.myConfigJson["myTags"] = __newTagName

        # Update the configuration file.
        self.updateMyConfig()

    def deleteTag(self):
        """Delete the tag."""
        self.myConfigJson["myTags"] = []
        self.updateMyConfig()

    def deleteDeviceId(self):
        """Delete the device uuid from configuration file."""
        self.myConfigJson["myDeviceId"] = ""
        self.updateMyConfig()

    def getTenantId(self):
        """Returns the tenant Id."""
        return self.myConfigJson["myTenantId"]

    def setTenantId(self, __myTenantId):
        """Sets the tenant Id for the script."""
        self.myConfigJson["myTenantId"] = __myTenantId
        self.updateMyConfig()

    def deleteTenantId(self):
        """Deletes the tenant Id and updates configuration file."""
        self.setTenantId("")

    @staticmethod
    def checkMyTenantId(__myConfigJson):
        """
        Checks if the Tenant ID is defined.
        Returns True if it is.
        Returns False if it is not
        """
        result = False
        if "myTenantId" in __myConfigJson:
            if __myConfigJson["myTenantId"] != "":
                return True
        return result

    @staticmethod
    def checkMyTags(__myConfigJson):
        """
        Checks if tags are defined. This is an optional field.
        Returns True if it is.
        Returns False if it is not.
        """
        result = bool("myTags" in __myConfigJson)
        return result

    @staticmethod
    def checkMyDeviceId(__myConfigJson):
        """
        Checks if the device ID is defined.
        Returns True if it is.
        Returns False if is not.
        """
        result = False
        if "myDeviceId" in __myConfigJson:
            if __myConfigJson["myDeviceId"] != "":
                result = True
        return result

    def checkIfTenantIdExists(self, __myConfigJson):
        """Check to see if the Tenant Id is defined."""
        if not self.checkMyTenantId(__myConfigJson):
            print("myTenantId is not defined. Please use --setTenantId argument.")
            sys.exit(1)

    def generateDeviceId(self):
        """Generate a device id."""
        self.myConfigJson["myDeviceId"] = self.generateUuid()
        self.updateMyConfig()

    def checkIfDeviceIdExists(self, __myConfigJson):
        """Check to see if the device Id is defined. If not, generate a new one."""
        if not self.checkMyDeviceId(__myConfigJson):
            self.generateDeviceId()

    def createBlankConfigurationFile(self):
        """
        Creates a blank configuration file with an updated myDeviceId field.
        This will overwrite any existing configuration.
        """
        __blankConfigurationJson = {
            "myTenantId": "",
            "myTags": "",
            "myDeviceId": self.generateUuid()
        }

        with open(self.myConfigFile, 'w') as f_myConfig:
            f_myConfig.write(json.dumps(__blankConfigurationJson, indent=4))

    def parseConfigFile(self):
        """Returns the json object from the configuration file."""
        try:
            if not path.exists(self.myConfigFile):
                self.createBlankConfigurationFile()

            with open(self.myConfigFile, 'r') as f_myConfig:
                __myConfigJson = json.load(f_myConfig)

            return __myConfigJson

        except json.decoder.JSONDecodeError as e:
            print(f"Syntax error in {self.myConfigFile} file at line {e.lineno} and column {e.colno}.")
            sys.exit(1)

    def refreshConfigFile(self):
        """Gets the configuration file and loads it into memory."""
        self.myConfigJson = self.parseConfigFile()

    def __init__(self, __myConfigFile="myConfig.json"):
        """Initialize the class."""
        # Define the class version.
        self.classVersion = "0.04"

        self.myConfigJson = {}

        # Get the hostname of the device where this is being run on.
        self.hostname = self.getHostname()

        # Assign the __myConfigFile value to the class's variable myConfigFile.
        self.myConfigFile = __myConfigFile

        # Load the configuration file.
        self.refreshConfigFile()

        # Check to see if the device Id exists, if not, generate one.
        self.checkIfDeviceIdExists(self.myConfigJson)
