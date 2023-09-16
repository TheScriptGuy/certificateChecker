# Certificate Module
# Version:                 0.20
# Last updated:            2023-09-15
# Author:                  TheScriptGuy

import ssl
import socket
import datetime
import json
import requests
import hashlib
import os
import sys
from . import getCertificateChain

from dateutil.relativedelta import relativedelta


class certificateModule:
    """certificateModule class"""

    @staticmethod
    def getContextVariables() -> dict:
        """Get the variables from the contextVariables.json"""
        # Assume contextVariables is empty.
        contextVariables = None

        try:
            # Attempt to load the contextVariables.json file.
            with open('contextVariables.json') as fContextVariables:
                contextVariables = json.load(fContextVariables)

        except FileNotFoundError:
            print('I could not find contextVariables.json')

        return contextVariables

    def getCertificate(self, __hostinfo: dict) -> dict:
        """Connect to the host and get the certificate."""
        # Determine which context to create
        if __hostinfo['options'] is not None and \
                "local_untrusted_allow" in __hostinfo['options']:
            hostnamePortPair = f'{__hostinfo["hostname"]}:{__hostinfo["port"]}'
            certificateHashFilename = hashlib.sha256(
                hostnamePortPair.encode()
            ).hexdigest() + ".pem"

            if not os.path.exists(certificateHashFilename):
                # Try to build the chain
                occ = getCertificateChain.getCertificateChain()
                occ.getCertificateChain(
                    __hostinfo['hostname'],
                    __hostinfo['port']
                )
            
            # Lets try and see if we can create the right context with the hash file.
            try:
                __ctx = ssl.create_default_context(cafile=certificateHashFilename)
            except ssl.SSLError:
                print(f"An SSL error occured. Try deleting the {certificateHashFilename} file.")
                sys.exit(1)
        else:
            # Create the default context.
            __ctx = ssl.create_default_context()

        # Check to see if there are any options that need to be
        # passed for the connection
        if __hostinfo['options'] is not None:
            if "unsafe_legacy" in __hostinfo['options']:
                __ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
            if "local_untrusted_allow" in __hostinfo['options']:
                __ctx.check_hostname = False
                __ctx.verify_mode = ssl.CERT_OPTIONAL

        # If there are any global options that need to be set.
        if self.contextVariables is not None:
            # If securityLevel is set
            if self.contextVariables["securityLevel"] == 1:
                # Lower the default security level
                __ctx.set_ciphers('DEFAULT@SECLEVEL=1')

        # Initialize the __hostnameData object.
        __hostnameData = {
            "certificateMetaData": None,
            "connectionCipher": None,
        }

        try:
            # Create a new socket.
            with socket.socket() as sock:
                # Set timeout value for socket to 10 seconds.
                sock.settimeout(10.0)
                with __ctx.wrap_socket(
                    sock,
                    server_hostname=__hostinfo['hostname']
                ) as s:
                    s.connect((__hostinfo['hostname'], __hostinfo['port']))
                    __certificate = s.getpeercert()
                    __cipher = s.cipher()
                    __hostnameData["certificateMetaData"] = __certificate
                    __hostnameData["connectionCipher"] = __cipher

        except ssl.SSLCertVerificationError as e:
            connectHost = (
                f"{__hostinfo['hostname']}:{__hostinfo['port']}, "
                f"options: {__hostinfo['options']}"
            )
            print(connectHost + ' - Certificate error - ', e.verify_message)

        except socket.gaierror as e:
            connectHost = (
                f"{__hostinfo['hostname']}:{__hostinfo['port']}, "
                f"options: {__hostinfo['options']}"
            )
            print(connectHost + ' - Socket error - ', e.strerror)

        except FileNotFoundError as e:
            connectHost = (
                f"{__hostinfo['hostname']}:{__hostinfo['port']}, "
                f"options: {__hostinfo['options']}"
            )
            print(connectHost + ' - File not found - ', e.strerror)

        except TimeoutError as e:
            connectHost = (
                f"{__hostinfo['hostname']}:{__hostinfo['port']}, "
                f"options: {__hostinfo['options']}"
            )
            print(connectHost + ' - Timeout error - ', e.strerror)

        except OSError as e:
            connectHost = (
                f"{__hostinfo['hostname']}:{__hostinfo['port']}, "
                f"options: {__hostinfo['options']}"
            )
            print(connectHost + ' - OSError - ', e.strerror)

        return __hostnameData

    @staticmethod
    def returnNotAfter(__certificateObject) -> None:
        """Return the notAfter field from the certificate."""
        if __certificateObject is not None:
            return __certificateObject['notAfter']
        return ""

    def howMuchTimeLeft(self, __certificateObject) -> None:
        """Return the remaining time left on the certificate."""
        if __certificateObject is not None:
            timeNow = datetime.datetime.utcnow().replace(microsecond=0)
            certNotAfter = datetime.datetime.strptime(
                self.returnNotAfter(
                    __certificateObject["certificateMetaData"]
                ),
                self.certTimeFormat
            )

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
                    timeLeft.append(f"{myDeltaDate[field]} {field}")
                else:
                    if myDeltaDate[field] == 1:
                        timeLeft.append(f"{myDeltaDate[field]} {field[:-1]}")

            certResult = ', '.join(timeLeft)
        else:
            certResult = "Invalid certificate"
        return certResult

    def calculateCertificateUtilization(self, __notBefore: datetime, __notAfter: datetime) -> float:
        """Calculating the percentage utilization of the certificate"""
        # Convert __notBefore to datetime object
        notBeforeTime = datetime.datetime.strptime(
            __notBefore,
            self.certTimeFormat
        )

        # Convert __notAfter to datetime object
        notAfterTime = datetime.datetime.strptime(
            __notAfter,
            self.certTimeFormat
        )

        # Get the current time.
        currentTime = datetime.datetime.utcnow()

        # Calculate the differences between
        # currentTime, notAfterTime, and notBeforeTime
        rest = notAfterTime - currentTime
        total = notAfterTime - notBeforeTime

        # Calculate the percentage utilization of the time
        # available before expiry.
        percentageUtilization = 100 - (rest / total * 100)

        # Return the percentage utilization as a string formatted to 2 places.
        return float(f"{percentageUtilization:.2f}")

    def calculateCertificateTemplateTime(self, __notBefore: datetime, __notAfter: datetime) -> int:
        """
        Calculate the number of seconds between
        __notBefore and __notAfter.
        """
        # Convert __notBefore to datetime object
        notBeforeTime = datetime.datetime.strptime(
            __notBefore,
            self.certTimeFormat
        )

        # Convert __notAfter to datetime object
        notAfterTime = datetime.datetime.strptime(
            __notAfter,
            self.certTimeFormat
        )

        # Calcualte the difference
        timeDifference = notAfterTime - notBeforeTime

        # Get the number of seconds from the calculation above
        timeDifferenceInSeconds = int(timeDifference.total_seconds())

        return timeDifferenceInSeconds

    def convertCertificateObject2Json(
            self,
            __hostname: str,
            __port: int,
            __startTime: datetime,
            __endTime: datetime,
            __certificateObject: dict
            ) -> dict:
        """Convert the certificate object into JSON format."""
        myJsonCertificateInfo = {}

        startTime = __startTime.isoformat()
        endTime = __endTime.isoformat()

        # Calculate queryTime between __endTime and __startTime in milliseconds
        queryTime = round(
            float(
                (
                    __endTime - __startTime
                ).total_seconds() * 1000
            ), 2
        )

        myJsonCertificateInfo["hostname"] = __hostname
        myJsonCertificateInfo["port"] = int(__port)
        myJsonCertificateInfo["startTime"] = startTime
        myJsonCertificateInfo["endTime"] = endTime
        myJsonCertificateInfo["queryTime"] = queryTime

        if __certificateObject["connectionCipher"] is not None:
            myJsonCertificateInfo["connectionCipher"] = \
                __certificateObject["connectionCipher"]

        myJsonCertificateInfo["certificateInfo"] = {}

        if __certificateObject["certificateMetaData"] is not None:

            certKeys = __certificateObject.keys()

            # Certificate might not have subject defined.
            if 'subject' in certKeys:
                myJsonCertificateInfo["certificateInfo"]["subject"] = dict(
                    x[0] for x in __certificateObject["certificateMetaData"]["subject"]
                )

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

            # Get the notBefore and notAfter dates.
            certBeforeDate = __certificateObject["certificateMetaData"]["notBefore"]
            certAfterDate = __certificateObject["certificateMetaData"]["notAfter"]

            # Percentage Utilization of certificate
            myJsonCertificateInfo["percentageUtilization"] = self.calculateCertificateUtilization(certBeforeDate, certAfterDate)

            # Certificate template time validity
            # Work out the time that certificates are issued for
            myJsonCertificateInfo["certificateTemplateTime"] = self.calculateCertificateTemplateTime(certBeforeDate, certAfterDate)

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

    def uploadJsonData(self, __certificateJsonData: dict, __httpUrl: str) -> str:
        """
        This will upload the json data to a URL via a POST method.
        If the verbose argument is set, it'll display what URL it's being
        submitted to as well as the json data (jsonData).
        When the response is returned, it'll return the X-Headers that are sent back
        from the server.
        """
        x = requests.post(__httpUrl, json=__certificateJsonData)
        return x.headers

    def __init__(self, __contextVariables=0):
        """Initialize the class."""
        self.initialized = True
        self.moduleVersion = "0.18"
        self.certificate = {}
        if __contextVariables == 1:
            self.contextVariables = self.getContextVariables()
        else:
            self.contextVariables = None

        # Certificate date/time format that is to be interpreted by datetime module.
        self.certTimeFormat = "%b %d %H:%M:%S %Y %Z"
