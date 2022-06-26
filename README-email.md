## Example to send email1
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


