# Certificate Module

import ssl, socket
import argparse
import datetime
import json
import requests

from dateutil.relativedelta import relativedelta

class certificateModule:

    def getCertificate(self,__hostname):
        __ctx = ssl.create_default_context()
        try:
            with __ctx.wrap_socket(socket.socket(), server_hostname=__hostname) as s:
                s.connect((__hostname, 443))
                cert = s.getpeercert()
                return cert
        
        except ssl.SSLCertVerificationError as e:
            print('Certificate error - ',e.verify_message)
            return None
        
        except socket.gaierror as e:
            print('Socket error - ',e.strerror)
            return None

        except OSError as e:
            print('OSError - ', e.strerror)
            return None

        except TimeoutError as e:
            print('Timeout error - ', e.strerror)
            return None

    def printSubject(self,__certificateObject):
        if __certificateObject != None:
            subject = dict(x[0] for x in __certificateObject['subject'])
            issued_to = subject['commonName']
            print("Subject: ",issued_to)

    def printSubjectAltName(self,__certificateObject):
        __subjectAltName = []

        for field,value in __certificateObject['subjectAltName']:
            __subjectAltName.append({field:value})
    
        print("Subject Alt Name: ", __subjectAltName)

    def printIssuer(self,__certificateObject):
        if __certificateObject != None:
            issuer = dict(x[0] for x in __certificateObject['issuer'])
            issued_by = issuer['commonName']
            print("Issued by: ", issued_by)

    def printNotBefore(self,__certificateObject):
        if __certificateObject != None:
            notBefore = __certificateObject['notBefore']
            print("Certificate start date: ", notBefore)

    def printNotAfter(self,__certificateObject):
        if __certificateObject != None:
            notAfter = __certificateObject['notAfter']
            print("Certificate end date: ", notAfter)


    def returnNotBefore(self,__certificateObject):
        if __certificateObject != None:
            return __certificateObject['notBefore']

    def returnNotAfter(self,__certificateObject):
        if __certificateObject != None:
            return __certificateObject['notAfter']

    def howMuchTimeLeft(self,__certificateObject):
        if __certificateObject != None:
            timeNow = datetime.datetime.now().replace(microsecond=0)
            certNotAfter = datetime.datetime.strptime(self.returnNotAfter(__certificateObject), '%b %d %H:%M:%S %Y %Z')
    
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

    def checkIssuer(self,__certificateObject):
        return True

    def checkRevocation(self,__certificateObject):
        return True

    def checkTimeValidity(self,__certificateObject):
        if __certificateObject != None:
            timeNow = datetime.datetime.now().replace(microsecond=0).date()
            certNotAfter = datetime.datetime.strptime(self.returnNotAfter(__certificateObject), '%b %d %H:%M:%S %Y %Z').date()
            certNotBefore = datetime.datetime.strptime(self.returnNotBefore(__certificateObject), '%b %d %H:%M:%S %Y %Z').date()

    
            # Assume time not valid
            isValid = False

            if (certNotBefore < timeNow) and (certNotAfter > timeNow):
                isValid = True
            else:
                isValid = False

            return isValid

    def printOCSP(self,__certificateObject):
        if __certificateObject != None:
            __OCSPList = []
            for value in __certificateObject['OCSP']:
                __OCSPList.append(value)
            print("OCSP: ", __OCSPList)

    def printCRLDistributionPoints(self,__certificateObject):
        if __certificateObject != None:
            __CRLList = []
            if 'crlDistributionPoints' in __certificateObject:
                for value in __certificateObject['crlDistributionPoints']:
                    __CRLList.append(value)
                print("CRL: ", __CRLList)

    def printCertificateSerialNumber(self,__certificateObject):
        if __certificateObject != None:
            certificateSerialNumber = __certificateObject['serialNumber']
            print("Serial Number: ", certificateSerialNumber)

    def printCaIssuers(self,__certificateObject):
        if __certificateObject != None:
            certificateCaIssuers = __certificateObject['caIssuers']
            print("CA Issuers: ", certificateCaIssuers)

    def printHowMuchTimeLeft(self,__certificateObject):
        if __certificateObject != None:
            timeLeft = self.howMuchTimeLeft(__certificateObject)
            print("Time left: ", timeLeft)

    def certificateValid(self,__certificateObject):
        if __certificateObject != None:
            if self.checkTimeValidity(__certificateObject) and self.checkRevocation(__certificateObject) and self.checkIssuer(__certificateObject):
                print("Certificate good!")
            else:
                print("Certificate invalid!")

    def printCertInfo(self,__certificateObject):
        self.printSubject(__certificateObject)
        self.printIssuer(__certificateObject)
        self.printSubjectAltName(__certificateObject)
        self.printNotBefore(__certificateObject)
        self.printNotAfter(__certificateObject)
        self.printOCSP(__certificateObject)
        self.printCRLDistributionPoints(__certificateObject)
        self.printCaIssuers(__certificateObject)
        self.printCertificateSerialNumber(__certificateObject)
        self.printHowMuchTimeLeft(__certificateObject)

    def printCertInfoJSON(self,__certificateObject):
        if __certificateObject != None:
            jsonCertInfoFormat = json.dumps(__certificateObject)
            print(jsonCertInfoFormat)

    def convertCertificateObject2Json(self,__hostname,__startTime,__endTime,__certificateObject):
        if __certificateObject != None:
            myJsonCertificateInfo = {}
            certKeys = __certificateObject.keys()
        
            startTime = __startTime.strftime("%Y/%m/%d %H:%M:%S.%f")
            endTime = __endTime.strftime("%Y/%m/%d %H:%M:%S.%f")
            queryTime = str((__endTime - __startTime).total_seconds())

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

            myJsonCertificateInfo["certificateInfo"]["timeLeft"] = self.howMuchTimeLeft(__certificateObject)

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

    def uploadJsonData(self,__certificateJsonData,__httpUrl):
        """
        This will upload the json data to a URL via a POST method.
        If the verbose argument is set, it'll display what URL it's being
        submitted to as well as the json data (jsonData).
        When the response is returned, it'll return the X-Headers that are sent back
        from the server.
        """
        x = requests.post(__httpUrl, json = __certificateJsonData)
        return x.headers


   

    def __init__(self):
        self.initialized = True
        self.certificate = {}


