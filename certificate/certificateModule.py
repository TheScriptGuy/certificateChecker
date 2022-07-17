# Certificate Module1
# Version: 0.11
# Last updated: 2022-07-16
# Author: TheScriptGuy

import ssl
import socket
import datetime
import json
import requests

from dateutil.relativedelta import relativedelta


class certificateModule:
    """certificateModule class"""

    @staticmethod
    def getCertificate(__hostname, __port):
        """Connect to the host and get the certificate."""
        __ctx = ssl.create_default_context()

        # Initialize the __hostnameData object.
        __hostnameData = {
            "certificateMetaData": None,
            "connectionCipher": None,
        }

        try:
            with __ctx.wrap_socket(socket.socket(), server_hostname=__hostname) as s:
                s.connect((__hostname, __port))
                __certificate = s.getpeercert()
                __cipher = s.cipher()
                __hostnameData["certificateMetaData"] = __certificate
                __hostnameData["connectionCipher"] = __cipher

        except ssl.SSLCertVerificationError as e:
            connectHost = __hostname + ":" + str(__port)
            print(connectHost + ' - Certificate error - ', e.verify_message)

        except socket.gaierror as e:
            connectHost = __hostname + ":" + str(__port)
            print(connectHost + ' - Socket error - ', e.strerror)

        except FileNotFoundError as e:
            connectHost = __hostname + ":" + str(__port)
            print(connectHost + ' - File not found - ', e.strerror)

        except TimeoutError as e:
            connectHost = __hostname + ":" + str(__port)
            print(connectHost + ' - Timeout error - ', e.strerror)

        except OSError as e:
            connectHost = __hostname + ":" + str(__port)
            print(connectHost + ' - OSError - ', e.strerror)

        return __hostnameData

    @staticmethod
    def printSubject(__certificateObject):
        """Print the subject name of the certificate."""
        if __certificateObject is not None:
            subject = dict(x[0] for x in __certificateObject['subject'])
            issued_to = subject['commonName']
            print("Subject: ", issued_to, end='')

    @staticmethod
    def printSubjectAltName(__certificateObject):
        """Print the Subject Alternate Name(s) of the certificate."""
        __subjectAltName = []

        for field, value in __certificateObject['subjectAltName']:
            __subjectAltName.append({field: value})

        print("Subject Alt Name: ", __subjectAltName)

    @staticmethod
    def printIssuer(__certificateObject):
        """Print the Issuer of the certificate."""
        if __certificateObject is not None:
            issuer = dict(x[0] for x in __certificateObject['issuer'])
            issued_by = issuer['commonName']
            print("Issued by: ", issued_by)

    @staticmethod
    def printNotBefore(__certificateObject):
        """Print the notBefore field of the certificate."""
        if __certificateObject is not None:
            notBefore = __certificateObject['notBefore']
            print("Certificate start date: ", notBefore)

    @staticmethod
    def printNotAfter(__certificateObject):
        """Print the notAfter field of the certificate."""
        if __certificateObject is not None:
            notAfter = __certificateObject['notAfter']
            print("Certificate end date: ", notAfter)

    @staticmethod
    def returnNotBefore(__certificateObject):
        """Return the notBefore field from the certificate."""
        if __certificateObject is not None:
            return __certificateObject['notBefore']
        return ""

    @staticmethod
    def returnNotAfter(__certificateObject):
        """Return the notAfter field from the certificate."""
        if __certificateObject is not None:
            return __certificateObject['notAfter']
        return ""

    def howMuchTimeLeft(self, __certificateObject):
        """Return the remaining time left on the certificate."""
        if __certificateObject is not None:
            timeNow = datetime.datetime.utcnow().replace(microsecond=0)
            certNotAfter = datetime.datetime.strptime(self.returnNotAfter(__certificateObject["certificateMetaData"]), self.certTimeFormat)

            __delta = relativedelta(certNotAfter, timeNow)

            myDeltaDate = {
                'years': __delta.years,
                'months': __delta.months,
                'days': __delta.days,
                'hours': __delta.hours,
                'minutes': __delta.minutes,
                'seconds': __delta.seconds,
            }
            timeLeft = []

            for field in myDeltaDate:
                if myDeltaDate[field] > 1:
                    timeLeft.append("%d %s" % (myDeltaDate[field], field))
                else:
                    if myDeltaDate[field] == 1:
                        timeLeft.append("%d %s" % (myDeltaDate[field], field[:-1]))

            certResult = ', '.join(timeLeft)
        else:
            certResult = "Invalid certificate"
        return certResult

    @staticmethod
    def checkIssuer(__certificateObject):
        """Check to see if issuers are trusted."""
        return True

    @staticmethod
    def checkRevocation(__certificateObject):
        """Check to see if certificate hasn't been revoked."""
        return True

    def checkTimeValidity(self, __certificateObject):
        """
        Check to see if the certificate is valid:
            current date is after certificate start date
            current date is before certificate expiry date
        """
        if __certificateObject is not None:
            timeNow = datetime.datetime.utcnow().replace(microsecond=0).date()
            certNotAfter = datetime.datetime.strptime(self.returnNotAfter(__certificateObject), self.certTimeFormat).date()
            certNotBefore = datetime.datetime.strptime(self.returnNotBefore(__certificateObject), self.certTimeFormat).date()

            # Assume time not valid
            isValid = bool((certNotBefore < timeNow) and (certNotAfter > timeNow))

            return isValid
        return False

    @staticmethod
    def printOCSP(__certificateObject):
        """Print the OCSP field of the certificate."""
        if __certificateObject is not None:
            __OCSPList = []
            for value in __certificateObject['OCSP']:
                __OCSPList.append(value)
            print("OCSP: ", __OCSPList)

    @staticmethod
    def printCRLDistributionPoints(__certificateObject):
        """Print the CRL distribution points of the certificate."""
        if __certificateObject is not None:
            __CRLList = []
            if 'crlDistributionPoints' in __certificateObject:
                for value in __certificateObject['crlDistributionPoints']:
                    __CRLList.append(value)
                print("CRL: ", __CRLList)

    @staticmethod
    def printCertificateSerialNumber(__certificateObject):
        """Print the certificate serial number."""
        if __certificateObject is not None:
            certificateSerialNumber = __certificateObject['serialNumber']
            print("Serial Number: ", certificateSerialNumber)

    @staticmethod
    def printCaIssuers(__certificateObject):
        """Print the certificates CA issuers."""
        if __certificateObject is not None:
            certificateCaIssuers = __certificateObject['caIssuers']
            print("CA Issuers: ", certificateCaIssuers)

    def printHowMuchTimeLeft(self, __certificateObject):
        """Print how much time is left on the certificate."""
        if __certificateObject is not None:
            timeLeft = self.howMuchTimeLeft(__certificateObject)
            print("Time left: ", timeLeft)

    def certificateValid(self, __certificateObject):
        """
        Currently not in use.
        Check to see if the certificate is valid (Time, Recovation, Issuer)
        """
        if __certificateObject is not None:
            if self.checkTimeValidity(__certificateObject) and self.checkRevocation(__certificateObject) and self.checkIssuer(__certificateObject):
                print("Certificate good!")
            else:
                print("Certificate invalid!")

    def printCertInfo(self, __certificateObject):
        """Print out all the certificate properties."""
        if __certificateObject is not None:
            self.printSubject(__certificateObject)
            print()
            self.printIssuer(__certificateObject)
            self.printSubjectAltName(__certificateObject)
            self.printNotBefore(__certificateObject)
            self.printNotAfter(__certificateObject)
            self.printOCSP(__certificateObject)
            self.printCRLDistributionPoints(__certificateObject)
            self.printCaIssuers(__certificateObject)
            self.printCertificateSerialNumber(__certificateObject)
            self.printHowMuchTimeLeft(__certificateObject)
        else:
            print("No certificate info to display!")

    def printCertInfoJSON(self, __certificateObject):
        """Print the certificate information in JSON format."""
        if __certificateObject is not None:
            jsonCertInfoFormat = json.dumps(__certificateObject)
            print(jsonCertInfoFormat)
        else:
            jsonCertInfoFormat = {
                "subject": {"None": "None"},
                "certificateIssuer" : {"None": "None"},
                "version" : 0,
                "serialNumber" : "0",
                "notBefore" : "Jan 1 00:00:00 0000 GMT",
                "notAfter" : "Jan 1 00:00:00 0000 GMT",
                "timeLeft" : "0 seconds",
                "OCSP" : "None",
                "crlDistributionPoints" : "None",
                "caIssuers" : "None",
                "subjectAltName" : {"None": "None"}
            }
            print(jsonCertInfoFormat)

    def calculateCertificateUtilization(self, __notBefore, __notAfter):
        """Calculating the percentage utilization of the certificate"""
        # Convert __notBefore to datetime object
        notBeforeTime = datetime.datetime.strptime(__notBefore, self.certTimeFormat)
        # Convert __notAfter to datetime object
        notAfterTime = datetime.datetime.strptime(__notAfter, self.certTimeFormat)

        # Get the current time.
        currentTime = datetime.datetime.utcnow()

        # Calculate the differences between currentTime, notAfterTime, and notBeforeTime
        rest = notAfterTime - currentTime
        total = notAfterTime - notBeforeTime

        # Calculate the percentage utilization of the time available before expiry.
        percentageUtilization = 100 - (rest / total * 100)

        # Return the percentage utilization as a string formatted to 2 places.
        return float(f"{percentageUtilization:.2f}")

    def calculateCertificateTemplateTime(self, __notBefore, __notAfter):
        """Calculate the number of seconds between __notBefore and __notAfter."""
        # Convert __notBefore to datetime object
        notBeforeTime = datetime.datetime.strptime(__notBefore, self.certTimeFormat)
        # Convert __notAfter to datetime object
        notAfterTime = datetime.datetime.strptime(__notAfter, self.certTimeFormat)

        # Calcualte the difference
        timeDifference = notAfterTime - notBeforeTime

        # Get the number of seconds from the calculation above
        timeDifferenceInSeconds = int(timeDifference.total_seconds())

        return timeDifferenceInSeconds

    def convertCertificateObject2Json(self, __hostname, __port, __startTime, __endTime, __certificateObject):
        """Convert the certificate object into JSON format."""
        myJsonCertificateInfo = {}

        startTime = __startTime.isoformat()
        endTime = __endTime.isoformat()

        # Calculate queryTime between __endTime and __startTime in milliseconds
        queryTime = round(float((__endTime - __startTime).total_seconds() * 1000), 2)

        myJsonCertificateInfo["hostname"] = __hostname
        myJsonCertificateInfo["port"] = int(__port)
        myJsonCertificateInfo["startTime"] = startTime
        myJsonCertificateInfo["endTime"] = endTime
        myJsonCertificateInfo["queryTime"] = queryTime

        if __certificateObject["connectionCipher"] is not None:
            myJsonCertificateInfo["connectionCipher"] = __certificateObject["connectionCipher"]

        myJsonCertificateInfo["certificateInfo"] = {}

        if __certificateObject["certificateMetaData"] is not None:

            certKeys = __certificateObject.keys()

            # Certificate might not have subject defined.
            if 'subject' in certKeys:
                myJsonCertificateInfo["certificateInfo"]["subject"] = dict(x[0] for x in __certificateObject["certificateMetaData"]["subject"])

            myJsonCertificateInfo["certificateInfo"]["certificateIssuer"] = dict(x[0] for x in __certificateObject["certificateMetaData"]["issuer"])

            myJsonCertificateInfo["certificateInfo"]["version"] = __certificateObject["certificateMetaData"]["version"]
            myJsonCertificateInfo["certificateInfo"]["serialNumber"] = __certificateObject["certificateMetaData"]["serialNumber"]
            myJsonCertificateInfo["certificateInfo"]["notBefore"] = __certificateObject["certificateMetaData"]["notBefore"]
            myJsonCertificateInfo["certificateInfo"]["notAfter"] = __certificateObject["certificateMetaData"]["notAfter"]

            # Certificate might not have OCSP defined
            if "OCSP" in certKeys:
                myJsonCertificateInfo["certificateInfo"]["OCSP"] = __certificateObject["certificateMetaData"]["OCSP"]

            # Certificate might not have CRL defined
            if "crlDistributionPoints" in certKeys:
                myJsonCertificateInfo["certificateInfo"]["crlDistributionPoints"] = __certificateObject["certificateMetaData"]["crlDistributionPoints"]

            myJsonCertificateInfo["certificateInfo"]["caIssuers"] = __certificateObject["certificateMetaData"]["caIssuers"]

            # Initialize subjectAltName
            myJsonCertificateInfo["certificateInfo"]["subjectAltName"] = {}
            # Keep track of how many entries there are
            subjectAltNameCounter = 0

            for field, value in __certificateObject["certificateMetaData"]["subjectAltName"]:
                myJsonCertificateInfo["certificateInfo"]["subjectAltName"].update({field + str(subjectAltNameCounter): value})
                subjectAltNameCounter += 1

            # Time left on certificate
            myJsonCertificateInfo["timeLeft"] = self.howMuchTimeLeft(__certificateObject)

            # Percentage Utilization of certificate
            myJsonCertificateInfo["percentageUtilization"] = self.calculateCertificateUtilization(__certificateObject["certificateMetaData"]["notBefore"], __certificateObject["certificateMetaData"]["notAfter"])

            # Certificate template time validity
            # Work out the time that certificates are issued for
            myJsonCertificateInfo["certificateTemplateTime"] = self.calculateCertificateTemplateTime(__certificateObject["certificateMetaData"]["notBefore"], __certificateObject["certificateMetaData"]["notAfter"])

            # Reset number of entries
            subjectAltNameCounter = 0

        else:
            myJsonCertificateInfo["certificateInfo"]["subject"] = {"None": "None"}
            myJsonCertificateInfo["certificateInfo"]["certificateIssuer"] = {"None": "None"}
            myJsonCertificateInfo["certificateInfo"]["version"] = 0
            myJsonCertificateInfo["certificateInfo"]["serialNumber"] = "0"
            myJsonCertificateInfo["certificateInfo"]["notBefore"] = "Jan 1 00:00:00 0000 GMT"
            myJsonCertificateInfo["certificateInfo"]["notAfter"] = "Jan 1 00:00:00 0000 GMT"
            myJsonCertificateInfo["certificateInfo"]["OCSP"] = "None"
            myJsonCertificateInfo["certificateInfo"]["crlDistributionPoints"] = "None"
            myJsonCertificateInfo["certificateInfo"]["caIssuers"] = "None"
            myJsonCertificateInfo["certificateInfo"]["subjectAltName"] = {"None": "None"}
            myJsonCertificateInfo["percentageUtilization"] = 0.00
            myJsonCertificateInfo["timeLeft"] = "0 seconds"
            myJsonCertificateInfo["certificateTemplateTime"] = 0
            myJsonCertificateInfo["connectionCipher"] = []

        return myJsonCertificateInfo

    def uploadJsonData(self, __certificateJsonData, __httpUrl):
        """
        This will upload the json data to a URL via a POST method.
        If the verbose argument is set, it'll display what URL it's being
        submitted to as well as the json data (jsonData).
        When the response is returned, it'll return the X-Headers that are sent back
        from the server.
        """
        x = requests.post(__httpUrl, json=__certificateJsonData)
        return x.headers

    def __init__(self):
        """Initialize the class."""
        self.initialized = True
        self.moduleVersion = "0.11"
        self.certificate = {}

        # Certificate date/time format that is to be interpreted by datetime module.
        self.certTimeFormat = "%b %d %H:%M:%S %Y %Z"
