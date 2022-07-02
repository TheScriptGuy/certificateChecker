## Example of JSON structure for certificate specifically
```json
{
    "hostname": "apple.com",
    "port": 443,
    "startTime": "2022-07-01T15:53:31.509182",
    "endTime": "2022-07-01T15:53:31.560310",
    "queryTime": 51.13,
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
    },
    "timeLeft": "10 months, 25 days, 6 hours, 5 minutes, 5 seconds",
    "percentageUtilization": 16.64
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
    "dataFormatVersion": 14,
    "scriptStartTime": "2022-07-02T21:21:25.803929",
    "scriptEndTime": "2022-07-02T21:21:25.859357",
    "scriptQueryTime": 55.43,
    "certResults":
    [
        {
            "hostname": "apple.com",
            "port": 443,
            "startTime": "2022-07-02T21:21:25.803929",
            "endTime": "2022-07-02T21:21:25.859357",
            "queryTime": 55.43,
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
            },
            "timeLeft": "10 months, 24 days, 37 minutes, 11 seconds",
            "percentageUtilization": 16.96
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
    "dataFormatVersion": 14,
    "scriptStartTime": "2022-07-02T21:19:02.495375",
    "scriptEndTime": "2022-07-02T21:19:03.928107",
    "scriptQueryTime": 1432.73,
    "certResults":
    [
        {
            "hostname": "apple.com",
            "port": 443,
            "startTime": "2022-07-02T21:19:02.495407",
            "endTime": "2022-07-02T21:19:02.547379",
            "queryTime": 51.97,
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
            },
            "timeLeft": "10 months, 24 days, 39 minutes, 34 seconds",
            "percentageUtilization": 16.96
        },
        {
            "hostname": "news24.com",
            "port": 443,
            "startTime": "2022-07-02T21:19:02.549329",
            "endTime": "2022-07-02T21:19:02.602949",
            "queryTime": 53.62,
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
                }
            },
            "timeLeft": "9 months, 28 days, 2 hours, 40 minutes, 57 seconds",
            "percentageUtilization": 17.46
        },
        {
            "hostname": "reuters.com",
            "port": 443,
            "startTime": "2022-07-02T21:19:02.603078",
            "endTime": "2022-07-02T21:19:02.899738",
            "queryTime": 296.66,
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
                }
            },
            "timeLeft": "2 months, 1 day, 15 hours, 35 minutes, 3 seconds",
            "percentageUtilization": 29.28
        },
        {
            "hostname": "thisisaverybadhost.xyz",
            "port": 443,
            "startTime": "2022-07-02T21:19:03.919881",
            "endTime": "2022-07-02T21:19:03.928059",
            "queryTime": 8.18,
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
                "OCSP": "None",
                "crlDistributionPoints": "None",
                "caIssuers": "None",
                "subjectAltName":
                {
                    "None": "None"
                }
            },
            "percentageUtilization": 0.0,
            "timeLeft": "0 seconds"
        }
    ]
}
```
