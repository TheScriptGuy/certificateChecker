from cryptography import x509
from cryptography.hazmat.backends import default_backend
from typing import Tuple, Optional, Union


class CertificateDecoder:
    CLASS_VERSION = "0.01"

    def decode(self, der_cert_bytes: bytes) -> dict:
        """This returns the same format as the output of getpeercert()"""

        cert = x509.load_der_x509_certificate(der_cert_bytes, default_backend())
        return {
            "subject": self._parse_name(cert.subject),
            "issuer": self._parse_name(cert.issuer),
            "version": cert.version.value,
            "serialNumber": format(cert.serial_number, 'X'),
            "notBefore": cert.not_valid_before_utc.strftime("%b %d %H:%M:%S %Y GMT"),
            "notAfter": cert.not_valid_after_utc.strftime("%b %d %H:%M:%S %Y GMT"),
            "subjectAltName": self._get_extension_value(cert, x509.SubjectAlternativeName),
            "OCSP": self._get_extension_value(cert, x509.AuthorityInformationAccess, method='OCSP'),
            "caIssuers": self._get_extension_value(cert, x509.AuthorityInformationAccess, method='caIssuers'),
            "crlDistributionPoints": self._get_extension_value(cert, x509.CRLDistributionPoints)
        }

    def _parse_name(self, name: x509.Name) -> Tuple[Tuple[Tuple[str, str], ...], ...]:
        """This will iterate over the values."""

        return tuple(
            tuple((attr.oid._name, attr.value) for attr in rdn)
            for rdn in name.rdns  # Use .rdns to iterate over RDNs in the Name
        )

    def _get_extension_value(self, cert: x509.Certificate, ext_type, method: Optional[str] = None) -> Union[Tuple[str, ...], None]:
        """This will iterate through the OCSP, caIssuers, subjectAlternativeNames and CRLDistributionsPoints."""

        try:
            ext = cert.extensions.get_extension_for_class(ext_type)
            if method == 'OCSP':
                return tuple(a.access_location.value for a in ext.value if a.access_method == x509.oid.AuthorityInformationAccessOID.OCSP)
            elif method == 'caIssuers':
                return tuple(a.access_location.value for a in ext.value if a.access_method == x509.oid.AuthorityInformationAccessOID.CA_ISSUERS)
            elif isinstance(ext.value, x509.SubjectAlternativeName):
                return tuple(("DNS", name.value) for name in ext.value)
            elif isinstance(ext.value, x509.CRLDistributionPoints):
                return tuple(dp.full_name[0].value for dp in ext.value if dp.full_name)  # Check if full_name is not empty
        except (x509.ExtensionNotFound, ValueError):
            return None

