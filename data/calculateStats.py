# Class:          calculateStats
# Author:         Nolan Rumble
# Date:           2022/11/20
# Version:        0.03

import argparse
import datetime
import sys
import time

from dateutil.relativedelta import relativedelta


class calculateStats:
    """This calculates statistics off the data provided."""

    @staticmethod
    def convertTimeIntoHumanReadable(__seconds):
        """Return the remaining time left on the certificate."""
        # Get date/time since epoch based off seconds
        myDateTime = datetime.datetime.fromtimestamp(__seconds)

        # Create epoch time datetime object.
        beginDate = datetime.date(1970, 1, 1)

        # Calculate the difference between the 2 dates myDateTime and beginDate
        myDateTimeObject = relativedelta(myDateTime, beginDate)

        myDateTime = {
            'years': myDateTimeObject.years,
            'months': myDateTimeObject.months,
            'days': myDateTimeObject.days,
            'hours': myDateTimeObject.hours,
            'minutes': myDateTimeObject.minutes,
            'seconds': myDateTimeObject.seconds,
        }

        timeYMDHMS = []

        # Iterate through the myDateTime dict and formulate a list of the values.
        # If the delimeter field is 0, don't include it in final result
        for field in myDateTime:
            if myDateTime[field] > 1:
                humanReadable = f"{myDateTime[field]} {field}"
                timeYMDHMS.append(humanReadable)
            else:
                if myDateTime[field] == 1:
                    humanReadable = f"{myDateTime[field]} {field[:-1]}"
                    timeYMDHMS.append(humanReadable)
        myDateTimeString = ', '.join(timeYMDHMS)

        # Return the human readable form string.
        return myDateTimeString

    def calculateStatistics(self, __certResults):
        """Returns statistics based off certificate information provided."""
        # Calculate the average utilization and query time across all tests.
        avgUtilization = float(0)
        avgQueryTime = float(0)
        avgTemplateTimeSeconds = float(0)

        lowestCertificateTemplateTime = 9999999999999
        highestCertificateTemplateTime = 0

        successfulTests = 0
        failedTests = 0

        commonCAIssuers = {}

        commonCipherInfoCount = {
            "bits": {},
            "cipher": {},
            "version": {}
        }

        combinedStatistics = {
            "numberOfTests": {
                "success": 0,
                "failed": 0
            },
            "averageCertificateUtilization": 0.0,
            "averageQueryTime": 0.0,
            "averageTemplateTimeSeconds": 0,
            "averageTemplateTimeHumanReadable": 0,
            "lowestCertificateTemplateTime": 0,
            "lowestCertificateTemplateTimeHumanReadable": "0 seconds",
            "highestCertificateTemplateTime": 0,
            "highestCertificateTemplateTimeHumanReadable": "0 seconds",
            "commonCAIssuersCount": commonCAIssuers,
            "commonCipherInfoCount": commonCipherInfoCount
        }
        for item in __certResults:
            if item["certificateInfo"]["version"] != 0:
                avgUtilization += item["percentageUtilization"]
                avgQueryTime += item["queryTime"]
                avgTemplateTimeSeconds += item["certificateTemplateTime"]

                # Calculate lowest certificate template time.
                if lowestCertificateTemplateTime > item["certificateTemplateTime"]:
                    lowestCertificateTemplateTime = item["certificateTemplateTime"]

                # Calculate highest certificate template time.
                if highestCertificateTemplateTime < item["certificateTemplateTime"]:
                    highestCertificateTemplateTime = item["certificateTemplateTime"]

                caIssuerCommonName = item["certificateInfo"]["certificateIssuer"]["commonName"]

                # Calculate common Certificate Authority Issuers
                if caIssuerCommonName in commonCAIssuers:
                    commonCAIssuers[caIssuerCommonName] += 1
                else:
                    commonCAIssuers[caIssuerCommonName] = 1

                # Calculate common cipher connection details
                if str(item["connectionCipher"][0]) in commonCipherInfoCount["cipher"]:
                    commonCipherInfoCount["cipher"][str(item["connectionCipher"][0])] += 1
                else:
                    commonCipherInfoCount["cipher"][str(item["connectionCipher"][0])] = 1

                connectionCipherVersion = str(item["connectionCipher"][1]).replace(".", "")

                if connectionCipherVersion in commonCipherInfoCount["version"]:
                    commonCipherInfoCount["version"][connectionCipherVersion] += 1
                else:
                    commonCipherInfoCount["version"][connectionCipherVersion] = 1

                connectionCipherBits = str(item["connectionCipher"][2])
                if connectionCipherBits in commonCipherInfoCount["bits"]:
                    commonCipherInfoCount["bits"][connectionCipherBits] += 1
                else:
                    commonCipherInfoCount["bits"][connectionCipherBits] = 1

                # Increment number of successful tests
                successfulTests += 1
            else:
                # Incrememt number of failed tests
                failedTests += 1

        # Round the values to 2 decimal places.
        if successfulTests > 0:
            avgUtilization = round(avgUtilization / successfulTests, 2)
            avgQueryTime = round(avgQueryTime / successfulTests, 2)
            avgTemplateTimeSeconds = int(round(avgTemplateTimeSeconds / successfulTests, 2))

            combinedStatistics = {
                "numberOfTests": {
                    "success": successfulTests,
                    "failed": failedTests
                },
                "averageCertificateUtilization": avgUtilization,
                "averageQueryTime": avgQueryTime,
                "averageTemplateTimeSeconds": avgTemplateTimeSeconds,
                "averageTemplateTimeHumanReadable": self.convertTimeIntoHumanReadable(avgTemplateTimeSeconds),
                "lowestCertificateTemplateTime": lowestCertificateTemplateTime,
                "lowestCertificateTemplateTimeHumanReadable": self.convertTimeIntoHumanReadable(lowestCertificateTemplateTime),
                "highestCertificateTemplateTime": highestCertificateTemplateTime,
                "highestCertificateTemplateTimeHumanReadable": self.convertTimeIntoHumanReadable(highestCertificateTemplateTime),
                "commonCAIssuersCount": commonCAIssuers,
                "commonCipherInfoCount": commonCipherInfoCount
            }   
        else:
            combinedStatistics["numberOfTests"]["failed"] = failedTests

        return combinedStatistics

    def combineData(self, __certResults, __mySystemInfo, __scriptStartTime, __scriptEndTime):
        """Combines all the data into structured data."""
        # Convert script start/end times into string isoformat
        scriptStartTime = __scriptStartTime.isoformat()
        scriptEndTime = __scriptEndTime.isoformat()
        scriptExecutionTime = round(float((__scriptEndTime - __scriptStartTime).total_seconds() * 1000), 2)

        # Get all the statistics for the measurements performed
        statistics = self.calculateStatistics(__certResults)

        # Create the json script structure with all the meta data.
        myData = {
            "tenantId": __mySystemInfo.myConfigJson["myTenantId"],
            "deviceId": __mySystemInfo.myConfigJson["myDeviceId"],
            "deviceTag": __mySystemInfo.myConfigJson["myTags"],
            "clientHostName": __mySystemInfo.hostname,
            "dataFormatVersion": self.dataFormatVersion,
            "queryStatistics": {
                "scriptStartTime": scriptStartTime,
                "scriptEndTime": scriptEndTime,
                "scriptExecutionTime": scriptExecutionTime,
                "averageQueryTime": statistics["averageQueryTime"],
                "averageCertificateUtilization": statistics["averageCertificateUtilization"],
                "averageTemplateTime": statistics["averageTemplateTimeSeconds"],
                "averageTemplateTimeHumanReadable": statistics["averageTemplateTimeHumanReadable"],
                "lowestCertificateTemplateTime": statistics["lowestCertificateTemplateTime"],
                "lowestCertificateTemplateTimeHumanReadable": statistics["lowestCertificateTemplateTimeHumanReadable"],
                "highestCertificateTemplateTime": statistics["highestCertificateTemplateTime"],
                "highestCertificateTemplateTimeHumanReadable": statistics["highestCertificateTemplateTimeHumanReadable"],
                "commonCAIssuersCount": statistics["commonCAIssuersCount"],
                "commonCipherInfoCount": statistics["commonCipherInfoCount"],
                "numberofTests": statistics["numberOfTests"]
            },
            "certResults": __certResults
        }

        return myData

    def __init__(self):
        """Initialize the sendDataMongoDB class."""
        self.initialized = True
        self.version = "0.03"
        self.dataFormatVersion = 20

