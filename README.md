# Certificate Checker

Version: 0.06

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
python3 certChecker.py -h

usage: certCheck.py [-h] [--hostname HOSTNAME] [--displayCertificate]
                    [--displayCertificateJSON] [--displayScriptDataJSON]
                    [--displayTimeLeft] [--setTag SETTAG] [--deleteTag]
                    [--getTag] [--renewUuid] [--getUuid] [--deleteUuid]

Certificate Checker V0.06

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
  --setTag SETTAG       Set the tag for the query results. Creates tag.cfg
                        file with tag.
  --deleteTag           Delete the tag file - tag.cfg
  --getTag              Get the tag from tag.cfg file
  --renewUuid           Renew the UUID value.
  --getUuid             Get the UUID value from uuid.cfg file.
  --deleteUuid          Remove the UUID value. Caution: when script runs again
                        a new UUID will be generated.
  --uploadJsonData UPLOADJSONDATA
                        Upload JSON data to HTTP URL via HTTP POST method.
```



Features to add:
* convert script to object orientated programming (partially done)
* Supply own CA certificate repository
* Post results to a webserver using POST method
* send email notification that script is about to expire within <X> number of days.

