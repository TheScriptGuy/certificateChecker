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
    def sendJsonScriptDataToFile(
            __fileName: str,
            __jsonScriptData: list
            ) -> None:
        """Send script data to __filename."""
        jsonScriptData = __jsonScriptData

        # Open the __fileName for append modde.
        with open(__fileName, "a") as fileJsonScriptData:
            # Iterate through the list.
            while jsonScriptData:
                # Get the first entry from the jsonScriptData list.
                jsonScriptDataItem = jsonScriptData.pop(0)

                # Convert the scriptStartTime to string type.
                jsonScriptDataItem["queryStatistics"]["scriptStartTime"] = jsonScriptDataItem["queryStatistics"]["scriptStartTime"].strftime('%Y-%m-%dT%H:%M:%S.%f')

                # Convert the scriptEndTime to string type.
                jsonScriptDataItem["queryStatistics"]["scriptEndTime"] = jsonScriptDataItem["queryStatistics"]["scriptEndTime"].strftime('%Y-%m-%dT%H:%M:%S.%f')

                # Iterate through the certResults and convert to string type
                # for startTime and endTime
                for iResult in jsonScriptDataItem["certResults"]:
                    iResult["startTime"] = iResult["startTime"].strftime('%Y-%m-%dT%H:%M:%S.%f')
                    iResult["endTime"] = iResult["endTime"].strftime('%Y-%m-%dT%H:%M:%S.%f')

                # If the _id field exists, convert it to string type from ObjectId.
                if "_id" in jsonScriptDataItem:
                    jsonScriptDataItem["_id"] = str(jsonScriptDataItem["_id"])

                # Write the data back to the file.
                fileJsonScriptData.write(json.dumps(jsonScriptDataItem) + "\n")

    @staticmethod
    def getJsonScriptDataFromFile(
            __fileName: str
            ) -> None:
        """Load the contents of __filename into a list."""
        jsonLinesFile = []
        # Check to see if there's a certificateData.json file. If yes, upload its data first.
        try:
            # Open the certificateData.json file for read-only mode.
            with open(__fileName, "r") as fileJsonScriptData:
                while True:
                    """
                    Keep reading lines until we reach the end of the file.
                    Strip the \n character from the end of the line.
                    """
                    fileLine = fileJsonScriptData.readline().replace("\n", "")
                    if not fileLine:
                        # We reached the end of the file, exit out of the loop
                        break

                    # Convert the line into json format.
                    jsonLine = json.loads(fileLine)

                    # Convert the scriptStartTime to datetime format.
                    jsonLine["queryStatistics"]["scriptStartTime"] = datetime.fromisoformat(jsonLine["queryStatistics"]["scriptStartTime"])

                    # Convert the scriptEndTime to datetime format.
                    jsonLine["queryStatistics"]["scriptEndTime"] = datetime.fromisoformat(jsonLine["queryStatistics"]["scriptEndTime"])

                    # Iterate through all the certResults and convert them to datetime format.
                    for iResult in jsonLine["certResults"]:
                        iResult["startTime"] = datetime.fromisoformat(iResult["startTime"])
                        iResult["endTime"] = datetime.fromisoformat(iResult["endTime"])

                    # If the _id field exists, convert it to the ObjectId type.
                    if "_id" in jsonLine:
                        jsonLine["_id"] = ObjectId(jsonLine["_id"])

                    # Append jsonLine to jsonLinesFile
                    jsonLinesFile.append(jsonLine)

        except FileNotFoundError:
            # File not found error - just ignore.
            pass

        # Return the jsonLinesFile list.
        return jsonLinesFile

    def __init__(self):
        """Initialize the mongo_data class."""
        self.initialized = True
        self.version = "0.01"
