import json
from . import CertificateStatistics

class DisplayCertificate:
    """This class is responsible for displaying the certificate Meta Data."""
    CLASS_VERSION = "0.01"

    # Define a certificate_stats object for use when calculating statistics about the certificate.
    certificate_stats = CertificateStatistics.CertificateStatistics()

    @staticmethod
    def printSubject(__certificateObject: dict) -> None:
        """Print the subject name of the certificate."""
        if __certificateObject is not None:
            subject = dict(x[0] for x in __certificateObject['subject'])
            issued_to = subject['commonName']
            print("Subject: ", issued_to, end='')

    @staticmethod
    def printSubjectAltName(__certificateObject) -> None:
        """Print the Subject Alternate Name(s) of the certificate."""
        __subjectAltName = []

        for field, value in __certificateObject['subjectAltName']:
            __subjectAltName.append({field: value})

        print("Subject Alt Name: ", __subjectAltName)

    @staticmethod
    def printIssuer(__certificateObject) -> None:
        """Print the Issuer of the certificate."""
        if __certificateObject is not None:
            issuer = dict(x[0] for x in __certificateObject['issuer'])
            issued_by = issuer['commonName']
            print("Issued by: ", issued_by)

    @staticmethod
    def printNotBefore(__certificateObject) -> None:
        """Print the notBefore field of the certificate."""
        if __certificateObject is not None:
            notBefore = __certificateObject['notBefore']
            print("Certificate start date: ", notBefore)

    @staticmethod
    def printNotAfter(__certificateObject) -> None:
        """Print the notAfter field of the certificate."""
        if __certificateObject is not None:
            notAfter = __certificateObject['notAfter']
            print("Certificate end date: ", notAfter)

    @staticmethod
    def printOCSP(__certificateObject) -> None:
        """Print the OCSP field of the certificate."""
        if __certificateObject is not None:
            __OCSPList = []
            for value in __certificateObject['OCSP']:
                __OCSPList.append(value)
            print("OCSP: ", __OCSPList)

    @staticmethod
    def printCRLDistributionPoints(__certificateObject) -> None:
        """Print the CRL distribution points of the certificate."""
        if __certificateObject is not None:
            __CRLList = []
            if 'crlDistributionPoints' in __certificateObject and __certificateObject["crlDistributionPoints"] is not None:
                for value in __certificateObject['crlDistributionPoints']:
                    __CRLList.append(value)
                print("CRL: ", __CRLList)

    @staticmethod
    def printCertificateSerialNumber(__certificateObject) -> None:
        """Print the certificate serial number."""
        if __certificateObject is not None:
            certificateSerialNumber = __certificateObject['serialNumber']
            print("Serial Number: ", certificateSerialNumber)

    @staticmethod
    def printCaIssuers(__certificateObject) -> None:
        """Print the certificates CA issuers."""
        if __certificateObject is not None:
            certificateCaIssuers = __certificateObject['caIssuers']
            print("CA Issuers: ", certificateCaIssuers)

    def printHowMuchTimeLeft(self, __certificateObject) -> None:
        """Print how much time is left on the certificate."""
        if __certificateObject is not None:
            timeLeft = DisplayCertificate.certificate_stats.howMuchTimeLeft(__certificateObject)
            print("Time left: ", timeLeft)

    def printCertInfo(self, __certificateObject) -> None:
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

    @staticmethod
    def printCertInfoJSON(__certificateObject) -> None:
        """Print the certificate information in JSON format."""
        if __certificateObject is not None:
            jsonCertInfoFormat = json.dumps(__certificateObject)
            print(jsonCertInfoFormat)
        else:
            jsonCertInfoFormat = {
                "subject": {"None": "None"},
                "certificateIssuer": {"None": "None"},
                "version": 0,
                "serialNumber": "0",
                "notBefore": "Jan 1 00:00:00 0000 GMT",
                "notAfter": "Jan 1 00:00:00 0000 GMT",
                "timeLeft": "0 seconds",
                "OCSP": "None",
                "crlDistributionPoints": "None",
                "caIssuers": "None",
                "subjectAltName": {"None": "None"}
            }
            print(jsonCertInfoFormat)

