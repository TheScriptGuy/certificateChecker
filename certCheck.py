# Program:        Certificate Checker
# Author:         Nolan Rumble
# Date:           2022/03/20
# Version:        0.06
scriptVersion = "0.06"

import argparse
import datetime
import sys
import json

from systemInfo import systemInfo,systemData
from certificate import certificateModule

def parseArguments():
    """
    Create argument options and parse through them to determine what to do with script.
    """

    # Instantiate the parser
    global scriptVersion
    parser = argparse.ArgumentParser(description='Certificate Checker V' + scriptVersion)

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

    parser.add_argument('--setTag', default='',
                        help='Set the tag for the query results. Creates tag.cfg file with tag.')
                
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
    global args
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
        "dataFormatVersion": 1,
        "certResults": certResults
    }

    return myData


if __name__ == "__main__":
    parseArguments()

    o_mySystemData = systemData.systemData()
    o_myInfo = systemInfo.systemInfo()

    defineInfoArguments(o_mySystemData,o_myInfo)

    jsonCertificateInfo = {}

    o_myCertificate = certificateModule.certificateModule()
    o_startTime = datetime.datetime.now()
    
    myCertificate = o_myCertificate.getCertificate(args.hostname)
    
    o_endTime = datetime.datetime.now()

    jsonCertificateInfo = o_myCertificate.convertCertificateObject2Json(args.hostname,o_startTime,o_endTime,myCertificate)
    
    jsonScriptData = gatherData(jsonCertificateInfo)

    if myCertificate != None:
        if args.displayCertificate:
            o_myCertificate.printCertInfo(myCertificate)
    
        if args.displayTimeLeft:
            print(o_myCertificate.howMuchTimeLeft(myCertificate))

        if args.displayCertificateJSON:
            o_myCertificate.printCertInfoJSON(jsonCertificateInfo)
        
        if args.displayScriptDataJSON:
            myJSONScriptData = json.dumps(jsonScriptData)
            print(myJSONScriptData)

