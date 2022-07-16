## Example of JSON structure for certificate specifically
```bash
$ python3 certCheck.py --hostname apple.com --displayCertificateJSON
```


The result outputis
```json
{
    "hostname": "apple.com",
    "port": 443,
    "startTime": "2022-07-16T21:57:07.587858",
    "endTime": "2022-07-16T21:57:07.628875",
    "queryTime": 41.02,
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
    "connectionCipher":
    [
        "TLS_AES_128_GCM_SHA256",
        "TLSv1.3",
        128
    ],
    "timeLeft": "10 months, 10 days, 1 minute, 29 seconds",
    "percentageUtilization": 20.51
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
    "deviceId": "2a44a3c9-3461-6161-b7ae-9c070d76c57d",
    "deviceTag": "",
    "clientHostName": "PRODMON01",
    "dataFormatVersion": 16,
    "scriptStartTime": "2022-07-16T21:58:14.750980",
    "scriptEndTime": "2022-07-16T21:58:14.789993",
    "scriptExecutionTime": 39.01,
    "averageQueryTime": 39.01,
    "averageCertificateUtilization": 20.51,
    "certResults":
    [
        {
            "hostname": "apple.com",
            "port": 443,
            "startTime": "2022-07-16T21:58:14.750980",
            "endTime": "2022-07-16T21:58:14.789993",
            "queryTime": 39.01,
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
            "connectionCipher":
            [
                "TLS_AES_128_GCM_SHA256",
                "TLSv1.3",
                128
            ],
            "timeLeft": "10 months, 10 days, 22 seconds",
            "percentageUtilization": 20.51
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
    "deviceId": "2a44a3c9-1235-6011-b7ae-9c070d76c57d",
    "deviceTag": "",
    "clientHostName": "PRODMON01",
    "dataFormatVersion": 16,
    "scriptStartTime": "2022-07-16T22:11:03.898656",
    "scriptEndTime": "2022-07-16T22:11:05.233176",
    "scriptExecutionTime": 1334.52,
    "averageQueryTime": 265.93,
    "averageCertificateUtilization": 32.37,
    "certResults":
    [
        {
            "hostname": "apple.com",
            "port": 443,
            "startTime": "2022-07-16T22:11:03.898688",
            "endTime": "2022-07-16T22:11:03.945809",
            "queryTime": 47.12,
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
            "timeLeft": "10 months, 9 days, 23 hours, 47 minutes, 33 seconds",
            "percentageUtilization": 20.51
        },
        {
            "hostname": "news24.com",
            "port": 443,
            "startTime": "2022-07-16T22:11:03.947064",
            "endTime": "2022-07-16T22:11:03.995779",
            "queryTime": 48.72,
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
            "timeLeft": "9 months, 14 days, 1 hour, 48 minutes, 56 seconds",
            "percentageUtilization": 21.29
        },
        {
            "hostname": "reuters.com",
            "port": 443,
            "startTime": "2022-07-16T22:11:03.995894",
            "endTime": "2022-07-16T22:11:04.288112",
            "queryTime": 292.22,
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
            "timeLeft": "1 month, 18 days, 14 hours, 43 minutes, 1 second",
            "percentageUtilization": 44.87
        },
        {
            "hostname": "thisisaverybadhost.xyz",
            "port": 443,
            "startTime": "2022-07-16T22:11:05.230848",
            "endTime": "2022-07-16T22:11:05.233140",
            "queryTime": 2.29,
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
            "connectionCipher":
            []
        }
    ]
}
```
