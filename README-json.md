## Example of JSON structure for certificate specifically
```bash
$ python3 certCheck.py --hostname apple.com --displayCertificateJSON
```


The result outputis
```json
{
    "hostname": "apple.com",
    "port": 443,
    "startTime": "2022-07-16T22:37:17.272867",
    "endTime": "2022-07-16T22:37:17.319674",
    "queryTime": 46.81,
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
    "timeLeft": "10 months, 9 days, 23 hours, 21 minutes, 19 seconds",
    "percentageUtilization": 20.51,
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
    "clientHostName": "PRODMON01",
    "dataFormatVersion": 17,
    "scriptStartTime": "2022-07-16T22:36:25.012074",
    "scriptEndTime": "2022-07-16T22:36:25.078410",
    "scriptExecutionTime": 66.34,
    "averageQueryTime": 66.34,
    "averageCertificateUtilization": 20.51,
    "certResults":
    [
        {
            "hostname": "apple.com",
            "port": 443,
            "startTime": "2022-07-16T22:36:25.012074",
            "endTime": "2022-07-16T22:36:25.078410",
            "queryTime": 66.34,
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
            "timeLeft": "10 months, 9 days, 23 hours, 22 minutes, 11 seconds",
            "percentageUtilization": 20.51,
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
    "deviceId": "2a44a3c9-db11-4301-b7ae-9c070d76c57d",
    "deviceTag": "",
    "clientHostName": "PRODMON01",
    "dataFormatVersion": 17,
    "scriptStartTime": "2022-07-16T22:28:52.233703",
    "scriptEndTime": "2022-07-16T22:28:53.650857",
    "scriptExecutionTime": 1417.15,
    "averageQueryTime": 282.41,
    "averageCertificateUtilization": 32.39,
    "certResults":
    [
        {
            "hostname": "apple.com",
            "port": 443,
            "startTime": "2022-07-16T22:28:52.233739",
            "endTime": "2022-07-16T22:28:52.281488",
            "queryTime": 47.75,
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
            "timeLeft": "10 months, 9 days, 23 hours, 29 minutes, 44 seconds",
            "percentageUtilization": 20.51,
            "certificateTemplateTime": 34127999
        },
        {
            "hostname": "news24.com",
            "port": 443,
            "startTime": "2022-07-16T22:28:52.282717",
            "endTime": "2022-07-16T22:28:52.341212",
            "queryTime": 58.49,
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
            "timeLeft": "9 months, 14 days, 1 hour, 31 minutes, 7 seconds",
            "percentageUtilization": 21.29,
            "certificateTemplateTime": 31622399
        },
        {
            "hostname": "reuters.com",
            "port": 443,
            "startTime": "2022-07-16T22:28:52.341364",
            "endTime": "2022-07-16T22:28:52.633270",
            "queryTime": 291.91,
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
            "timeLeft": "1 month, 18 days, 14 hours, 25 minutes, 13 seconds",
            "percentageUtilization": 44.89,
            "certificateTemplateTime": 7775999
        },
        {
            "hostname": "thisisaverybadhost.xyz",
            "port": 443,
            "startTime": "2022-07-16T22:28:53.648471",
            "endTime": "2022-07-16T22:28:53.650821",
            "queryTime": 2.35,
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
