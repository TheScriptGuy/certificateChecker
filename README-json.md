## Example of JSON structure for certificate specifically
```bash
$ python3 certCheck.py --hostname apple.com --displayCertificateJSON
```


The result outputis
```json
{
    "hostname": "apple.com",
    "port": 443,
    "startTime": "2022-07-17T22:14:39.978393",
    "endTime": "2022-07-17T22:14:40.042846",
    "queryTime": 64.45,
    "connectionCipher":
    [
        "TLS_AES_128_GCM_SHA256",
        "TLSv1.3",
        128
    ],
    "certificateInfo":
    {
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
        "caIssuers":
        [
            "http://certs.apple.com/apevsecc1g1.der"
        ],
        "subjectAltName":
        {
            "DNS0": "apple.com"
        }
    },
    "timeLeft": "10 months, 8 days, 23 hours, 43 minutes, 56 seconds",
    "percentageUtilization": 20.76,
    "certificateTemplateTime": 34127999
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
    "clientHostName": "calvin",
    "dataFormatVersion": 19,
    "queryStatistics":
    {
        "scriptStartTime": "2022-07-17T22:12:54.498603",
        "scriptEndTime": "2022-07-17T22:12:54.541030",
        "scriptExecutionTime": 42.43,
        "averageQueryTime": 42.43,
        "averageCertificateUtilization": 20.76,
        "averageTemplateTime": 34127999,
        "averageTemplateTimeHumanReadable": "1 year, 29 days, 15 hours, 59 minutes, 59 seconds",
        "numberofTests":
        {
            "success": 1,
            "failed": 0
        }
    },
    "certResults":
    [
        {
            "hostname": "apple.com",
            "port": 443,
            "startTime": "2022-07-17T22:12:54.498603",
            "endTime": "2022-07-17T22:12:54.541030",
            "queryTime": 42.43,
            "connectionCipher":
            [
                "TLS_AES_128_GCM_SHA256",
                "TLSv1.3",
                128
            ],
            "certificateInfo":
            {
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
                "caIssuers":
                [
                    "http://certs.apple.com/apevsecc1g1.der"
                ],
                "subjectAltName":
                {
                    "DNS0": "apple.com"
                }
            },
            "timeLeft": "10 months, 8 days, 23 hours, 45 minutes, 42 seconds",
            "percentageUtilization": 20.76,
            "certificateTemplateTime": 34127999
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
    "dataFormatVersion": 19,
    "queryStatistics":
    {
        "scriptStartTime": "2022-07-17T22:07:46.284438",
        "scriptEndTime": "2022-07-17T22:07:46.652491",
        "scriptExecutionTime": 368.05,
        "averageQueryTime": 121.33,
        "averageCertificateUtilization": 29.43,
        "averageTemplateTime": 24508799,
        "averageTemplateTimeHumanReadable": "9 months, 10 days, 8 hours, 59 minutes, 59 seconds",
        "numberofTests":
        {
            "success": 3,
            "failed": 1
        }
    },
    "certResults":
    [
        {
            "hostname": "apple.com",
            "port": 443,
            "startTime": "2022-07-17T22:07:46.284476",
            "endTime": "2022-07-17T22:07:46.328282",
            "queryTime": 43.81,
            "connectionCipher":
            [
                "TLS_AES_128_GCM_SHA256",
                "TLSv1.3",
                128
            ],
            "certificateInfo":
            {
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
                "caIssuers":
                [
                    "http://certs.apple.com/apevsecc1g1.der"
                ],
                "subjectAltName":
                {
                    "DNS0": "apple.com"
                }
            },
            "timeLeft": "10 months, 8 days, 23 hours, 50 minutes, 50 seconds",
            "percentageUtilization": 20.76,
            "certificateTemplateTime": 34127999
        },
        {
            "hostname": "news24.com",
            "port": 443,
            "startTime": "2022-07-17T22:07:46.329542",
            "endTime": "2022-07-17T22:07:46.373214",
            "queryTime": 43.67,
            "connectionCipher":
            [
                "TLS_AES_256_GCM_SHA384",
                "TLSv1.3",
                256
            ],
            "certificateInfo":
            {
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
            "timeLeft": "9 months, 13 days, 1 hour, 52 minutes, 13 seconds",
            "percentageUtilization": 21.56,
            "certificateTemplateTime": 31622399
        },
        {
            "hostname": "reuters.com",
            "port": 443,
            "startTime": "2022-07-17T22:07:46.373394",
            "endTime": "2022-07-17T22:07:46.649901",
            "queryTime": 276.51,
            "connectionCipher":
            [
                "ECDHE-RSA-AES256-GCM-SHA384",
                "TLSv1.2",
                256
            ],
            "certificateInfo":
            {
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
                "caIssuers":
                [
                    "http://r3.i.lencr.org/"
                ],
                "subjectAltName":
                {
                    "DNS0": "reuters.com"
                }
            },
            "timeLeft": "1 month, 17 days, 14 hours, 46 minutes, 19 seconds",
            "percentageUtilization": 45.98,
            "certificateTemplateTime": 7775999
        },
        {
            "hostname": "thisisaverybadhost.xyz",
            "port": 443,
            "startTime": "2022-07-17T22:07:46.650302",
            "endTime": "2022-07-17T22:07:46.652458",
            "queryTime": 2.16,
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
            "timeLeft": "0 seconds",
            "certificateTemplateTime": 0,
            "connectionCipher":
            []
        }
    ]
}
```
