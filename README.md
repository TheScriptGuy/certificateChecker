# Certificate Checker

Version: 0.18

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
usage: certCheck.py [-h] [--hostname HOSTNAME] [--displayCertificate]
                    [--displayCertificateJSON] [--displayScriptDataJSON]
                    [--displayTimeLeft] [--queryFile QUERYFILE]
                    [--uploadJsonData UPLOADJSONDATA] [--mongoDB]
                    [--sendEmail] [--setTag SETTAG] [--deleteTag] [--getTag]
                    [--renewUuid] [--getUuid] [--deleteUuid]

Certificate Checker v0.18

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
  --queryFile QUERYFILE
                        Import a query file to for hostname queries. Supports
                        local files and HTTP/HTTPS links
  --uploadJsonData UPLOADJSONDATA
                        Upload JSON data to HTTP URL via HTTP POST method.
  --mongoDB             Upload results to MongoDB. Connection details stored
                        in mongo.cfg
  --sendEmail           Send an email with the results. SMTP connection
                        details stored in mail.cfg
  --setTag SETTAG       Set the tag for the query results. Creates tag.cfg
                        file with tag. Use commas to separate multiple tags.
  --deleteTag           Delete the tag file - tag.cfg
  --getTag              Get the tag from tag.cfg file
  --renewUuid           Renew the UUID value.
  --getUuid             Get the UUID value from uuid.cfg file.
  --deleteUuid          Remove the UUID value. Caution: when script runs again
                        a new UUID will be generated.
```

## Example to upload to mongoDB
First configure the `mongo.cfg` file with the connection details in json format.

Important things to note about the mongo.cfg file:
* The fields `username`, `password`, `database`, `collection` are all optional.
* Only `uri` is mandatory.

* If `database` isn't specified then the field defaults to `certificateDataDB.`
* If `collection` isn't specified then the field defaults to `certCollection`.

```json
{
    "uri": "192.168.100.10",
    "username": "mongoUsername",
    "password": "m0ng0P4ssw0rd",
    "database": "myCertDatabase"
    "collection": "myCertCollection"
}
```

To send the data to the MongoDB run the following command (for a single host):
```bash
$ python3 certCheck.py --hostname apple.com --mongoDB
$
```
To upload the results from multiple queries:
```bash
$ python3 certCheck.py --queryFile myQueries --mongoDB
$
```

## Example to send email
If you'd like to be sent an email of the results of the queries, the mail.cfg file needs to be defined.

Some important things to note in the mail.cfg file:
* Right now only Authenticated SMTP STARTTLS is allowed. This means you need all the fields below in order to access except the verbose field.
* If the verbose field is defined to True, then additional SMTP interactions will be displayed.
* the bodyHtmlFile and bodyTextFile variables define where the HTML and TEXT versions of each file is. Make sure you add the MONITOREDHOSTS keyword into the HTML and TEXT files. This is used for inserting the results into the correct place.

```json
{
    "hostname": "mail.mysmartdomain.com",
    "port": 465,
    "smtpuser": "certChecker@email.com",
    "smtppass": "BlaPasswordBla1",
    "startTLS": "true",
    "from": "certChecker@email.com",
    "to": "your_email_here@gmail.com",
    "subject": "Certificate Checker",
    "bodyHtmlFile": "bodyhtml.html",
    "bodyTextFile": "bodytext.txt",
    "verbose": "false"
}
```


### Single host:
```bash
$ python3 certCheck.py --hostname apple.com --sendEmail
$
```

### Multiple hosts:
```bash
$ python3 certCheck.py --queryFile queryfile --sendEmail
$
```

## Example of JSON structure for certificate specifically
```json
{
    "hostname": "apple.com",
    "port": 443,
    "startTime": "2022/06/16 16:14:19.793797",
    "endTime": "2022/06/16 16:14:19.863822",
    "queryTime": "0.070025",
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
    "deviceUuid": "a1089eb8-744d-4bca-9310-9b8642a8e2e5",
    "deviceTag":
    [
        "production"
    ],
    "clientHostName": "PRODMON01",
    "dataFormatVersion": 6,
    "certResults":
    [
        {
            "hostname": "apple.com",
            "port": 443,
            "startTime": "2022/06/16 16:15:42.398002",
            "endTime": "2022/06/16 16:15:42.447273",
            "queryTime": "0.049271",
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
                "timeLeft": "11 months, 10 days, 5 hours, 42 minutes, 54 seconds",
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
        },
        {
            "hostname": "news24.com",
            "port": 443,
            "startTime": "2022/06/16 16:15:42.451359",
            "endTime": "2022/06/16 16:15:42.525880",
            "queryTime": "0.074521",
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
                "timeLeft": "10 months, 14 days, 7 hours, 44 minutes, 17 seconds",
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
                "percentageUtilization": "13.03"
            }
        },
        {
            "hostname": "reuters.com",
            "port": 443,
            "startTime": "2022/06/16 16:15:42.526309",
            "endTime": "2022/06/16 16:15:42.832125",
            "queryTime": "0.305816",
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
                "timeLeft": "2 months, 18 days, 20 hours, 38 minutes, 23 seconds",
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
                "percentageUtilization": "11.27"
            }
        },
        {
            "hostname": "test.remotenode.org",
            "port": 443,
            "startTime": "2022/06/16 16:15:42.832676",
            "endTime": "2022/06/16 16:15:43.218270",
            "queryTime": "0.385594",
            "certificateInfo":
            {
                "subject":
                {
                    "commonName": "test.remotenode.org"
                },
                "certificateIssuer":
                {
                    "countryName": "US",
                    "organizationName": "Let's Encrypt",
                    "commonName": "R3"
                },
                "version": 3,
                "serialNumber": "03ADFAA00EBD8CB2E094969B470E94725ECD",
                "notBefore": "May 23 19:59:46 2022 GMT",
                "notAfter": "Aug 21 19:59:45 2022 GMT",
                "timeLeft": "2 months, 5 days, 3 hours, 44 minutes, 2 seconds",
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
                    "DNS0": "test.remotenode.org"
                },
                "percentageUtilization": "26.49"
            }
        },
        {
            "hostname": "mail.remotenode.org",
            "port": 465,
            "startTime": "2022/06/16 16:15:43.218740",
            "endTime": "2022/06/16 16:15:44.160865",
            "queryTime": "0.942125",
            "certificateInfo":
            {
                "subject":
                {
                    "commonName": "mail.remotenode.org"
                },
                "certificateIssuer":
                {
                    "countryName": "US",
                    "organizationName": "Let's Encrypt",
                    "commonName": "R3"
                },
                "version": 3,
                "serialNumber": "048446B2E1AE9BC3A866A302418B20ECC48C",
                "notBefore": "May  4 02:56:39 2022 GMT",
                "notAfter": "Aug  2 02:56:38 2022 GMT",
                "timeLeft": "1 month, 16 days, 10 hours, 40 minutes, 54 seconds",
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
                    "DNS0": "mail.remotenode.org"
                },
                "percentageUtilization": "48.39"
            }
        },
        {
            "hostname": "thisisaverybadhost.xyz",
            "port": 443,
            "startTime": "2022/06/16 16:15:44.161469",
            "endTime": "2022/06/16 16:15:44.165156",
            "queryTime": "0.003687",
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

Features to add:
* Supply own CA certificate repository
* send email notification that script is about to expire within <X> number of days.
