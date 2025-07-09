# Description:     Get the certificate chain from a website.
# Author:          TheScriptGuy
# Last modified:   2025-07-09
# Version:         0.08

import ssl
import socket
import requests
import sys
import re
import hashlib

from cryptography import x509
from cryptography.x509.oid import ExtensionOID
from cryptography.hazmat.primitives import serialization

from asn1crypto import cms, pem

from typing import Optional


class getCertificateChain:
    """
    Attempt to fetch full certificate chains from poorly configured websites.
    """

    @staticmethod
    def loadRootCACertChain(__filename: str) -> dict:
        caRootStore = {}
        try:
            with open(__filename, "r") as f_caCert:
                lines = f_caCert.readlines()

            i = 0
            while i < len(lines):
                if re.match(r"^={5,}", lines[i]):
                    rootCAName = lines[i - 1].strip()
                    cert_lines = []
                    i += 1
                    while i < len(lines) and "END CERTIFICATE" not in lines[i]:
                        cert_lines.append(lines[i])
                        i += 1
                    cert_lines.append("-----END CERTIFICATE-----\n")
                    caRootStore[rootCAName] = ''.join(cert_lines)
                i += 1

            print(f"Number of Root CAs loaded: {len(caRootStore)}")
            return caRootStore

        except FileNotFoundError:
            print("Could not find cacert.pem file.")
            sys.exit(1)

    @staticmethod
    def getCertificate(__hostname: str, __port: int) -> x509.Certificate:
        try:
            ctx = ssl._create_unverified_context()
            ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
            with socket.create_connection((__hostname, __port)) as sock, ctx.wrap_socket(sock, server_hostname=__hostname) as sslSock:
                cert_bytes = sslSock.getpeercert(True)
                return x509.load_der_x509_certificate(cert_bytes)
        except Exception as e:
            print(f"Failed to retrieve certificate from {__hostname}:{__port} - {e}")
            sys.exit(1)

    def getCertificateFromUri(self, __uri: str) -> list[x509.Certificate]:
        try:
            response = requests.get(__uri, timeout=10)
            response.raise_for_status()
            content = response.content

            # If PEM-wrapped, unwrap it
            if pem.detect(content):
                _, _, content = pem.unarmor(content)

            try:
                pkcs7 = cms.ContentInfo.load(content)
                if pkcs7['content_type'].native == 'signed_data':
                    certs = []
                    for cert in pkcs7['content']['certificates']:
                        if cert.name == 'certificate':
                            cert_der = cert.chosen.dump()
                            cert_obj = x509.load_der_x509_certificate(cert_der)
                            certs.append(cert_obj)
                    return certs
            except Exception:
                # Not a PKCS#7, try DER fallback
                try:
                    cert_obj = x509.load_der_x509_certificate(content)
                    return [cert_obj]
                except Exception as inner:
                    print(f"Could not parse certificate from {__uri}: {inner}")
                    return []

        except requests.RequestException as e:
            print(f"Error downloading from {__uri}: {e}")
            return []

    @staticmethod
    def returnCertAKI(cert: x509.Certificate) -> Optional[bytes]:
        try:
            aki_ext = cert.extensions.get_extension_for_oid(ExtensionOID.AUTHORITY_KEY_IDENTIFIER)
            return aki_ext.value.key_identifier
        except x509.ExtensionNotFound:
            return None

    @staticmethod
    def returnCertSKI(cert: x509.Certificate) -> Optional[bytes]:
        try:
            ski_ext = cert.extensions.get_extension_for_oid(ExtensionOID.SUBJECT_KEY_IDENTIFIER)
            return ski_ext.value.digest
        except x509.ExtensionNotFound:
            return None

    @staticmethod
    def returnCertAIAList(cert: x509.Certificate) -> list[str]:
        aia_list = []
        try:
            aia_ext = cert.extensions.get_extension_for_oid(ExtensionOID.AUTHORITY_INFORMATION_ACCESS)
            for entry in aia_ext.value:
                if entry.access_method._name == "caIssuers":
                    aia_list.append(entry.access_location.value)
        except x509.ExtensionNotFound:
            pass
        return aia_list

    def walkTheChain(self, cert: x509.Certificate, depth: int):
        if depth > self.maxDepth:
            return

        cert_aki = self.returnCertAKI(cert)
        if cert_aki is None:
            print("No AKI present. Stopping chain walk.")
            return

        aia_uris = self.returnCertAIAList(cert)
        if not aia_uris:
            print("No AIA URIs. Attempting to match against known Root CAs.")

            caRootStore = self.loadRootCACertChain("cacert.pem")
            for rootName, rootPem in caRootStore.items():
                try:
                    root_cert = x509.load_pem_x509_certificate(rootPem.encode('ascii'))
                    root_ski = self.returnCertSKI(root_cert)
                    if root_ski == cert_aki:
                        print(f"Root CA Found - {rootName}")
                        self.certChain.append(root_cert)
                        return
                except Exception:
                    continue
            print("ERROR - Root CA NOT found.")
            sys.exit(1)

        for uri in aia_uris:
            nextCerts = self.getCertificateFromUri(uri)
            if not nextCerts:
                continue

            for nextCert in nextCerts:
                self.certChain.append(nextCert)
                self.walkTheChain(nextCert, depth + 1)
                break  # Walk only the first found cert per URI

    @staticmethod
    def sendCertificateToFile(filename: str, cert: x509.Certificate) -> None:
        with open(filename, "ab") as f:
            f.write(cert.public_bytes(serialization.Encoding.PEM) + b'\n')

    def writeChainToFile(self, certs: list[x509.Certificate]) -> None:
        filename = f'{self.certificateHash}.pem'
        for cert in certs[1:]:  # Skip leaf
            self.sendCertificateToFile(filename, cert)

    def getCertificateChain(self, hostname: str, port: int):
        self.certificateHash = hashlib.sha256(f"{hostname}:{port}".encode()).hexdigest()
        leaf_cert = self.getCertificate(hostname, port)

        if leaf_cert:
            self.certChain.append(leaf_cert)
            self.walkTheChain(leaf_cert, 1)
            self.writeChainToFile(self.certChain)
        else:
            print("ERROR - Leaf certificate could not be retrieved.")
            sys.exit(1)

    def __init__(self):
        self.classVersion = "0.08"
        self.maxDepth = 4
        self.certChain = []
        self.certificateHash = ""
