# Class:            mongo_data
# Last updated:     2023/08/13
# Author:           TheScriptGuy (https://github.com/TheScriptGuy)
# Version:          0.01
# Description:      Reads/writes to certifciateData.json.
#                   If file certificateData.json exists, add it to the queue to upload.
#                   If upload unsuccessful, write the queue to file.
import json
from datetime import datetime
from bson.objectid import ObjectId


class mongo_data:
    """mongo_data class"""

    @staticmethod
    def sendJsonScriptDataToFile(__fileName, __jsonScriptData):
        """Send script data to __filename."""
        jsonScriptData = __jsonScriptData

        with open(__fileName, "a") as fileJsonScriptData:
            while jsonScriptData:
                jsonScriptDataItem = jsonScriptData.pop(0)
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

    def __init__(self):
        """Initialize the mongo_data class."""
        self.initialized = True
        self.version = "0.01"
