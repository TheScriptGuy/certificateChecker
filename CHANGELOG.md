# 2022/04/15
## Version 0.09
## Changes
* Added ability to query a custom port. Script will by default connect on port 443, but you can append a port number in the --queryFile reference (the file that it's iterating through) with a :port_number. e.g. example.com:443

## Version 0.08
## Changes
* Added queryFile option. Allows the querying of multiple hostnames in a single file on filesystem or downloading it from a HTTP/HTTPS link.
* Updated JSON format to reflect new data version due to multiple certificates that can now appear in structure.
* Updated the display output of howMuchTimeLeft function to also show the commonName of the certificate.

# 2022/04/10
## Changes
* Adding comments to certificateModule and a version number.

# 2022/04/03
## Version 0.07
## Changes
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
