# Program:        Certificate Checker
# Author:         Nolan Rumble
# Date:           2022/03/05
# Version:        0.03
scriptVersion = "0.03"

import ssl, socket
import argparse
import datetime
import json

from dateutil.relativedelta import relativedelta


def getCertificate(__hostname):
    ctx = ssl.create_default_context()
    try:
        with ctx.wrap_socket(socket.socket(), server_hostname=__hostname) as s:
            s.connect((__hostname, 443))
            cert = s.getpeercert()
            return cert
    except ssl.SSLCertVerificationError as e:
        print('Certificate error - ',e.verify_message)
        return None
    except socket.gaierror as e:
        print('Socket error - ',e.strerror)

def printSubject(__certificateObject):
    if __certificateObject != None:
        subject = dict(x[0] for x in __certificateObject['subject'])
        issued_to = subject['commonName']
        print(issued_to)

def printSubjectAltName(__certificateObject):
    __subjectAltName = []

    for field,value in __certificateObject['subjectAltName']:
        __subjectAltName.append({field:value})
    
    print(__subjectAltName)

def printIssuer(__certificateObject):
    if __certificateObject != None:
        issuer = dict(x[0] for x in __certificateObject['issuer'])
        issued_by = issuer['commonName']
        print(issued_by)

def printNotBefore(__certificateObject):
    if __certificateObject != None:
        notBefore = __certificateObject['notBefore']
        print(notBefore)

def printNotAfter(__certificateObject):
    if __certificateObject != None:
        notAfter = __certificateObject['notAfter']
        print(notAfter)


def returnNotBefore(__certificateObject):
    if __certificateObject != None:
        return __certificateObject['notBefore']

def returnNotAfter(__certificateObject):
    if __certificateObject != None:
        return __certificateObject['notAfter']

def howMuchTimeLeft(__certificateObject):
    if __certificateObject != None:
        timeNow = datetime.datetime.now().replace(microsecond=0)
        certNotAfter = datetime.datetime.strptime(returnNotAfter(__certificateObject), '%b %d %H:%M:%S %Y %Z')
    
        __delta = relativedelta(certNotAfter,timeNow)

        myDeltaDate = {
            'years': __delta.years,
            'months': __delta.months,
            'days': __delta.days,
            'hours': __delta.hours,
            'days': __delta.days,
            'minutes': __delta.minutes,
            'seconds': __delta.seconds,
        }

        timeLeft = []

        for field in myDeltaDate:
            if myDeltaDate[field] > 1:
                timeLeft.append("%d %s" % (myDeltaDate[field],field))
            else:
                if myDeltaDate[field] == 1:
                    timeLeft.append("%d %s" % (myDeltaDate[field], field[:-1]))
    
        return ', '.join(timeLeft)

def checkIssuer(__certificateObject):
    return True

def checkRevocation(__certificateObject):
    return True

def checkTimeValidity(__certificateObject):
    if __certificateObject != None:
        timeNow = datetime.datetime.now().replace(microsecond=0).date()
        certNotAfter = datetime.datetime.strptime(returnNotAfter(__certificateObject), '%b %d %H:%M:%S %Y %Z').date()
        certNotBefore = datetime.datetime.strptime(returnNotBefore(__certificateObject), '%b %d %H:%M:%S %Y %Z').date()

    
        # Assume time not valid
        isValid = False

        if (certNotBefore < timeNow) and (certNotAfter > timeNow):
            isValid = True
        else:
            isValid = False

        return isValid

def printOCSP(__certificateObject):
    if __certificateObject != None:
        __OCSPList = []
        for value in __certificateObject['OCSP']:
            __OCSPList.append(value)
        print(__OCSPList)

def printCRLDistributionPoints(__certificateObject):
    if __certificateObject != None:
        __CRLList = []
    
        for value in __certificateObject['crlDistributionPoints']:
            __CRLList.append(value)
    
        print(__CRLList)

def printCertificateSerialNumber(__certificateObject):
    if __certificateObject != None:
        certificateSerialNumber = __certificateObject['serialNumber']
        print(certificateSerialNumber)

def printCaIssuers(__certificateObject):
    if __certificateObject != None:
        certificateCaIssuers = __certificateObject['caIssuers']
        print(certificateCaIssuers)

def printHowMuchTimeLeft(__certificateObject):
    if __certificateObject != None:
        timeLeft = howMuchTimeLeft(__certificateObject)
        print(timeLeft)

