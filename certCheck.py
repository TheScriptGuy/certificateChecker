# Program:        Certificate Checker
# Author:         Nolan Rumble
# Date:           2022/05/26
# Version:        0.16

import argparse
import datetime
import sys
import json

from systemInfo import systemInfo, systemData
from certificate import certificateModule
from data import certData
from data import sendDataMongoDB

scriptVersion = "0.16"

# Global Variables
args = None
o_myCertificate = None
o_myInfo = None
o_mySystemData = None


def parseArguments():
    """Create argument options and parse through them to determine what to do with script."""
    # Instantiate the parser
    parser = argparse.ArgumentParser(description='Certificate Checker v' + scriptVersion)

    # Optional arguments
    parser.add_argument('--hostname', default="google.com",
                        help='Hostname to get certificate from. Defaults to google.com')

    parser.add_argument('--displayCertificate', action='store_true',
                        help='Display certificate info')

    parser.add_argument('--displayCertificateJSON', action='store_true',
                        help='Display certificate info in JSON format')

    parser.add_argument('--displayScriptDataJSON', action='store_true',
                        help='Display script info and queried certificates in JSON format')

    parser.add_argument('--displayTimeLeft', action='store_true',
                        help='Display time left until expiry on certificate.')

    parser.add_argument('--queryFile', default='',
                        help='Import a query file to for hostname queries. Supports local files and HTTP/HTTPS links')

    parser.add_argument('--uploadJsonData', default='',
                        help='Upload JSON data to HTTP URL via HTTP POST method.')

    parser.add_argument('--mongoDB', action='store_true',
                        help='Upload results to MongoDB. Connection details stored in mongo.cfg')

    parser.add_argument('--setTag', default='',
                        help='Set the tag for the query results. Creates tag.cfg file with tag. Use commas to separate multiple tags.')

    parser.add_argument('--deleteTag', action='store_true',
                        help='Delete the tag file - tag.cfg')

    parser.add_argument('--getTag', action='store_true',
                        help='Get the tag from tag.cfg file')

    parser.add_argument('--renewUuid', action='store_true',
                        help='Renew the UUID value.')

    parser.add_argument('--getUuid', action='store_true',
                        help='Get the UUID value from uuid.cfg file.')

    parser.add_argument('--deleteUuid', action='store_true',
                        help='Remove the UUID value. Caution: when script runs again a new UUID will be generated.')

    global args

    args = parser.parse_args()


def defineInfoArguments(o_systemData, o_systemInfo):
    """This validates the arguments used for tag and uuid definitions."""
    # If setTag argument is set, create the new Tag.
    if args.setTag:
        o_systemData.setTag(args.setTag)
        print('New tag set.')
        sys.exit(0)

    # If getTag is set, it will grab the value in tag.cfg file.
    if args.getTag:
        print(o_systemInfo.getTag())
        sys.exit(0)

    # If deleteTag is set, it will delete the tag.cfg file.
    if args.deleteTag:
        o_systemData.deleteTag()
        sys.exit(0)

    # If getUuid is set, it grab the value in uuid.cfg
    if args.getUuid:
        print(o_systemInfo.getUuid())
        sys.exit(0)

    # If deleteUuid is set, the uuid.cfg file will be deleted.
    if args.deleteUuid:
        o_systemData.deleteUuid()
        sys.exit(0)

    # If renewUuid is set, first delete uuid.cfg file, then generate a new uuid.
    if args.renewUuid:
        o_systemData.deleteUuid()
        o_systemData.createUuidIfNotExist()
        sys.exit(0)


def gatherData(certResults):
    """
    This will collect all the data into a uniform data structure that can
    help with measuring results across multiple executions.

    Data that is included is:
    * deviceUuid         - a unique device identifier.
    * deviceTag          - a tag for the device to help with aggregating data across.
                           multiple endpoints (for example all production, development, qa devices).
    * hostName           - the hostname of the device where script is executing.
    * scriptUTCStartTime - script start time (UTC format).
    * scriptUTCEndTime   - script end time (UTC format).
    * queryResults       - The results of all queries that were performed against the nameservers.
    """
    myInfo = systemInfo.systemInfo()

    if myInfo.uuid == "":
        n = systemData.systemData()
        n.createUuidIfNotExist()
        myInfo.uuid = myInfo.getUuid()

    myData = {
        "deviceUuid": myInfo.uuid,
        "deviceTag": myInfo.deviceTag,
        "clientHostName": myInfo.hostname,
        "dataFormatVersion": 5,
        "certResults": certResults
    }

    return myData


def checkArguments(__myCertificate, __jsonCertificateInfo):
    """This will see how the data needs to be displayed to stdout."""
    if args.displayCertificateJSON:
        # Display the certificate JSON structure
        o_myCertificate.printCertInfoJSON(__jsonCertificateInfo)

    if __myCertificate is not None:
        if args.displayCertificate:
            o_myCertificate.printCertInfo(__myCertificate)

        if args.displayTimeLeft:
            # Display the remaining time left on the certificate being queried.
            o_myCertificate.printSubject(__myCertificate)
            print(" ", o_myCertificate.howMuchTimeLeft(__myCertificate))


