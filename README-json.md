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
    "deviceId": "2a4123c9-3051-405f-b7ae-9341346c57d",
    "deviceTag": "",
    "clientHostName": "PRODMON01",
    "dataFormatVersion": 20,
    "queryStatistics":
    {
        "scriptStartTime": "2022-10-23T22:57:55.637526",
        "scriptEndTime": "2022-10-23T22:57:55.684981",
        "scriptExecutionTime": 47.45,
        "averageQueryTime": 47.45,
        "averageCertificateUtilization": 45.58,
        "averageTemplateTime": 34127999,
        "averageTemplateTimeHumanReadable": "1 year, 29 days, 15 hours, 59 minutes, 59 seconds",
        "lowestCertificateTemplateTime": 34127999,
        "lowestCertificateTemplateTimeHumanReadable": "1 year, 29 days, 15 hours, 59 minutes, 59 seconds",
        "highestCertificateTemplateTime": 34127999,
        "highestCertificateTemplateTimeHumanReadable": "1 year, 29 days, 15 hours, 59 minutes, 59 seconds",
        "commonCAIssuersCount":
        {
            "Apple Public EV Server ECC CA 1 - G1": 1
        },
        "commonCipherInfoCount":
        {
            "bits":
            {
                "128": 1
            },
            "cipher":
            {
                "TLS_AES_128_GCM_SHA256": 1
            },
            "version":
            {
                "TLSv1.3": 1
            }
        },
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
            "startTime": "2022-10-23T22:57:55.637526",
            "endTime": "2022-10-23T22:57:55.684981",
            "queryTime": 47.45,
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
            "timeLeft": "7 months, 2 days, 23 hours, 41 seconds",
            "percentageUtilization": 45.58,
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
    "dataFormatVersion": 20,
    "queryStatistics":
    {
        "scriptStartTime": "2022-10-23T22:50:12.830321",
        "scriptEndTime": "2022-10-23T22:50:14.251425",
        "scriptExecutionTime": 1421.1,
        "averageQueryTime": 282.82,
        "averageCertificateUtilization": 38.05,
        "averageTemplateTime": 22584959,
        "averageTemplateTimeHumanReadable": "8 months, 18 days, 2 hours, 35 minutes, 59 seconds",
        "lowestCertificateTemplateTime": 7775999,
        "lowestCertificateTemplateTimeHumanReadable": "2 months, 30 days, 15 hours, 59 minutes, 59 seconds",
        "highestCertificateTemplateTime": 34127999,
        "highestCertificateTemplateTimeHumanReadable": "1 year, 29 days, 15 hours, 59 minutes, 59 seconds",
        "commonCAIssuersCount":
        {
            "Apple Public EV Server ECC CA 1 - G1": 1,
            "Cloudflare Inc ECC CA-3": 1,
            "COMODO RSA Organization Validation Secure Server CA": 1,
            "R3": 2
        },
        "commonCipherInfoCount":
        {
            "bits":
            {
                "128": 2,
                "256": 3
            },
            "cipher":
            {
                "TLS_AES_128_GCM_SHA256": 1,
                "TLS_AES_256_GCM_SHA384": 3,
                "ECDHE-RSA-AES128-GCM-SHA256": 1
            },
            "version":
            {
                "TLSv1.3": 4,
                "TLSv1.2": 1
            }
        },
        "numberofTests":
        {
            "success": 5,
            "failed": 1
        }
    },
    "certResults":
    [
        {
            "hostname": "apple.com",
            "port": 443,
            "startTime": "2022-10-23T22:50:12.830354",
            "endTime": "2022-10-23T22:50:12.874737",
            "queryTime": 44.38,
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
            "timeLeft": "7 months, 2 days, 23 hours, 8 minutes, 24 seconds",
            "percentageUtilization": 45.58,
            "certificateTemplateTime": 34127999
        },
        {
            "hostname": "news24.com",
            "port": 443,
            "startTime": "2022-10-23T22:50:12.876082",
            "endTime": "2022-10-23T22:50:12.946077",
            "queryTime": 70.0,
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
            "timeLeft": "6 months, 7 days, 1 hour, 9 minutes, 47 seconds",
            "percentageUtilization": 48.35,
            "certificateTemplateTime": 31622399
        },
        {
            "hostname": "reuters.com",
            "port": 443,
            "startTime": "2022-10-23T22:50:12.946226",
            "endTime": "2022-10-23T22:50:13.222335",
            "queryTime": 276.11,
            "connectionCipher":
            [
                "ECDHE-RSA-AES128-GCM-SHA256",
                "TLSv1.2",
                128
            ],
            "certificateInfo":
            {
                "certificateIssuer":
                {
                    "countryName": "GB",
                    "stateOrProvinceName": "Greater Manchester",
                    "localityName": "Salford",
                    "organizationName": "COMODO CA Limited",
                    "commonName": "COMODO RSA Organization Validation Secure Server CA"
                },
                "version": 3,
                "serialNumber": "E0D89C311AF7835D847BB6EBD4BB4E82",
                "notBefore": "Oct 14 00:00:00 2022 GMT",
                "notAfter": "Oct 14 23:59:59 2023 GMT",
                "caIssuers":
                [
                    "http://crt.comodoca.com/COMODORSAOrganizationValidationSecureServerCA.crt"
                ],
                "subjectAltName":
                {
                    "DNS0": "thomsonreuters.com",
                    "DNS1": "*.casecenter.tr.com",
                    "DNS2": "*.findlaw.com",
                    "DNS3": "*.int.thomsonreuters.com",
                    "DNS4": "*.learnlive.com",
                    "DNS5": "*.mobile.reuters.com",
                    "DNS6": "*.reuters.com",
                    "DNS7": "*.thomson.com",
                    "DNS8": "*.thomsonreuters.com",
                    "DNS9": "*.westlaw.com",
                    "DNS10": "acceluslms.com",
                    "DNS11": "adviser.accelus.com",
                    "DNS12": "archbolde-update.co.uk",
                    "DNS13": "breakingviews.com",
                    "DNS14": "carswell.com",
                    "DNS15": "caselines.com",
                    "DNS16": "clb1.canadalawbook.ca",
                    "DNS17": "clb7.canadalawbook.ca",
                    "DNS18": "cpeasy.com",
                    "DNS19": "cvmailasia.com",
                    "DNS20": "deskcopy.thomsonreuters.ca",
                    "DNS21": "editionsyvonblais.com",
                    "DNS22": "fastsalestax.com",
                    "DNS23": "find.support.checkpoint.thomsonreuters.com",
                    "DNS24": "findandprint.com",
                    "DNS25": "findprint.com",
                    "DNS26": "funds.in.reuters.com",
                    "DNS27": "funds.uk.reuters.com",
                    "DNS28": "funds.us.reuters.com",
                    "DNS29": "highq.com",
                    "DNS30": "hk-lawyer.org",
                    "DNS31": "iblj.com",
                    "DNS32": "jctadmin.com",
                    "DNS33": "laley.com.ar",
                    "DNS34": "lawtel.com",
                    "DNS35": "legalbusinessonline.com",
                    "DNS36": "legaledcenter.com",
                    "DNS37": "livenotecentral.com",
                    "DNS38": "login.westlawasia.com",
                    "DNS39": "login.westlawindia.com",
                    "DNS40": "oconnors.com",
                    "DNS41": "onesourcelogin.com.au",
                    "DNS42": "onesourcelogin.eu",
                    "DNS43": "onesourcetax.com",
                    "DNS44": "ordermgr.courtexpress.westlaw.com",
                    "DNS45": "quickview.com",
                    "DNS46": "reuters.co.uk",
                    "DNS47": "reuters.com",
                    "DNS48": "reuters.com.cn",
                    "DNS49": "reuters.de",
                    "DNS50": "reuters.es",
                    "DNS51": "reuters.fr",
                    "DNS52": "reuters.it",
                    "DNS53": "reutersagency.com",
                    "DNS54": "reutersconnect.com",
                    "DNS55": "roundhall.ie",
                    "DNS56": "serengetilaw.com",
                    "DNS57": "services.serengetilaw.com",
                    "DNS58": "stockscreener.in.reuters.com",
                    "DNS59": "stockscreener.uk.reuters.com",
                    "DNS60": "stockscreener.us.reuters.com",
                    "DNS61": "support.riahome.com",
                    "DNS62": "support2.riahome.com",
                    "DNS63": "sweetandmaxwell.co.uk",
                    "DNS64": "thomson.com",
                    "DNS65": "thomsonreuters.ca",
                    "DNS66": "thomsonreuters.cn",
                    "DNS67": "thomsonreuters.co.jp",
                    "DNS68": "thomsonreuters.co.kr",
                    "DNS69": "thomsonreuters.co.nz",
                    "DNS70": "thomsonreuters.com.au",
                    "DNS71": "thomsonreuters.com.br",
                    "DNS72": "thomsonreuters.com.hk",
                    "DNS73": "thomsonreuters.com.my",
                    "DNS74": "thomsonreuters.com.pe",
                    "DNS75": "thomsonreuters.com.sg",
                    "DNS76": "thomsonreuters.es",
                    "DNS77": "thomsonreuters.in",
                    "DNS78": "thomsonreutersmexico.com",
                    "DNS79": "tr.com",
                    "DNS80": "tracker.serengetilaw.com",
                    "DNS81": "training.digita.thomsonreuters.com",
                    "DNS82": "triform.com",
                    "DNS83": "westfindandprint.com",
                    "DNS84": "westfindprint.com",
                    "DNS85": "westlawasia.com",
                    "DNS86": "westlawnextcanada.com",
                    "DNS87": "www.acceluslms.com",
                    "DNS88": "www.adviser.accelus.com",
                    "DNS89": "www.adviser.westlaw.com",
                    "DNS90": "www.analytics.hotprod.westlaw.com",
                    "DNS91": "www.analytics.qed.westlaw.com",
                    "DNS92": "www.analytics.westlaw.com",
                    "DNS93": "www.archbolde-update.co.uk",
                    "DNS94": "www.ca.practicallaw.thomsonreuters.com",
                    "DNS95": "www.carswell.com",
                    "DNS96": "www.cn.reuters.com",
                    "DNS97": "www.cpeasy.com",
                    "DNS98": "www.cvmailasia.com",
                    "DNS99": "www.drafting.westlaw.com",
                    "DNS100": "www.ediscoverypoint.thomsonreuters.com",
                    "DNS101": "www.editionsyvonblais.com",
                    "DNS102": "www.findandprint.com",
                    "DNS103": "www.findprint.com",
                    "DNS104": "www.findprint.westlaw.com",
                    "DNS105": "www.firmcentral.hotprod.westlaw.com",
                    "DNS106": "www.firmcentral.qed.westlaw.com",
                    "DNS107": "www.firmcentral.westlaw.com",
                    "DNS108": "www.forms.hotprod.westlaw.com",
                    "DNS109": "www.forms.qed.westlaw.com",
                    "DNS110": "www.forms.westlaw.com",
                    "DNS111": "www.iblj.com",
                    "DNS112": "www.laley.com.ar",
                    "DNS113": "www.lawtel.com",
                    "DNS114": "www.login.westlawindia.com",
                    "DNS115": "www.monitorsuite.thomsonreuters.com",
                    "DNS116": "www.nextcanada.hotprod.westlaw.com",
                    "DNS117": "www.nextcanada.qed.westlaw.com",
                    "DNS118": "www.nextcanada.westlaw.com",
                    "DNS119": "www.oconnors.com",
                    "DNS120": "www.practicetechnology.thomsonreuters.com",
                    "DNS121": "www.proview.hotprod.thomsonreuters.com",
                    "DNS122": "www.proview.thomsonreuters.com",
                    "DNS123": "www.reuters.co.uk",
                    "DNS124": "www.reuters.com.cn",
                    "DNS125": "www.reuters.de",
                    "DNS126": "www.reuters.es",
                    "DNS127": "www.reuters.fr",
                    "DNS128": "www.reuters.it",
                    "DNS129": "www.roundhall.ie",
                    "DNS130": "www.serengetilaw.com",
                    "DNS131": "www.support.riahome.com",
                    "DNS132": "www.tr.com",
                    "DNS133": "www.triform.com",
                    "DNS134": "www.v3.taxnetpro.com",
                    "DNS135": "www.westfindandprint.com",
                    "DNS136": "www.westfindprint.com",
                    "DNS137": "www.westlawnextcanada.com",
                    "DNS138": "www.wireless.reuters.com"
                }
            },
            "timeLeft": "11 months, 21 days, 1 hour, 9 minutes, 46 seconds",
            "percentageUtilization": 2.72,
            "certificateTemplateTime": 31622399
        },
        {
            "hostname": "test.remotenode.org",
            "port": 443,
            "startTime": "2022-10-23T22:50:13.222993",
            "endTime": "2022-10-23T22:50:13.608658",
            "queryTime": 385.66,
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
                    "organizationName": "Let's Encrypt",
                    "commonName": "R3"
                },
                "version": 3,
                "serialNumber": "03B092614FDFFC7671BFCC3F1E9B5C014F4A",
                "notBefore": "Sep 21 22:12:20 2022 GMT",
                "notAfter": "Dec 20 22:12:19 2022 GMT",
                "caIssuers":
                [
                    "http://r3.i.lencr.org/"
                ],
                "subjectAltName":
                {
                    "DNS0": "test.remotenode.org"
                }
            },
            "timeLeft": "1 month, 26 days, 23 hours, 22 minutes, 6 seconds",
            "percentageUtilization": 35.58,
            "certificateTemplateTime": 7775999
        },
        {
            "hostname": "mail.remotenode.org",
            "port": 465,
            "startTime": "2022-10-23T22:50:13.609113",
            "endTime": "2022-10-23T22:50:14.247040",
            "queryTime": 637.93,
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
                    "organizationName": "Let's Encrypt",
                    "commonName": "R3"
                },
                "version": 3,
                "serialNumber": "04C41320E31433441C6C91DC18C7F5503D70",
                "notBefore": "Sep  1 17:24:09 2022 GMT",
                "notAfter": "Nov 30 17:24:08 2022 GMT",
                "caIssuers":
                [
                    "http://r3.i.lencr.org/"
                ],
                "subjectAltName":
                {
                    "DNS0": "mail.remotenode.org"
                }
            },
            "timeLeft": "1 month, 6 days, 18 hours, 33 minutes, 54 seconds",
            "percentageUtilization": 58.03,
            "certificateTemplateTime": 7775999
        },
        {
            "hostname": "thisisaverybadhost.xyz",
            "port": 443,
            "startTime": "2022-10-23T22:50:14.247608",
            "endTime": "2022-10-23T22:50:14.251382",
            "queryTime": 3.77,
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
