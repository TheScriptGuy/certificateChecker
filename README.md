# Certificate Checker

Version: 0.19

Author: TheScriptGuy

With the growing usage of certificates within an organization, it's really easy to lose track of when a certificate will expire.
 
This python script will get the certificate from a supplied hostname and return the properties of the certificate(s) in JSON format.

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
usage: certCheck.py [-h] [--hostname HOSTNAME] [--displayCertificate] [--displayCertificateJSON] [--displayScriptDataJSON] [--displayTimeLeft] [--queryFile QUERYFILE] [--uploadJsonData UPLOADJSONDATA] [--mongoDB] [--sendEmail] [--setTag SETTAG]
                    [--delTag] [--getTag] [--renewDeviceId] [--getDeviceId] [--deleteDeviceId] [--setTenantId SETTENANTID] [--getTenantId] [--delTenantId] [--createBlankConfiguration]

Certificate Checker v0.19

optional arguments:
  -h, --help            show this help message and exit
  --hostname HOSTNAME   Hostname to get certificate from
  --displayCertificate  Display certificate info
  --displayCertificateJSON
                        Display certificate info in JSON format
  --displayScriptDataJSON
                        Display script info and queried certificates in JSON format
  --displayTimeLeft     Display time left until expiry on certificate.
  --queryFile QUERYFILE
                        Import a query file to for hostname queries. Supports local files and HTTP/HTTPS links
  --uploadJsonData UPLOADJSONDATA
                        Upload JSON data to HTTP URL via HTTP POST method.
  --mongoDB             Upload results to MongoDB. Connection details stored in mongo.cfg
  --sendEmail           Send an email with the results. SMTP connection details stored in mail.cfg
  --setTag SETTAG       Set the tag for the query results. Use commas to separate multiple tags.
  --delTag              Removes the tags from the configuration file.
  --getTag              Get tags from the configuration file.
  --renewDeviceId       Renew the device UUID value.
  --getDeviceId         Get the device UUID value from configuration file.
  --deleteDeviceId      Remove the device UUID value. When script runs again a new UUID will be generated.
  --setTenantId SETTENANTID
                        Sets the tenant ID for the script.
  --getTenantId         Gets the tenant ID from configuration file.
  --delTenantId         Deletes the tenant ID from the configuration file.
  --createBlankConfiguration
                        Creates a blank configuration file template - myConfig.json. Overwrites any existing configuration
```

[Example to send an email](https://github.com/TheScriptGuy/certificateChecker/blob/main/README-email.md)

[Example to upload to mongoDB](https://github.com/TheScriptGuy/certificateChecker/blob/main/README-mongoDB.md)

[Example of JSON structures](https://github.com/TheScriptGuy/certificateChecker/blob/main/README-json.md)

Features to add:
* Supply own CA certificate repository