def processQueryFile():
    """
    This will get all the contents of the query file to be used when polling
    multiple hosts
    """
    # First check to see if the --displayCertificateJSON argument is used.
    # This argument cannot be used in conjunction with the --queryFile argument
    if args.displayCertificateJSON:
        print("Please use the --displayScriptDataJSON argument with the query file option")
        sys.exit(1)

    myCertData = certData.certData()

    jsonScriptData = []

    for myHostname in myCertData.loadQueriesFile(args.queryFile):
        # Define initial certificate object
        o_myCertificate = certificateModule.certificateModule()

        # For SSL performance measurement - START
        o_startTime = datetime.datetime.now()

        # Connect to the hostname from the queryFile argument and get the certificate associated with it.
        myCertificate = o_myCertificate.getCertificate(myHostname["hostname"], myHostname["port"])

        # For SSL performance measurement - END
        o_endTime = datetime.datetime.now()

        # Convert the certificate object into JSON format.
        jsonCertificateInfo = o_myCertificate.convertCertificateObject2Json(myHostname["hostname"], myHostname["port"], o_startTime, o_endTime, myCertificate)

        jsonScriptData.append(jsonCertificateInfo)

        checkArguments(myCertificate, jsonCertificateInfo)

    myJsonScriptData = gatherData(jsonScriptData)

    if args.displayScriptDataJSON:
        # Display the certificate and system JSON structure
        print(json.dumps(myJsonScriptData))

    if args.uploadJsonData:
        # Upload the system data and certificate information to the appropriate URL
        print(o_myCertificate.uploadJsonData(myJsonScriptData, args.uploadJsonData))

    if args.mongoDB:
        # Upload the data to the mongoDB, defined by mongo.cfg
        # Define the sendDataMongoDB object
        sdMDB = sendDataMongoDB.sendDataMongoDB()
        uploadResult = sdMDB.uploadDataToMongoDB(jsonScriptData)
        print(uploadResult)


def processHostname():
    """This will attempt to connect to the hostname defined by the --hostname argument."""
    # Define initial certificate object
    o_myCertificate = certificateModule.certificateModule()

    # For SSL performance measurement - START
    o_startTime = datetime.datetime.now()

    # Connect to the hostname from the --hostname argument and get the certificate associated with it.
    if ":" in args.hostname:
        tmpLine = args.hostname.split(':')
        hostnameQuery = {"hostname": tmpLine[0], "port": int(tmpLine[1])}

    else:
        hostnameQuery = {"hostname": args.hostname, "port": 443}

    myCertificate = o_myCertificate.getCertificate(hostnameQuery["hostname"], hostnameQuery["port"])

    # For SSL performance measurement - END
    o_endTime = datetime.datetime.now()

    # Convert the certificate object into JSON format.
    jsonCertificateInfo = o_myCertificate.convertCertificateObject2Json(hostnameQuery["hostname"], hostnameQuery["port"], o_startTime, o_endTime, myCertificate)

    # Append system data to JSON certificate structure
    jsonScriptData = gatherData(jsonCertificateInfo)

    if args.displayCertificateJSON:
        # Display the certificate JSON structure
        o_myCertificate.printCertInfoJSON(jsonCertificateInfo)

    if args.displayCertificate:
        # Display the certificate properties.
        o_myCertificate.printCertInfo(myCertificate)

    if args.displayTimeLeft:
        # Display the remaining time left on the certificate being queried.
        print(o_myCertificate.howMuchTimeLeft(myCertificate))

    if args.displayScriptDataJSON:
        # Display the certificate and system JSON structure
        myJSONScriptData = json.dumps(jsonScriptData)
        print(myJSONScriptData)

    if args.uploadJsonData:
        # Upload the system data and certificate information to the appropriate URL
        print(o_myCertificate.uploadJsonData(jsonScriptData, args.uploadJsonData))

    if args.mongoDB:
        # Upload the data to the mongoDB, defined by mongo.cfg
        # Define the sendDataMongoDB object
        sdMDB = sendDataMongoDB.sendDataMongoDB()
        uploadResult = sdMDB.uploadDataToMongoDB(jsonScriptData)
        print(uploadResult)


if __name__ == "__main__":
    # Get all the arguments sent through to the script
    parseArguments()

    # Set initial objects for systemData and systemInfo
    o_mySystemData = systemData.systemData()
    o_myInfo = systemInfo.systemInfo()

    # Gather system data and info
    defineInfoArguments(o_mySystemData, o_myInfo)

    # initialize jsonCertificateInfo
    jsonCertificateInfo = {}
    jsonScriptData = {}

    if args.queryFile:
        processQueryFile()
        sys.exit(0)

    if args.hostname:
        processHostname()
        sys.exit(0)
