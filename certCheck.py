# Program:        Certificate Checker
# Author:         Nolan Rumble
# Date:           2022/12/04
# Version:        0.34

import argparse
import datetime
import sys
import json
import time

from systemInfo import systemInfo
from certificate import certificateModule
from data import calculateStats
from data import certData
from data import sendDataMongoDB
from data import emailTemplateBuilder
from data import sendDataEmail

scriptVersion = "0.34"

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
    parser.add_argument('--hostname', default='',
                        help='Hostname to get certificate from')

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

    parser.add_argument('--sendEmail', action='store_true',
                        help='Send an email with the results. SMTP connection details stored in mail.cfg')

    parser.add_argument('--retryAmount', default=1,
                        help='Attempt to retry the connection if any error occured. Defaults to 1 attempt.')

    parser.add_argument('--timeBetweenRetries', default=1,
                        help='The number of seconds between each retry attempt if the connection fails. Defaults to 1 second.')

    parser.add_argument('--setTag', default='',
                        help='Set the tag for the query results. Use commas to separate multiple tags.')

    parser.add_argument('--delTag', action='store_true',
                        help='Removes the tags from the configuration file.')

    parser.add_argument('--getTag', action='store_true',
                        help='Get tags from the configuration file.')

    parser.add_argument('--renewDeviceId', action='store_true',
                        help='Renew the device UUID value.')

    parser.add_argument('--getDeviceId', action='store_true',
                        help='Get the device UUID value from configuration file.')

    parser.add_argument('--deleteDeviceId', action='store_true',
                        help='Remove the device UUID value. When script runs again a new UUID will be generated.')

    parser.add_argument('--setTenantId', default='',
                        help='Sets the tenant ID for the script.')

    parser.add_argument('--getTenantId', action='store_true',
                        help='Gets the tenant ID from configuration file.')

    parser.add_argument('--delTenantId', action='store_true',
                        help='Deletes the tenant ID from the configuration file.')

    parser.add_argument('--createBlankConfiguration', action='store_true',
                        help='Creates a blank configuration file template - myConfig.json. Overwrites any existing configuration')

    global args

    args = parser.parse_args()


def defineInfoArguments(o_systemInfo):
    """This validates the arguments used for tag and device Id, and tenant Id definitions."""
    # If createBlankConfiguration is set, create a blank configuration file template.
    if args.createBlankConfiguration:
        o_systemInfo.createBlankConfigurationFile()
        sys.exit(0)

    # If setTag argument is set, create the new Tag.
    if args.setTag:
        o_systemInfo.setTag(args.setTag)
        print('New tag set.')
        sys.exit(0)

    # If getTag is set, it will grab the value in tag.cfg file.
    if args.getTag:
        print(o_systemInfo.getTag())
        sys.exit(0)

    # If delTag is set, it will delete the tag(s) from the configuration file.
    if args.delTag:
        o_systemInfo.deleteTag()
        sys.exit(0)

    # If getDeviceId is set, retrieve it from the configuration file.
    if args.getDeviceId:
        print(o_systemInfo.getDeviceId())
        sys.exit(0)

    # If deleteDeviceId is set, remove it from the configuration file.
    if args.deleteDeviceId:
        o_systemInfo.deleteDeviceId()
        sys.exit(0)

    # If renewDeviceId is set, delete it from the configuration file.
    if args.renewDeviceId:
        o_systemInfo.deleteDeviceId()
        o_systemInfo.generateDeviceId()
        sys.exit(0)

    # If setTenantId is set, add it to the configuration file.
    if args.setTenantId:
        o_systemInfo.setTenantId(args.setTenantId)
        sys.exit(0)

    # If getTenantId is set, retrieve the tenant Id from the configuration file.
    if args.getTenantId:
        print(o_systemInfo.getTenantId())
        sys.exit(0)

    # If delTenantId is set, remove the tenant Id from the configuration file.
    if args.delTenantId:
        o_systemInfo.deleteTenantId()
        sys.exit(0)


def gatherData(__certResults, __scriptStartTime, __scriptEndTime):
    """
    This will collect all the data into a uniform data structure that can
    help with measuring results across multiple executions.

    Data that is included is:
    * myTenantId                     - a unique tenant identifier.
    * myDeviceId                     - a unique device identifier.
    * myDeviceTag                    - a tag for the device to help with aggregating data across.
                                       multiple endpoints (for example all production, development, qa devices).
    * hostName                       - the hostname of the device where script is executing.
    * scriptStartTime                - script start time (UTC format).
    * scriptEndTime                  - script end time (UTC format).
    * scriptExecutionTime            - script query time (difference between scriptEndTime and scriptStartTime.
    * averageQueryTime               - The average query time across all the tests.
    * averageCertificateUtilization  - Average certificate utilization across all the tests.
    * averageTemplateTime            - Average template time being used across all the tests.
    * queryResults                   - The results of all queries that were performed against the nameservers.
    """
    mySystemInfo = systemInfo.systemInfo()
    myDetails = calculateStats.calculateStats()

    # Create the json script structure with all the meta data.
    myData = myDetails.combineData(__certResults, mySystemInfo, __scriptStartTime, __scriptEndTime)

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


