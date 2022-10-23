# 2022/10/23
## Version 0.31
### Changes
* updated dataFormatVersion to 20:
    * added new fields - `lowestTemplateTime`, `lowestTemplateTimeHumanReadable`, `highestTemplateTime`, `highestTemplateTimeHumanReadable`
    * added Certificate Authority Common Name count field - `commonCAIssuersCount`
    * added Common Cipher Information Connection Count - `commonCipherInfoCount`
* Example new json structure (to see more, please see [here](https://github.com/TheScriptGuy/certificateChecker/blob/main/README-json.md)):
```json
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
}
```

# 2022/07/22
## Version 0.30
### Changes
* improved MongoDB connection string handling.
* improved MongoDB error handling.

# 2022/07/17
## Version 0.30
### Changes
* Updated dataFormatVersion to 19: 
    * to reflect a new structure for the statistics (`queryStatistics`) from all the test results,
    * moved the `scriptStartTime`, `scriptEndTime`, `scriptExecutionTime`, `averageQueryTime`, `averageCertificateTemplateTime` under the `queryStatistics` field,
    * created a new dict `numberOfTests` which mentions the number of `success` and `failed` tests for the time the script was executed.
* Example new json structure (to see more, please see [here](https://github.com/TheScriptGuy/certificateChecker/blob/main/README-json.md)):
```json
"queryStatistics":
{
    "scriptStartTime": "2022-07-17T22:07:46.284438",
    "scriptEndTime": "2022-07-17T22:07:46.652491",
    "scriptExecutionTime": 368.05,
    "averageQueryTime": 121.33,
    "averageCertificateUtilization": 29.43,
    "averageTemplateTime": 24508799.0,
    "averageTemplateTimeHumanReadable": "9 months, 10 days, 8 hours, 59 minutes, 59 seconds",
    "numberofTests":
    {
        "success": 3,
        "failed": 1
    }
}
```

# 2022/07/16
## Version 0.29
### Changes
* Updated dataFormatVersion to 17 to reflect the time delta in seconds between the notBefore and notAfter times.

## Version 0.28
### Changes
* Updated dataFormatVersion to 16 to reflect 1 new field for cipher suites used in connection.

# 2022/07/10
## Version 0.27
### Changes
* Updated dataFormatVersion to 15 to reflect 2 new fields for average utilization of certificates (`averageCertificateUtilization`) and average query time (`averageQueryTime`). 

# 2022/07/04
## Version 0.26
### Fixes
* Fixed minor bug with sendDataMongoDB.py to reference collectionNames from mongo.cfg correctly.

# 2022/07/02
## Version 0.26
### Changes
* Changed dataFormatVersion to 14 to include script execution time. 

### Fixes
* Fixed a bug with the creation of the the --createConfigurationFile option.

## Version 0.25
### Changes
* Changed dataFormatVersion to 13 to include script start and end times for improved data searchability.

# 2022/07/01
## Version 0.24
### Changes
* Changed dataFormatVersion to 12 to reflect minor change to `startTime` and `endTime` formats to datetime objects for easier searching in Mongo.

## Version 0.23
### Changes
* Changed dataFormatVersion to 11 to reflect date/time changes for `startTime` and `endTime` fields to comply with `ISO8601 format`.
* Changed all references to `now()` to reference `utcnow()`

# 2022/06/28
## Version 0.22
### Changes
* Changed dataFormatVersion to 10 to reflect minor change to `percentageUtilization` and `queryTime` field from str() to float() and rounded float value to 2 decimal places.

# 2022/06/26
## Version 0.21
### Changes
* Changed dataFormatVersion to 9 to reflect new data format. The `percentageUtilization` and `timeLeft` fields have moved up one level in the data structure.

## Version 0.20
### Changes
* Changed dataFormatVersion to 8 to reflect `queryTime` change from seconds to milliseconds.

## Version 0.19
### Additions
* Added the ability to create a tenantId as part of the configuration.
* Added the --getTenantId, --setTenantId, --delTenantId arguments.
* Added the --createBlankConfiguration option to create a new configuration file.

### Changes
* Changed the arguments:
    * `--renewUuid`, now called `--renewDeviceId` 
    * `--getUuid`, now called `--getDeviceId`
    * `--deleteUuid`, now called `--deleteDeviceId`
* Changed the existing `--setTag`, `--delTag`, `--getTag` arguments to use the new configuration file.
* No longer using tag.cfg and uuid.cfg files. Combined the fields into a myConfig.json file.
* Consolidated the systemData class definitions into the systemInfo class.
* Updated dataFormatVersion to 7 to reflect new tenantId field.
* Script will always create a default configuration (myConfig.json) with following fields:
```json
{
    "myTenantId": "",
    "myTags": "",
    "myDeviceId": "unique-random-id"
}
```

# 2022/06/16
## Version 0.18
### Additions
* NEW FEATURE - send an email notification of the monitored hosts. See README.md for more details.

# 2022/06/14
## Version 0.17
### Changes
* Updated dataFormatVersion to 6. This is to address a new feature. The certResults field has changed to a list.

## Version 0.16
### Additions
* Add ability for tagging a device with multiple tags. See README.md for to apply.

### Changes
* Updated the dataFormatVersion to reflect the new multiple tag options.

# 2022/05/25
## Version 0.15
### Fixes
* Fixed a logic flaw with the --displayCertificateJSON and --queryFile argument.

### Additions
* Added a percentage utilization of the certificate time frame.

### Changes
* Updated the dataFormatVersion to reflect the new version format with the new `percentageUtilization` field.

# 2022/05/24
## Version 0.14
### Changes
* Changed the logic of how the MongoDB feature works. Moved the entries to the sendDataMongoDB.py file.

# 2022/05/16
## Version 0.13
### Additions
* Adding support for MongoDB data upload (using sendDataMongoDB class)

# 2022/04/15
## Version 0.12
### Fixes
* Aligning code with best practices.
* Fixing logic with displaying the amount of time left until certificate expires.

## Version 0.11
### Fixes
* Insert None values for a hostname that doesn't have a valid certificate into the Json output.
* Fixed bug with --hostname argument and not having the the port defined

## Version 0.10
### Fixes
* Fixed a bug with the --hostname argument and the amount of keyword arguments that needed to be used.

### Changes
* Added the ability to do a custom port with the --hostname argument. For example, `--hostname example.com` assumes you want to connect on TCP port 443. The entry `--hostname example.com:1234` connections to example.com on TCP port 1234.

## Version 0.09
### Changes
* Added ability to query a custom port. Script will by default connect on port 443, but you can append a port number in the --queryFile reference (the file that it's iterating through) with a :port_number. e.g. example.com:443

## Version 0.08
### Changes
* Added queryFile option. Allows the querying of multiple hostnames in a single file on filesystem or downloading it from a HTTP/HTTPS link.
* Updated JSON format to reflect new data version due to multiple certificates that can now appear in structure.
* Updated the display output of `howMuchTimeLeft` function to also show the commonName of the certificate.

# 2022/04/10
### Changes
* Adding comments to certificateModule and a version number.

# 2022/04/03
## Version 0.07
### Changes
* Added ability to post the results of the certificate check and system data where query is performed from (in JSON format) to a specific URL via HTTP post method.

## Version 0.06 
### Bugfixes
* Added some error handling for when a host doesn't exist.
* displayTimeLeft was not showing how much time was left for the certificate.

### Changes
* Added device UUID generation.
* Added ability to regenerate device UUID if necessary
* Added ability to add/remove tags for data aggregation purposes.
* Using more object orientated model of code (still room for improvement though)