def certificateValid(__certificateObject):
    if __certificateObject != None:
        if checkTimeValidity(__certificateObject) and checkRevocation(__certificateObject) and checkIssuer(__certificateObject):
            print("Certificate good!")
        else:
            print("Certificate invalid!")

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

    parser.add_argument('--displayTimeLeft', action='store_true',
                        help='Display time left until expiry on certificate.')

    global args
    args = parser.parse_args()



def printCertInfo(__certificateObject):
    printSubject(__certificateObject)
    printIssuer(__certificateObject)
    printSubjectAltName(__certificateObject)
    printNotBefore(__certificateObject)
    printNotAfter(__certificateObject)
    printOCSP(__certificateObject)
    printCRLDistributionPoints(__certificateObject)
    printCaIssuers(__certificateObject)
    printCertificateSerialNumber(__certificateObject)
    printHowMuchTimeLeft(__certificateObject)

def printCertInfoJSON(__certificateObject):
    jsonCertInfoFormat = json.dumps(__certificateObject)
    print(jsonCertInfoFormat)

def convertCertificateObject2Json(__hostname,__startTime,__endTime,__certificateObject):
    myJsonCertificateInfo = {}
    certKeys = __certificateObject.keys()
    
    startTime = __startTime.strftime("%Y/%m/%d %H:%M:%S.%f")
    endTime = __endTime.strftime("%Y/%m/%d %H:%M:%S.%f")
    queryTime = str((__endTime - __startTime).total_seconds())

    myJsonCertificateInfo["dataVersion"] = 1
    myJsonCertificateInfo["hostname"] = __hostname
    myJsonCertificateInfo["startTime"] = startTime
    myJsonCertificateInfo["endTime"] = endTime
    myJsonCertificateInfo["queryTime"] = queryTime

    myJsonCertificateInfo["certificateInfo"] = {}

    # Certificate might not have subject defined.
    if 'subject' in certKeys:
        myJsonCertificateInfo["certificateInfo"]["subject"] = dict(x[0] for x in __certificateObject['subject'])
    
    myJsonCertificateInfo["certificateInfo"]["certificateIssuer"] = dict(x[0] for x in __certificateObject['issuer'])
    
    myJsonCertificateInfo["certificateInfo"]["version"] = __certificateObject['version']
    myJsonCertificateInfo["certificateInfo"]["serialNumber"] = __certificateObject['serialNumber']
    myJsonCertificateInfo["certificateInfo"]["notBefore"] = __certificateObject['notBefore']
    myJsonCertificateInfo["certificateInfo"]["notAfter"] = __certificateObject['notAfter']

    myJsonCertificateInfo["certificateInfo"]["timeLeft"] = howMuchTimeLeft(__certificateObject)

    # Certificate might not have OCSP defined
    if 'OCSP' in certKeys:
        myJsonCertificateInfo["certificateInfo"]["OCSP"] = __certificateObject['OCSP']
    
    # Certificate might not have CRL defined
    if 'crlDistributionPoints' in certKeys: 
        myJsonCertificateInfo["certificateInfo"]["crlDistributionPoints"] = __certificateObject['crlDistributionPoints']
    
    myJsonCertificateInfo["certificateInfo"]["caIssuers"] = __certificateObject['caIssuers']


    # Initialize subjectAltName
    myJsonCertificateInfo["certificateInfo"]["subjectAltName"] = {}
    # Keep track of how many entries there are
    subjectAltNameCounter = 0

    for field,value in __certificateObject['subjectAltName']:
        myJsonCertificateInfo["certificateInfo"]["subjectAltName"].update({field + str(subjectAltNameCounter):value})
        subjectAltNameCounter += 1

    # Reset number of entries
    subjectAltNameCounter = 0

    return myJsonCertificateInfo



if __name__ == "__main__":
    parseArguments()
    
    jsonCertificateInfo = {}

    obj_startTime = datetime.datetime.now()
    myCertificate = getCertificate(args.hostname)
    obj_endTime = datetime.datetime.now()

    
    if myCertificate != None:
        if args.displayCertificate:
            printCertInfo(myCertificate)
    
        if args.displayTimeLeft:
            howMuchTimeLeft(myCertificate)

        if args.displayCertificateJSON:
            jsonCertificateInfo = convertCertificateObject2Json(args.hostname,obj_startTime,obj_endTime,myCertificate)
            printCertInfoJSON(jsonCertificateInfo)
