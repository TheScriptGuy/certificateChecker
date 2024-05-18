# Certificate Module
# Version:                 0.27
# Last updated:            2024-05-18
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
from . import CertificateDecoder
from . import FileOperations
from . import CertificateStatistics
from . import CertificateTimeFormat


class certificateModule:
    """certificateModule class"""

    # Define a certificate_time_format object to be used in certificate calculations.
    certificate_time_format = CertificateTimeFormat.CertificateTimeFormat().cert_time_format

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
        hostnamePortPair = f'{__hostinfo["hostname"]}:{__hostinfo["port"]}'
        certificateHashFilename = hashlib.sha256(
            hostnamePortPair.encode()
        ).hexdigest() + ".pem"

        # Determine which context to create
        if __hostinfo['options'] is not None and \
                "local_untrusted_allow" in __hostinfo['options']:
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

        """
        Check to see if save_certificate is true.
        If it is, save the certificate to the file.
        """
        if not self.save_certificate:
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
                if self.contextVariables.get("insecure") != 1:
                    # If security_level is set
                    if self.contextVariables.get("security_level") == 1:
                        # Lower the default security level
                        __ctx.set_ciphers('DEFAULT@SECLEVEL=1')

                    # Check to see if local_untrusted_certificates should be allowed
                    if self.contextVariables.get("local_untrusted_allow") == 1:
                        __ctx.check_hostname = False
                        __ctx.verify_mode = ssl.CERT_OPTIONAL

                    # Check to see if unsafe_legacy is defined
                    if self.contextVariables.get("unsafe_legacy") == 1:
                        __ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT

                else:
                    __ctx.check_hostname = False
                    __ctx.verify_mode = ssl.CERT_OPTIONAL
        else:
            __ctx.check_hostname = False
            __ctx.verify_mode = ssl.CERT_NONE

        # Initialize the __hostnameData object.
        __hostnameData = {
            "certificateMetaData": None,
            "connectionCipher": None,
        }

        # Lets get a timestamp for this attempt
        timeNow = datetime.datetime.utcnow().replace(microsecond=0)

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
                    if self.contextVariables != {} and self.contextVariables.get("insecure") != 1:
                        __certificate = s.getpeercert()
                    else:
                        __binary_certificate = s.getpeercert(binary_form=True)
                        if self.save_certificate:
                            output_file = f"{self.output_directory}/{certificateHashFilename}"
                            file_write_time = datetime.datetime.utcnow().replace(microsecond=0)
                            print(f"{file_write_time} - Certificate for host {__hostinfo['hostname']}:{__hostinfo['port']} saved to {output_file}", end='')
                            file_writer = FileOperations.FileOperations(output_file)
                            file_writer.write_binary(__binary_certificate)
                            print("...Done")
                        _certdecoder = CertificateDecoder.CertificateDecoder()
                        __certificate = _certdecoder.decode(__binary_certificate)

                    __cipher = s.cipher()
                    __hostnameData["certificateMetaData"] = __certificate
                    __hostnameData["connectionCipher"] = __cipher

        except ssl.SSLCertVerificationError as e:
            connectHost = (
                f"{__hostinfo['hostname']}:{__hostinfo['port']}, "
                f"options: {__hostinfo['options']}"
            )
            print(f'{timeNow} - {connectHost} - Certificate error - {e.verify_message}')

        except socket.gaierror as e:
            connectHost = (
                f"{__hostinfo['hostname']}:{__hostinfo['port']}, "
                f"options: {__hostinfo['options']}"
            )
            print(f'{timeNow} - {connectHost} - Socket error - {e.strerror}')

        except FileNotFoundError as e:
            connectHost = (
                f"{__hostinfo['hostname']}:{__hostinfo['port']}, "
                f"options: {__hostinfo['options']}"
            )
            print(f'{timeNow} - {connectHost} - File not found - {e.strerror}')

        except TimeoutError as e:
            connectHost = (
                f"{__hostinfo['hostname']}:{__hostinfo['port']}, "
                f"options: {__hostinfo['options']}"
            )
            print(f'{timeNow} - {connectHost} - Timeout error - {e.strerror}')

        except OSError as e:
            connectHost = (
                f"{__hostinfo['hostname']}:{__hostinfo['port']}, "
                f"options: {__hostinfo['options']}"
            )
            print(f'{timeNow} - {connectHost} - OSError - {e.strerror}')

        return __hostnameData

    @staticmethod
    def returnNotBefore(__certificateObject) -> None:
        """Return the notBefore field from the certificate."""
        if __certificateObject is not None:
            return __certificateObject['notBefore']
        return ""

    @staticmethod
    def checkIssuer(__certificateObject) -> bool:
        """Check to see if issuers are trusted."""
        return True

    @staticmethod
    def checkRevocation(__certificateObject) -> bool:
        """Check to see if certificate hasn't been revoked."""
        return True

    def checkTimeValidity(self, __certificateObject) -> bool:
        """
        Check to see if the certificate is valid:
            current date is after certificate start date
            current date is before certificate expiry date
        """
        if __certificateObject is not None:
            timeNow = datetime.datetime.utcnow().replace(microsecond=0).date()
            certNotAfter = datetime.datetime.strptime(
                self.returnNotAfter(__certificateObject),
                certificateModule.certificate_time_format
            ).date()

            certNotBefore = datetime.datetime.strptime(
                self.returnNotBefore(__certificateObject),
                certificateModule.certificate_time_format
            ).date()

            # Assume time not valid
            isValid = bool(certNotBefore < timeNow < certNotAfter)

            return isValid
        return False

    def calculateCertificateUtilization(self, __notBefore: datetime, __notAfter: datetime) -> float:
        """Calculating the percentage utilization of the certificate"""
        # Convert __notBefore to datetime object
        notBeforeTime = datetime.datetime.strptime(
            __notBefore,
            certificateModule.certificate_time_format
        )

        # Convert __notAfter to datetime object
        notAfterTime = datetime.datetime.strptime(
            __notAfter,
            certificateModule.certificate_time_format
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
            certificateModule.certificate_time_format
        )

        # Convert __notAfter to datetime object
        notAfterTime = datetime.datetime.strptime(
            __notAfter,
            certificateModule.certificate_time_format
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

            if __certificateObject["certificateMetaData"]["subjectAltName"]:
                for field, value in __certificateObject["certificateMetaData"]["subjectAltName"]:
                    myJsonCertificateInfo["certificateInfo"]["subjectAltName"].update({field + str(subjectAltNameCounter): value})
                    subjectAltNameCounter += 1

            # Time left on certificate
            certificate_stats = CertificateStatistics.CertificateStatistics()
            myJsonCertificateInfo["timeLeft"] = certificate_stats.howMuchTimeLeft(__certificateObject["certificateMetaData"])

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

    def __init__(self, **kwargs):
        """Initialize the class."""
        self.initialized = True
        self.moduleVersion = "0.27"
        self.certificate = {}

        self.save_certificate = kwargs['save_certificate']
        self.output_directory = kwargs['output_directory']

        if 'contextVariables' in kwargs and kwargs['contextVariables'] == 1:
            self.contextVariables = self.getContextVariables()
        else:
            self.contextVariables = {}