def emailSendResults(__myJsonScriptData):
    """Email the results. Use the mail.cfg file for configuration data."""
    # Send an email message with the results from the query.
    # First we define the emailTemplate object by using the emailTemplateBuilder class.
    emailTemplate = emailTemplateBuilder.emailTemplateBuilder("mail.cfg")

    # Build the text template from the results in myJsonScriptData
    emailTemplate.buildEmailFromTextTemplate(__myJsonScriptData)

    # Build the HTML template from the results in myJsonScriptData
    emailTemplate.buildEmailFromHtmlTemplate(__myJsonScriptData)

    # Return the contents of the body message (text/html) to the myEmailMessage object.
    myEmailMessage = emailTemplate.returnBodyMessage()

    # Send the email.
    myEmailObject = sendDataEmail.sendDataEmail(myEmailMessage, "mail.cfg")


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

    scriptStartTime = datetime.datetime.utcnow()

    for myHostname in myCertData.loadQueriesFile(args.queryFile):
        # Define initial certificate object
        o_myCertificate = certificateModule.certificateModule()

        # For SSL performance measurement - START
        o_startTime = datetime.datetime.utcnow()

        # Iterate through number of retryAmount
        for counter in range(int(args.retryAmount)):
            # Connect to the hostname from the queryFile argument and get the certificate associated with it.
            myCertificate = o_myCertificate.getCertificate(myHostname["hostname"], myHostname["port"])

            if myCertificate["certificateMetaData"] is not None:
                break
            else:
                # If unable to connect to host for whatever reason, pause for a second then try again.
                time.sleep(int(args.timeBetweenRetries))

        # For SSL performance measurement - END
        o_endTime = datetime.datetime.utcnow()

        # Convert the certificate object into JSON format.
        jsonCertificateInfo = o_myCertificate.convertCertificateObject2Json(myHostname["hostname"], myHostname["port"], o_startTime, o_endTime, myCertificate)

        jsonScriptData.append(jsonCertificateInfo)

        checkArguments(myCertificate, jsonCertificateInfo)

    scriptEndTime = datetime.datetime.utcnow()

    myJsonScriptData = gatherData(jsonScriptData, scriptStartTime, scriptEndTime)

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
        uploadResult = sdMDB.uploadDataToMongoDB(myJsonScriptData)
        uploadTime = str(datetime.datetime.utcnow())
        print(uploadTime + " - " + str(uploadResult))

    if args.sendEmail:
        # Send an email with the results.
        emailSendResults(myJsonScriptData)


def processHostname():
    """This will attempt to connect to the hostname defined by the --hostname argument."""
    # Define initial certificate object
    o_myCertificate = certificateModule.certificateModule()

    # For SSL performance measurement - START
    o_startTime = datetime.datetime.utcnow()

    # Connect to the hostname from the --hostname argument and get the certificate associated with it.
    if ":" in args.hostname:
        tmpLine = args.hostname.split(':')
        hostnameQuery = {"hostname": tmpLine[0], "port": int(tmpLine[1])}

    else:
        hostnameQuery = {"hostname": args.hostname, "port": 443}

    # Iterate through number of retryAmount
    for counter in range(int(args.retryAmount)):
        # Connect to the hostname from the queryFile argument and get the certificate associated with it.
        myCertificate = o_myCertificate.getCertificate(hostnameQuery["hostname"], hostnameQuery["port"])
        if myCertificate["certificateMetaData"] is not None:
            break
        else:
            # If unable to connect to host for whatever reason, pause for a second then try again.
            time.sleep(int(args.timeBetweenRetries))

    # For SSL performance measurement - END
    o_endTime = datetime.datetime.utcnow()

    # Convert the certificate object into JSON format.
    jsonCertificateInfo = o_myCertificate.convertCertificateObject2Json(hostnameQuery["hostname"], hostnameQuery["port"], o_startTime, o_endTime, myCertificate)
    # Append system data to JSON certificate structure
    jsonScriptData = gatherData([jsonCertificateInfo], o_startTime, o_endTime)

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
        uploadTime = str(datetime.datetime.utcnow())
        print(uploadTime + " - " + str(uploadResult))

    if args.sendEmail:
        # Send an email with the results.
        emailSendResults(jsonScriptData)


if __name__ == "__main__":
    # Get all the arguments sent through to the script
    parseArguments()

    # Set initial objects for systemData and systemInfo
    o_myInfo = systemInfo.systemInfo()

    # Gather system data and info
    defineInfoArguments(o_myInfo)

    # initialize jsonCertificateInfo
    jsonCertificateInfo = {}
    jsonScriptData = []

    if args.queryFile:
        processQueryFile()
        sys.exit(0)

    if args.hostname:
        processHostname()
        sys.exit(0)
