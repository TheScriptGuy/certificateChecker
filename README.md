# Certificate Checker

Version: 0.62

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
python3 certChecker.py --hostname example.com --displayTimeLeft
```

## Help output
```bash
usage: certCheck.py [-h] [--hostname HOSTNAME] [--save_certificate] [--output_directory OUTPUT_DIRECTORY] [--displayCertificate] [--displayCertificateJSON] [--displayScriptDataJSON] [--displayTimeLeft]
                    [--queryFile QUERYFILE] [--uploadJsonData UPLOADJSONDATA] [--mongoDB] [--sendEmail] [--retryAmount RETRYAMOUNT] [--timeBetweenRetries TIMEBETWEENRETRIES] [--contextVariables] [--environmentVariables]
                    [--setTag SETTAG] [--delTag] [--getTag] [--renewDeviceId] [--getDeviceId] [--deleteDeviceId] [--setTenantId SETTENANTID] [--getTenantId] [--delTenantId] [--createBlankConfiguration]

Certificate Checker v0.62

options:
  -h, --help            show this help message and exit
  --hostname HOSTNAME   Hostname to get certificate from
  --save_certificate    Save the certificate to file.
  --output_directory OUTPUT_DIRECTORY
                        Save the file to the certificate directory. Will create directory if it does not exist. Defaults to certificate_directory
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
  --retryAmount RETRYAMOUNT
                        Attempt to retry the connection if any error occured. Defaults to 1 attempt.
  --timeBetweenRetries TIMEBETWEENRETRIES
                        The number of seconds between each retry attempt if the connection fails. Defaults to 1 second.
  --contextVariables    Read the context variables from contextVariables.json
  --environmentVariables
                        Uses the environment values for TENANT_ID and TAG to set the runtime environment.
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

## Saving certificate data to disk
If there is a need to save the files to disk, use the `--save_certificate` and `--output_directory` arguments.
Some examples
```bash
$ python3 certCheck.py --hostname google.com --save_certificate
2024-01-07 00:09:47 - Certificate for host google.com:443 saved to certificate_directory/bb701e2040fc41cbc99c6a152ab6aa6ea8f8488c13321df70efcf132e0fe8e1d.pem...Done
```
Notice that the certificate is saveed into the `certificate_directory` by default.
To adjust the save location, use the `--output_directory` argument.

In this example below, we'll save the certificates into the `saved_certs/2024` directory (neither of these directories exist).
```bash
$ python3 certCheck.py --hostname google.com --save_certificate --output_directory saved_certs/2024
2024-01-07 00:12:14 - Certificate for host google.com:443 saved to saved_certs/2024/bb701e2040fc41cbc99c6a152ab6aa6ea8f8488c13321df70efcf132e0fe8e1d.pem...Done
$ ls -l saved_certs/2024
total 4
-rw-r--r-- 1 programming programming 3701 Jan  6 16:12 bb701e2040fc41cbc99c6a152ab6aa6ea8f8488c13321df70efcf132e0fe8e1d.pem
```


## Environment variables
The script will by default attempt to look at a configuration file for the Tenant ID and Tags. If the environment variables are defined, then it will use that in preference to the configuration file.

To use, first define the variables:
```bash
$ export TENANT_ID="<insert tenant id here>"
$ export TAGS="<insert comma separated values>"
```

Now that environment variables are defined, we can use the `--environmentVariables` argument:
```bash
$ python3 certCheck.py --hostname apple.com --environmentVariables --displayScriptDataJSON
```

[Example of queryFile structure](https://github.com/TheScriptGuy/certificateChecker/blob/main/README-queryFile.md)

[Example to send an email](https://github.com/TheScriptGuy/certificateChecker/blob/main/README-email.md)

[Example to upload to mongoDB](https://github.com/TheScriptGuy/certificateChecker/blob/main/README-mongoDB.md)

[Example of JSON structures](https://github.com/TheScriptGuy/certificateChecker/blob/main/README-json.md)

