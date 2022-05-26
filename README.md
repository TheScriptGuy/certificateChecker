# Certificate Checker

Version: 0.16

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
$ python3 certCheck.py -h
usage: certCheck.py [-h] [--hostname HOSTNAME] [--displayCertificate]
                    [--displayCertificateJSON] [--displayScriptDataJSON]
                    [--displayTimeLeft] [--queryFile QUERYFILE]
                    [--uploadJsonData UPLOADJSONDATA] [--mongoDB]
                    [--setTag SETTAG] [--deleteTag] [--getTag] [--renewUuid]
                    [--getUuid] [--deleteUuid]

Certificate Checker v0.16

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


## Example of JSON structure for certificate specifically
```json
{
    "hostname": "apple.com",
    "port": 443,
    "startTime": "2022/05/26 06:47:33.990177",
    "endTime": "2022/05/26 06:47:34.044048",
    "queryTime": "0.053871",
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
        "timeLeft": "1 year, 15 hours, 11 minutes, 2 seconds",
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
        "percentageUtilization": "7.43"
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
    "deviceUuid": "d6120e04-9e95-4510-a08b-ee9caf72cbec",
    "deviceTag":
    [
        "production"
    ],
    "clientHostName": "PRODMON01",
    "dataFormatVersion": 5,
    "certResults":
    {
        "hostname": "apple.com",
        "port": 443,
        "startTime": "2022/05/26 06:51:22.572464",
        "endTime": "2022/05/26 06:51:22.620406",
        "queryTime": "0.047942",
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
            "timeLeft": "1 year, 15 hours, 7 minutes, 14 seconds",
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
            "percentageUtilization": "7.44"
        }
    }
}

```

Features to add:
* Supply own CA certificate repository
* send email notification that script is about to expire within <X> number of days.
