## Example of JSON structure for certificate specifically
```json
{
    "hostname": "apple.com",
    "port": 443,
    "startTime": "2022/06/26 21:20:43.092236",
    "endTime": "2022/06/26 21:20:43.141154",
    "queryTime": "48.918000000000006",
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
    "timeLeft": "11 months, 37 minutes, 53 seconds",
    "percentageUtilization": 15.44
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
    "deviceId": "2a44a3c9-3413-405f-b7ae-9c070d76c57d",
    "deviceTag": "",
    "clientHostName": "PRODMON01",
    "dataFormatVersion": 9,
    "certResults":
    [
        {
            "hostname": "apple.com",
            "port": 443,
            "startTime": "2022/06/26 21:25:09.099267",
            "endTime": "2022/06/26 21:25:09.150244",
            "queryTime": "50.977000000000004",
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
            "timeLeft": "11 months, 33 minutes, 27 seconds",
            "percentageUtilization": 15.44
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
    "dataFormatVersion": 9,
    "certResults":
    [
        {
            "hostname": "apple.com",
            "port": 443,
            "startTime": "2022/06/26 21:26:52.328284",
            "endTime": "2022/06/26 21:26:52.395797",
            "queryTime": "67.513",
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
            "timeLeft": "11 months, 31 minutes, 44 seconds",
            "percentageUtilization": 15.44
        },
        {
            "hostname": "news24.com",
            "port": 443,
            "startTime": "2022/06/26 21:26:52.397289",
            "endTime": "2022/06/26 21:26:52.471062",
            "queryTime": "73.77300000000001",
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
            "timeLeft": "10 months, 4 days, 2 hours, 33 minutes, 7 seconds",
            "percentageUtilization": 15.82
        },
        {
            "hostname": "reuters.com",
            "port": 443,
            "startTime": "2022/06/26 21:26:52.471413",
            "endTime": "2022/06/26 21:26:52.773433",
            "queryTime": "302.02000000000004",
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
            "timeLeft": "2 months, 8 days, 15 hours, 27 minutes, 13 seconds",
            "percentageUtilization": 22.62
        },
        {
            "hostname": "thisisaverybadhost.xyz",
            "port": 443,
            "startTime": "2022/06/26 21:26:53.971556",
            "endTime": "2022/06/26 21:26:54.025939",
            "queryTime": "54.383",
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
            "percentageUtilization": 0.00,
            "timeLeft": "0 seconds"
        }
    ]
}
```
