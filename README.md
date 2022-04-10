# Certificate Checker

Version: 0.07

Author: TheScriptGuy

With the growing usage of certificates within an organization, it's really easy to lose track of when a certificate will expire.
 
This python script will get the certificate from a supplied hostname (defaults to google.com if nothing specified) and return the properties of the script in JSON format.

## Usage
Displays the certificate metadata in JSON format
```bash
python3 certChecker.py --hostname example.com --displayCertificateJSON
```

Displays the certificate metadata and device performing the query metadata.
```bash
python3 certChecker.py --hostname example.com --displayScriptDataJSON
```

Only display time left when querying a certificate
```bash
python3 certChecker.py --hostname example.com
```

## Help output
```bash
python3 certChecker.py -h

usage: certCheck.py [-h] [--hostname HOSTNAME] [--displayCertificate]
                    [--displayCertificateJSON] [--displayScriptDataJSON]
                    [--displayTimeLeft] [--setTag SETTAG] [--deleteTag]
                    [--getTag] [--renewUuid] [--getUuid] [--deleteUuid]

Certificate Checker V0.07

optional arguments:
  -h, --help            show this help message and exit
  --hostname HOSTNAME   Hostname to get certificate from. Defaults to
                        google.com
  --displayCertificate  Display certificate info
  --displayCertificateJSON
                        Display certificate info in JSON format
  --displayScriptDataJSON
                        Display script info and queried certificates in JSON
                        format
  --displayTimeLeft     Display time left until expiry on certificate.
  --setTag SETTAG       Set the tag for the query results. Creates tag.cfg
                        file with tag.
  --deleteTag           Delete the tag file - tag.cfg
  --getTag              Get the tag from tag.cfg file
  --renewUuid           Renew the UUID value.
  --getUuid             Get the UUID value from uuid.cfg file.
  --deleteUuid          Remove the UUID value. Caution: when script runs again
                        a new UUID will be generated.
  --uploadJsonData UPLOADJSONDATA
                        Upload JSON data to HTTP URL via HTTP POST method.
```

## Example of JSON structure for certificate specifically
```json
{
    "hostname": "apple.com",
    "startTime": "2022/04/10 11:51:38.435369",
    "endTime": "2022/04/10 11:51:38.493124",
    "queryTime": "0.057755",
    "certificateInfo":
    {
        "subject":
        {
            "businessCategory": "Private Organization",
            "jurisdictionCountryName": "US",
            "jurisdictionStateOrProvinceName": "California",
            "serialNumber": "C0806592",
            "countryName": "US",
            "stateOrProvinceName": "California",
            "localityName": "Cupertino",
            "organizationName": "Apple Inc.",
            "organizationalUnitName": "management:idms.group.665035",
            "commonName": "apple.com"
        },
        "certificateIssuer":
        {
            "countryName": "US",
            "organizationName": "Apple Inc.",
            "commonName": "Apple Public EV Server ECC CA 1 - G1"
        },
        "version": 3,
        "serialNumber": "5E9661C3DD43CAB7D09D24C429A7C708",
        "notBefore": "Jun 22 11:26:36 2021 GMT",
        "notAfter": "Jul 22 11:26:35 2022 GMT",
        "timeLeft": "3 months, 11 days, 23 hours, 34 minutes, 57 seconds",
        "OCSP":
        [
            "http://ocsp.apple.com/ocsp03-apevsecc1g101"
        ],
        "crlDistributionPoints":
        [
            "http://crl.apple.com/apevsecc1g1.crl"
        ],
        "caIssuers":
        [
            "http://certs.apple.com/apevsecc1g1.der"
        ],
        "subjectAltName":
        {
            "DNS0": "apple.com"
        }
    }
}
```

An example of the JSON structure which includes the hostname information as well:
```json
{
    "deviceUuid": "074e760e-08ce-4ef9-a61c-5a028ee6db3f",
    "deviceTag": "Production",
    "clientHostName": "PRODCERT01",
    "dataFormatVersion": 1,
    "certResults":
    {
        "hostname": "apple.com",
        "startTime": "2022/04/10 11:55:00.085726",
        "endTime": "2022/04/10 11:55:00.140277",
        "queryTime": "0.054551",
        "certificateInfo":
        {
            "subject":
            {
                "businessCategory": "Private Organization",
                "jurisdictionCountryName": "US",
                "jurisdictionStateOrProvinceName": "California",
                "serialNumber": "C0806592",
                "countryName": "US",
                "stateOrProvinceName": "California",
                "localityName": "Cupertino",
                "organizationName": "Apple Inc.",
                "organizationalUnitName": "management:idms.group.665035",
                "commonName": "apple.com"
            },
            "certificateIssuer":
            {
                "countryName": "US",
                "organizationName": "Apple Inc.",
                "commonName": "Apple Public EV Server ECC CA 1 - G1"
            },
            "version": 3,
            "serialNumber": "5E9661C3DD43CAB7D09D24C429A7C708",
            "notBefore": "Jun 22 11:26:36 2021 GMT",
            "notAfter": "Jul 22 11:26:35 2022 GMT",
            "timeLeft": "3 months, 11 days, 23 hours, 31 minutes, 35 seconds",
            "OCSP":
            [
                "http://ocsp.apple.com/ocsp03-apevsecc1g101"
            ],
            "crlDistributionPoints":
            [
                "http://crl.apple.com/apevsecc1g1.crl"
            ],
            "caIssuers":
            [
                "http://certs.apple.com/apevsecc1g1.der"
            ],
            "subjectAltName":
            {
                "DNS0": "apple.com"
            }
        }
    }
}
```

Features to add:
* convert script to object orientated programming (partially done)
* Supply own CA certificate repository
* send email notification that script is about to expire within <X> number of days.

