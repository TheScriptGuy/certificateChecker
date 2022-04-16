# Certificate Checker

Version: 0.09

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
                    [--uploadJsonData UPLOADJSONDATA] [--setTag SETTAG]
                    [--deleteTag] [--getTag] [--renewUuid] [--getUuid]
                    [--deleteUuid]

Certificate Checker V0.09

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
  --setTag SETTAG       Set the tag for the query results. Creates tag.cfg
                        file with tag.
  --deleteTag           Delete the tag file - tag.cfg
  --getTag              Get the tag from tag.cfg file
  --renewUuid           Renew the UUID value.
  --getUuid             Get the UUID value from uuid.cfg file.
  --deleteUuid          Remove the UUID value. Caution: when script runs again
                        a new UUID will be generated.
```

## Example of JSON structure for certificate specifically
```json
{
    "hostname": "apple.com",
    "port": 443,
    "startTime": "2022/04/10 11:51:38.435369",
    "endTime": "2022/04/10 11:51:38.493124",
    "queryTime": "0.057755",
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
        "serialNumber": "5E9661C3DD43CAB7D09D24C429A7C708",
        "notBefore": "Jun 22 11:26:36 2021 GMT",
        "notAfter": "Jul 22 11:26:35 2022 GMT",
        "timeLeft": "3 months, 11 days, 23 hours, 34 minutes, 57 seconds",
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
    }
}
```

An example of the JSON structure which includes the hostname information as well:
```json
{
    "deviceUuid": "074e7305-1231-d9a3-a61c-5a028ee6db3f",
    "deviceTag": "ProductionMonitoring",
    "clientHostName": "PRODMON01",
    "dataFormatVersion": 3,
    "certResults":
    [
        {
            "hostname": "apple.com",
            "port": 443,
            "startTime": "2022/04/15 10:12:39.139486",
            "endTime": "2022/04/15 10:12:39.230373",
            "queryTime": "0.090887",
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
                "serialNumber": "5E9661C3DD43CAB7D09D24C429A7C708",
                "notBefore": "Jun 22 11:26:36 2021 GMT",
                "notAfter": "Jul 22 11:26:35 2022 GMT",
                "timeLeft": "3 months, 7 days, 1 hour, 13 minutes, 56 seconds",
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
            }
        },
        {
            "hostname": "google.com",
            "startTime": "2022/04/15 10:12:39.234198",
            "endTime": "2022/04/15 10:12:39.333427",
            "queryTime": "0.099229",
            "certificateInfo":
            {
                "subject":
                {
                    "commonName": "*.google.com"
                },
                "certificateIssuer":
                {
                    "countryName": "US",
                    "organizationName": "Google Trust Services LLC",
                    "commonName": "GTS CA 1C3"
                },
                "version": 3,
                "serialNumber": "5FEC2188D7658A640A000000013C6752",
                "notBefore": "Mar 28 01:19:44 2022 GMT",
                "notAfter": "Jun 20 01:19:43 2022 GMT",
                "timeLeft": "2 months, 4 days, 15 hours, 7 minutes, 4 seconds",
                "OCSP":
                [
                    "http://ocsp.pki.goog/gts1c3"
                ],
                "crlDistributionPoints":
                [
                    "http://crls.pki.goog/gts1c3/QqFxbi9M48c.crl"
                ],
                "caIssuers":
                [
                    "http://pki.goog/repo/certs/gts1c3.der"
                ],
                "subjectAltName":
                {
                    "DNS0": "*.google.com",
                    "DNS1": "*.appengine.google.com",
                    "DNS2": "*.bdn.dev",
                    "DNS3": "*.cloud.google.com",
                    "DNS4": "*.crowdsource.google.com",
                    "DNS5": "*.datacompute.google.com",
                    "DNS6": "*.google.ca",
                    "DNS7": "*.google.cl",
                    "DNS8": "*.google.co.in",
                    "DNS9": "*.google.co.jp",
                    "DNS10": "*.google.co.uk",
                    "DNS11": "*.google.com.ar",
                    "DNS12": "*.google.com.au",
                    "DNS13": "*.google.com.br",
                    "DNS14": "*.google.com.co",
                    "DNS15": "*.google.com.mx",
                    "DNS16": "*.google.com.tr",
                    "DNS17": "*.google.com.vn",
                    "DNS18": "*.google.de",
                    "DNS19": "*.google.es",
                    "DNS20": "*.google.fr",
                    "DNS21": "*.google.hu",
                    "DNS22": "*.google.it",
                    "DNS23": "*.google.nl",
                    "DNS24": "*.google.pl",
                    "DNS25": "*.google.pt",
                    "DNS26": "*.googleadapis.com",
                    "DNS27": "*.googleapis.cn",
                    "DNS28": "*.googlevideo.com",
                    "DNS29": "*.gstatic.cn",
                    "DNS30": "*.gstatic-cn.com",
                    "DNS31": "googlecnapps.cn",
                    "DNS32": "*.googlecnapps.cn",
                    "DNS33": "googleapps-cn.com",
                    "DNS34": "*.googleapps-cn.com",
                    "DNS35": "gkecnapps.cn",
                    "DNS36": "*.gkecnapps.cn",
                    "DNS37": "googledownloads.cn",
                    "DNS38": "*.googledownloads.cn",
                    "DNS39": "recaptcha.net.cn",
                    "DNS40": "*.recaptcha.net.cn",
                    "DNS41": "recaptcha-cn.net",
                    "DNS42": "*.recaptcha-cn.net",
                    "DNS43": "widevine.cn",
                    "DNS44": "*.widevine.cn",
                    "DNS45": "ampproject.org.cn",
                    "DNS46": "*.ampproject.org.cn",
                    "DNS47": "ampproject.net.cn",
                    "DNS48": "*.ampproject.net.cn",
                    "DNS49": "google-analytics-cn.com",
                    "DNS50": "*.google-analytics-cn.com",
                    "DNS51": "googleadservices-cn.com",
                    "DNS52": "*.googleadservices-cn.com",
                    "DNS53": "googlevads-cn.com",
                    "DNS54": "*.googlevads-cn.com",
                    "DNS55": "googleapis-cn.com",
                    "DNS56": "*.googleapis-cn.com",
                    "DNS57": "googleoptimize-cn.com",
                    "DNS58": "*.googleoptimize-cn.com",
                    "DNS59": "doubleclick-cn.net",
                    "DNS60": "*.doubleclick-cn.net",
                    "DNS61": "*.fls.doubleclick-cn.net",
                    "DNS62": "*.g.doubleclick-cn.net",
                    "DNS63": "doubleclick.cn",
                    "DNS64": "*.doubleclick.cn",
                    "DNS65": "*.fls.doubleclick.cn",
                    "DNS66": "*.g.doubleclick.cn",
                    "DNS67": "dartsearch-cn.net",
                    "DNS68": "*.dartsearch-cn.net",
                    "DNS69": "googletraveladservices-cn.com",
                    "DNS70": "*.googletraveladservices-cn.com",
                    "DNS71": "googletagservices-cn.com",
                    "DNS72": "*.googletagservices-cn.com",
                    "DNS73": "googletagmanager-cn.com",
                    "DNS74": "*.googletagmanager-cn.com",
                    "DNS75": "googlesyndication-cn.com",
                    "DNS76": "*.googlesyndication-cn.com",
                    "DNS77": "*.safeframe.googlesyndication-cn.com",
                    "DNS78": "app-measurement-cn.com",
                    "DNS79": "*.app-measurement-cn.com",
                    "DNS80": "gvt1-cn.com",
                    "DNS81": "*.gvt1-cn.com",
                    "DNS82": "gvt2-cn.com",
                    "DNS83": "*.gvt2-cn.com",
                    "DNS84": "2mdn-cn.net",
                    "DNS85": "*.2mdn-cn.net",
                    "DNS86": "googleflights-cn.net",
                    "DNS87": "*.googleflights-cn.net",
                    "DNS88": "admob-cn.com",
                    "DNS89": "*.admob-cn.com",
                    "DNS90": "*.gstatic.com",
                    "DNS91": "*.metric.gstatic.com",
                    "DNS92": "*.gvt1.com",
                    "DNS93": "*.gcpcdn.gvt1.com",
                    "DNS94": "*.gvt2.com",
                    "DNS95": "*.gcp.gvt2.com",
                    "DNS96": "*.url.google.com",
                    "DNS97": "*.youtube-nocookie.com",
                    "DNS98": "*.ytimg.com",
                    "DNS99": "android.com",
                    "DNS100": "*.android.com",
                    "DNS101": "*.flash.android.com",
                    "DNS102": "g.cn",
                    "DNS103": "*.g.cn",
                    "DNS104": "g.co",
                    "DNS105": "*.g.co",
                    "DNS106": "goo.gl",
                    "DNS107": "www.goo.gl",
                    "DNS108": "google-analytics.com",
                    "DNS109": "*.google-analytics.com",
                    "DNS110": "google.com",
                    "DNS111": "googlecommerce.com",
                    "DNS112": "*.googlecommerce.com",
                    "DNS113": "ggpht.cn",
                    "DNS114": "*.ggpht.cn",
                    "DNS115": "urchin.com",
                    "DNS116": "*.urchin.com",
                    "DNS117": "youtu.be",
                    "DNS118": "youtube.com",
                    "DNS119": "*.youtube.com",
                    "DNS120": "youtubeeducation.com",
                    "DNS121": "*.youtubeeducation.com",
                    "DNS122": "youtubekids.com",
                    "DNS123": "*.youtubekids.com",
                    "DNS124": "yt.be",
                    "DNS125": "*.yt.be",
                    "DNS126": "android.clients.google.com",
                    "DNS127": "developer.android.google.cn",
                    "DNS128": "developers.android.google.cn",
                    "DNS129": "source.android.google.cn"
                }
            }
        },
        {
            "hostname": "abc.com",
            "port": 443,
            "startTime": "2022/04/15 10:12:39.333884",
            "endTime": "2022/04/15 10:12:39.424769",
            "queryTime": "0.090885",
            "certificateInfo":
            {
                "subject":
                {
                    "commonName": "watchdisneyfe.com"
                },
                "certificateIssuer":
                {
                    "countryName": "US",
                    "organizationName": "Amazon",
                    "organizationalUnitName": "Server CA 1B",
                    "commonName": "Amazon"
                },
                "version": 3,
                "serialNumber": "0D5B328C17A02BB90493F4D87DD3B70F",
                "notBefore": "Jul 23 00:00:00 2021 GMT",
                "notAfter": "Aug 21 23:59:59 2022 GMT",
                "timeLeft": "4 months, 6 days, 13 hours, 47 minutes, 20 seconds",
                "OCSP":
                [
                    "http://ocsp.sca1b.amazontrust.com"
                ],
                "crlDistributionPoints":
                [
                    "http://crl.sca1b.amazontrust.com/sca1b.crl"
                ],
                "caIssuers":
                [
                    "http://crt.sca1b.amazontrust.com/sca1b.crt"
                ],
                "subjectAltName":
                {
                    "DNS0": "watchdisneyfe.com",
                    "DNS1": "freeform.com",
                    "DNS2": "*.abc.com",
                    "DNS3": "*.freeform.go.com",
                    "DNS4": "*.fxtvfe.com",
                    "DNS5": "*.abc-studios.com",
                    "DNS6": "*.disneynow.com",
                    "DNS7": "oscar.go.com",
                    "DNS8": "*.abcstudios.go.com",
                    "DNS9": "*.showms.freeform.go.com",
                    "DNS10": "*.us-east-1.aws.hosted.watchdisneyfe.com",
                    "DNS11": "fxnow.fxnetworks.com",
                    "DNS12": "abcstudios.go.com",
                    "DNS13": "fxtvfe.com",
                    "DNS14": "latamtvfe.com",
                    "DNS15": "blackishtv.com",
                    "DNS16": "*.oscar.go.com",
                    "DNS17": "*.cdn.watchdisneyfe.com",
                    "DNS18": "*.marvel.com",
                    "DNS19": "*.ngtvfe.com",
                    "DNS20": "foxplay.com",
                    "DNS21": "*.geo.hosted.watchdisneyfe.com",
                    "DNS22": "freeform.go.com",
                    "DNS23": "*.abc.go.com",
                    "DNS24": "marvelfe.com",
                    "DNS25": "marvel.com",
                    "DNS26": "abc.go.com",
                    "DNS27": "disneynow.com",
                    "DNS28": "*.disneynow.go.com",
                    "DNS29": "*.marvelfe.com",
                    "DNS30": "*.foxplay.com",
                    "DNS31": "*.watchdisneyfe.com",
                    "DNS32": "abc.com",
                    "DNS33": "disneynow.go.com",
                    "DNS34": "abc-studios.com",
                    "DNS35": "*.freeform.com",
                    "DNS36": "fftvfe.com",
                    "DNS37": "*.latamtvfe.com",
                    "DNS38": "*.fftvfe.com",
                    "DNS39": "*.blackishtv.com",
                    "DNS40": "ngtvfe.com"
                }
            }
        }
    ]
}
```

Features to add:
* convert script to object orientated programming (partially done)
* Supply own CA certificate repository
* send email notification that script is about to expire within <X> number of days.
