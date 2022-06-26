## Example of JSON structure for certificate specifically
```json
{
    "hostname": "apple.com",
    "port": 443,
    "startTime": "2022/06/16 16:14:19.793797",
    "endTime": "2022/06/16 16:14:19.863822",
    "queryTime": "70.025",
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
        "serialNumber": "6A1D3FA84A43C329F1051060FF4698BA",
        "notBefore": "Apr 26 21:58:37 2022 GMT",
        "notAfter": "May 26 21:58:36 2023 GMT",
        "timeLeft": "11 months, 10 days, 5 hours, 44 minutes, 17 seconds",
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
        },
        "percentageUtilization": "12.85"
    }
}
```

An example of the JSON structure which includes the hostname information as well:
```bash
$ python3 certCheck.py --hostname apple.com --displayScriptDataJSON
```
The resulting output is:
```json
{
    "tenantId": "",
    "deviceId": "2a44a3c9-3051-405f-b7ae-9c070d76c57d",
    "deviceTag": "",
    "clientHostName": "PRODMON01",
    "dataFormatVersion": 8,
    "certResults":
    [
        {
            "hostname": "apple.com",
            "port": 443,
            "startTime": "2022/06/26 12:23:11.737101",
            "endTime": "2022/06/26 12:23:11.782779",
            "queryTime": "45.678",
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
                "serialNumber": "6A1D3FA84A43C329F1051060FF4698BA",
                "notBefore": "Apr 26 21:58:37 2022 GMT",
                "notAfter": "May 26 21:58:36 2023 GMT",
                "timeLeft": "11 months, 9 hours, 35 minutes, 25 seconds",
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
                },
                "percentageUtilization": "15.34"
            }
        }
    ]
}
```
An example of the JSON structure which includes the multiple hosts from a query file as well:
```bash
$ python3 certCheck.py --queryFile queryfile --displayScriptDataJSON
```
The resulting output is (take note of the invalid host data at the end of the certResults attribute):
```json
{
    "tenantId": "",
    "deviceId": "2a44a3c9-3051-405f-b7ae-9c070d76c57d",
    "deviceTag": "",
    "clientHostName": "PRODMON01",
    "dataFormatVersion": 8,
    "certResults":
    [
        {
            "hostname": "apple.com",
            "port": 443,
            "startTime": "2022/06/26 12:26:41.551958",
            "endTime": "2022/06/26 12:26:41.596061",
            "queryTime": "44.103",
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
                "serialNumber": "6A1D3FA84A43C329F1051060FF4698BA",
                "notBefore": "Apr 26 21:58:37 2022 GMT",
                "notAfter": "May 26 21:58:36 2023 GMT",
                "timeLeft": "11 months, 9 hours, 31 minutes, 55 seconds",
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
                },
                "percentageUtilization": "15.34"
            }
        },
        {
            "hostname": "news24.com",
            "port": 443,
            "startTime": "2022/06/26 12:26:41.597296",
            "endTime": "2022/06/26 12:26:41.676241",
            "queryTime": "78.945",
            "certificateInfo":
            {
                "subject":
                {
                    "countryName": "US",
                    "stateOrProvinceName": "California",
                    "localityName": "San Francisco",
                    "organizationName": "Cloudflare, Inc.",
                    "commonName": "news24.com"
                },
                "certificateIssuer":
                {
                    "countryName": "US",
                    "organizationName": "Cloudflare, Inc.",
                    "commonName": "Cloudflare Inc ECC CA-3"
                },
                "version": 3,
                "serialNumber": "0A3FFDC35976BA08FD0F9C1DD8F83731",
                "notBefore": "Apr 30 00:00:00 2022 GMT",
                "notAfter": "Apr 30 23:59:59 2023 GMT",
                "timeLeft": "10 months, 4 days, 11 hours, 33 minutes, 18 seconds",
                "OCSP":
                [
                    "http://ocsp.digicert.com"
                ],
                "crlDistributionPoints":
                [
                    "http://crl3.digicert.com/CloudflareIncECCCA-3.crl",
                    "http://crl4.digicert.com/CloudflareIncECCCA-3.crl"
                ],
                "caIssuers":
                [
                    "http://cacerts.digicert.com/CloudflareIncECCCA-3.crt"
                ],
                "subjectAltName":
                {
                    "DNS0": "*.news24.com",
                    "DNS1": "news24.com"
                },
                "percentageUtilization": "15.72"
            }
        },
        {
            "hostname": "reuters.com",
            "port": 443,
            "startTime": "2022/06/26 12:26:41.676561",
            "endTime": "2022/06/26 12:26:41.976589",
            "queryTime": "300.028",
            "certificateInfo":
            {
                "subject":
                {
                    "commonName": "reuters.com"
                },
                "certificateIssuer":
                {
                    "countryName": "US",
                    "organizationName": "Let's Encrypt",
                    "commonName": "R3"
                },
                "version": 3,
                "serialNumber": "04203F2F15F8194772481DABC1061E213EAB",
                "notBefore": "Jun  6 12:54:06 2022 GMT",
                "notAfter": "Sep  4 12:54:05 2022 GMT",
                "timeLeft": "2 months, 9 days, 27 minutes, 24 seconds",
                "OCSP":
                [
                    "http://r3.o.lencr.org"
                ],
                "caIssuers":
                [
                    "http://r3.i.lencr.org/"
                ],
                "subjectAltName":
                {
                    "DNS0": "reuters.com"
                },
                "percentageUtilization": "22.20"
            }
        },
        {
            "hostname": "thisisaverybadhost.xyz",
            "port": 443,
            "startTime": "2022/06/26 12:26:43.323313",
            "endTime": "2022/06/26 12:26:43.331015",
            "queryTime": "0.007702",
            "certificateInfo":
            {
                "subject":
                {
                    "None": "None"
                },
                "certificateIssuer":
                {
                    "None": "None"
                },
                "version": 0,
                "serialNumber": "0",
                "notBefore": "Jan 1 00:00:00 0000 GMT",
                "notAfter": "Jan 1 00:00:00 0000 GMT",
                "timeLeft": "0 seconds",
                "OCSP": "None",
                "crlDistributionPoints": "None",
                "caIssuers": "None",
                "subjectAltName":
                {
                    "None": "None"
                },
                "percentageUtilization": "0.00"
            }
        }
    ]
}
```
