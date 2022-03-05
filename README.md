# Certificate Checker

Version: 0.03
Author: TheScriptGuy

With the growing usage of certificates within an organization, it's really easy to lose track of when a certificate will expire.
 
This python script will get the certificate from a supplied hostname (defaults to google.com if nothing specified) and return the properties of the script in JSON format.

## Usage
```bash
python3 certChecker.py --hostname example.com --displayCertificateJSON
```

Features to add:
* convert script to object orientated using classes etc
* Supply own CA certificate repository
* Post results to a webserver using POST method
* send email notification that script is about to expire within <X> number of days.

