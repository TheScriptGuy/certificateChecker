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


