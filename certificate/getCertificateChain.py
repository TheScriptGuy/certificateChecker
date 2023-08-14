# Description:     Get the certificate chain from a website.
# Author:          TheScriptGuy
# Last modified:   2023-08-13
# Version:         0.05

import ssl
import socket
import requests
import sys
import re
import hashlib

from cryptography import x509
from cryptography.x509.oid import ExtensionOID
from cryptography.hazmat.primitives import hashes, serialization
from typing import Optional


class getCertificateChain:
    """
    In some rare occassions where a website is poorly configured.
    e.g. not presenting the full certificate chain, the python's ssl fails to connect.
    This class will attempt to collect the certificate chain and store it to file for
    later use.
    """

    @staticmethod
    def loadRootCACertChain(
                            __filename: str
                            ) -> dict:
        """
        Load the Root CA Chain in a structured format.
        caRootStore = {
            "Root CA Name 1": "<PEM format1>",
            "Root CA Name 2": "<PEM format2>",
            ...
        }
        """
        previousLine = ""
        currentLine = ""

        caRootStore = {}
        try:
            with open(__filename, "r") as f_caCert:
                while True:
                    previousLine = currentLine
                    currentLine = f_caCert.readline()

                    if not currentLine:
                        break

                    if re.search("^\={5,}", currentLine):
                        # This is where the Root CA certificate file begins.
                        # Iterate through all the lines between
                        # -----BEGIN CERTIFICATE-----
                        # ...
                        # -----END CERTIFICATE-----
                        rootCACert = ""
                        rootCAName = previousLine.strip()

                        while True:
                            caCertLine = f_caCert.readline()
                            if caCertLine.strip() != "-----END CERTIFICATE-----":
                                rootCACert += caCertLine
                            else:
                                rootCACert += "-----END CERTIFICATE-----\n"
                                break

                        caRootStore[rootCAName] = rootCACert

            print(f"Number of Root CA's loaded: {len(caRootStore)}")

            return caRootStore

        except FileNotFoundError:
            print("Could not find cacert.pem file.")
            sys.exit(1)

    @staticmethod
    def getCertificate(
                       __hostname: str,
                       __port: int
                        ) -> x509.Certificate:
        """Retrieves the certificate from the website."""
        try:
            # Create the SSL context.
            # We will ignore any certificate warnings for this process.
            sslContext = ssl._create_unverified_context()

            with socket.create_connection((__hostname, __port)) as sock, sslContext.wrap_socket(sock, server_hostname=__hostname) as sslSocket:
                # Get the certificate from the connection, convert it to PEM format.
                sslCertificate = ssl.DER_cert_to_PEM_cert(sslSocket.getpeercert(True))

            # Load the PEM formatted file.
            sslCertificate = x509.load_pem_x509_certificate(sslCertificate.encode('ascii'))

        except ConnectionRefusedError:
            print(f"Connection refused to {__hostname}:{__port}")
            sys.exit(1)

        # Return the sslCertificate object.
        return sslCertificate

    @staticmethod
    def getCertificateFromUri(
                              __uri: str
                              ) -> str:
        """Gets the certificate from a URI.
        By default, we're expecting to find nothing. Therefore certI = None.
        If we find something, we'll update certI accordingly.
        """
        certI = None

        # Attempt to get the aia from __uri
        aiaRequest = requests.get(__uri)

        # If response status code is 200
        if aiaRequest.status_code == 200:
            # Get the content and assign to aiaContent
            aiaContent = aiaRequest.content

            # Convert the certificate into PEM format.
            sslCertificate = ssl.DER_cert_to_PEM_cert(aiaContent)

            # Load the PEM formatted content using x509 module.
            certI = x509.load_pem_x509_certificate(sslCertificate.encode('ascii'))

        # Return certI back to the script.
        return certI

    @staticmethod
    def returnCertAKI(__sslCertificate: x509.Certificate) -> Optional[x509.extensions.Extension]:
        """Returns the AKI of the certificate."""
        try:
            certAKI = __sslCertificate.extensions.get_extension_for_oid(ExtensionOID.AUTHORITY_KEY_IDENTIFIER)
        except x509.extensions.ExtensionNotFound:
            certAKI = None
        return certAKI

    @staticmethod
    def returnCertSKI(__sslCertificate: x509.Certificate) -> x509.extensions.Extension:
        """Returns the SKI of the certificate."""
        certSKI = __sslCertificate.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_KEY_IDENTIFIER)

        return certSKI

    @staticmethod
    def returnCertAIA(__sslCertificate: x509.Certificate) -> Optional[x509.extensions.Extension]:
        """Returns the AIA of the certificate. If not defined, then return None."""
        try:
            certAIA = __sslCertificate.extensions.get_extension_for_oid(ExtensionOID.AUTHORITY_INFORMATION_ACCESS)

        except x509.extensions.ExtensionNotFound:
            certAIA = None

        return certAIA

    @staticmethod
    def returnCertAIAList(__sslCertificate: x509.Certificate) -> list:
        """Returns a list of AIA's defined in __sslCertificate."""
        aiaUriList = []

        # Iterate through all the extensions.
        for extension in __sslCertificate.extensions:
            certValue = extension.value

            # If the extension is x509.AuthorityInformationAccess) then lets get the caIssuers from the field.
            if isinstance(certValue, x509.AuthorityInformationAccess):
                dataAIA = list(certValue)
                for item in dataAIA:
                    if item.access_method._name == "caIssuers":
                        aiaUriList.append(item.access_location._value)

        # Return the aiaUriList back to the script.
        return aiaUriList

    def walkTheChain(self, __sslCertificate: x509.Certificate, __depth: int):
        """
        Walk the length of the chain, fetching information from AIA
        along the way until AKI == SKI (i.e. we've found the Root CA.

        This is to prevent recursive loops. Usually there are only 4 certificates.
        If the maxDepth is too small (why?) adjust it at the beginning of the script.
        """
        if __depth <= self.maxDepth:
            # Retrive the AKI from the certificate.
            certAKI = self.returnCertAKI(__sslCertificate)

            # Sometimes the AKI can be none. Lets handle this accordingly.
            if certAKI is not None:
                certAKIValue = certAKI._value.key_identifier
            else:
                certAKIValue = None

            # Sometimes the AKI can be none. Lets handle this accordingly.
            if certAKIValue is not None:
                aiaUriList = self.returnCertAIAList(__sslCertificate)
                if aiaUriList:
                    # Iterate through the aiaUriList list.
                    for item in aiaUriList:
                        # get the certificate for the item element.
                        nextCert = self.getCertificateFromUri(item)

                        # If the certificate is not none (great), append it to the certChain, increase the __depth and run the walkTheChain subroutine again.
                        if nextCert is not None:
                            self.certChain.append(nextCert)
                            __depth += 1
                            self.walkTheChain(nextCert, __depth)
                        else:
                            print("Could not retrieve certificate.")
                            sys.exit(1)
                else:
                    # Now we have to go on a hunt to find the root from a standard root store.
                    print("Certificate didn't have AIA...ruh roh.")

                    # Load the Root CA Cert Chain.
                    caRootStore = self.loadRootCACertChain("cacert.pem")

                    # Assume we cannot find a Root CA
                    rootCACN = None

                    # Iterate through the caRootStore object.
                    for rootCA in caRootStore:
                        try:
                            # Get the pem encoded value from the caRootStore[rootCA] object
                            rootCACertificatePEM = caRootStore[rootCA]

                            # Load the pem file into the x509 format.
                            rootCACertificate = x509.load_pem_x509_certificate(rootCACertificatePEM.encode('ascii'))

                            # Get the Subject Key Identifier (SKI) from the rootCACertificate object.
                            rootCASKI = self.returnCertSKI(rootCACertificate)
                            rootCASKI_Value = rootCASKI._value.digest

                            # Root CA is when SKI = AKI.
                            if rootCASKI_Value == certAKIValue:
                                rootCACN = rootCA
                                print(f"Root CA Found - {rootCACN}")
                                self.certChain.append(rootCACertificate)
                                break
                        except x509.extensions.ExtensionNotFound:
                            # Apparently some Root CA's don't have a SKI?
                            pass

                    if rootCACN is None:
                        print("ERROR - Root CA NOT found.")
                        sys.exit(1)

    @staticmethod
    def sendCertificateToFile(__filename: str, __sslCertificate) -> None:
        """Write the certificate in PEM format to file."""
        with open(__filename, "ab") as f_clientPublicKey:
            f_clientPublicKey.write(
                __sslCertificate.public_bytes(
                    encoding=serialization.Encoding.PEM,
                ) + b'\n'
            )

    def writeChainToFile(self, __certificateChain: dict) -> None:
        """Write all the elements in the chain to file."""
        myCertChain = __certificateChain

        myCertChain.pop(0)

        # Iterate through all the elements in the chain.
        for _, certificateItem in enumerate(myCertChain):
            # Generate the certificate file name
            sslCertificateFilename = f'{self.certificateHash}.pem'

            # Send the certificate object to the sslCertificateFileName filename
            self.sendCertificateToFile(sslCertificateFilename, certificateItem)

    def getCertificateChain(self, __hostname: str, __port: int):
        """Get Certificate Chain."""
        # Create the hash for the __hostname:__port pair
        hostnamePort = f"{__hostname}:{__port}"

        self.certificateHash = hashlib.sha256(hostnamePort.encode()).hexdigest()

        # Get the website certificate object from myHostname["hostname"]:myHostname["port"]
        __websiteCertificate = self.getCertificate(__hostname, __port)

        if __websiteCertificate is not None:
            # Get the AIA from the __websiteCertificate object
            aia = self.returnCertAIA(__websiteCertificate)
            if aia is not None:
                # Append the __websiteCertificate object to the certChain list.
                self.certChain.append(__websiteCertificate)

                # Now we walk the chain up until we get the Root CA.
                self.walkTheChain(__websiteCertificate, 1)

                # Write the certificate chain to individual files.
                self.writeChainToFile(self.certChain)
            else:
                print("ERROR - I could not find AIA. Possible decryption taking place upstream?")
                sys.exit(1)

    def __init__(self):
        """Init the getCertChain class."""
        self.classVersion = "0.05"
        self.maxDepth = 4
        self.certChain = []
        self.certificateHash = ""
