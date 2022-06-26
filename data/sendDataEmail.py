# Send email class
# Version: 0.03
# Last modified: 2022-06-16

import smtplib
import ssl
import sys
from os import path
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import uuid
from .emailConfigurationChecker import emailConfigurationChecker


class sendDataEmail:
    """sendDataEmail class"""

    def sendSecureEmail(self, __emailConfiguration, __bodyMessage):
        """
        Sends an email based off emailObject information
        using emailConfiguration
        """
        try:
            __hostname = __emailConfiguration["hostname"]
            __port = __emailConfiguration["port"]
            __from = __emailConfiguration["from"]
            __to = __emailConfiguration["to"]
            __subject = __emailConfiguration["subject"]
            __smtpuser = __emailConfiguration["smtpuser"]
            __smtppass = __emailConfiguration["smtppass"]
            __verbose = __emailConfiguration["verbose"]

            # Get the current time to be inserted into the email headers.
            createTime = datetime.datetime.now()

            # Create the email headers.
            mailMessage = MIMEMultipart("alternative")
            mailMessage["Subject"] = __subject
            mailMessage["From"] = __from
            mailMessage["To"] = __to
            mailMessage["Message-id"] = str(uuid.uuid4())
            # Sat, 04 Jun 2022 13:18:36 -0700 (PDT)
            mailMessage["Date"] = createTime.strftime("%a, %d %b %Y %H:%M:%S %z (%Z)")

            if __verbose.lower() == "true": print("Creating MIMEText")
            textMessage = MIMEText(__bodyMessage["text"], "plain")
            htmlMessage = MIMEText(__bodyMessage["html"], "html")

            if __verbose.lower() == "true": print("Attaching text and html parts")
            mailMessage.attach(textMessage)
            mailMessage.attach(htmlMessage)

            if __verbose.lower() == "true": print("Creating SSL default context")
            ssl_context = ssl.create_default_context()

            with smtplib.SMTP_SSL(__hostname, __port, context=ssl_context) as smtpSecureServer:
                if __verbose.lower() == "true": print(f"Login to {__hostname}")
                smtpSecureServer.login(__smtpuser, __smtppass)
                if __verbose.lower() == "true": print("Sending email")
                smtpSecureServer.sendmail(__from, __to, mailMessage.as_string())
                if __verbose.lower() == "true": print("Done")
        except Exception as e:
            print("Exception - ruh roh")
            print(e)

    def setConfigDefaults(self):
        """Set the defaults for the variables/config options."""
        # mailConfiguration defaults
        self.mailConfig = {
            "hostname": "",
            "port": 25,
            "startTLS": False,
            "smtpuser": "",
            "smtppass": "",
            "to": "",
            "from": "",
            "subject": "",
            "bodyTextFile": "",
            "bodyHtmlFile": "",
            "verbose": False
        }

    def __init__(self, __bodyMessage, __mailConfigurationFile="mail.cfg"):
        """Initialize the sendDataEmail class"""
        # Initalize the class
        self.initialized = True

        self.setConfigDefaults()

        emailConfigChecker = emailConfigurationChecker(__mailConfigurationFile)


        # Load the configuration file. By default, load mail.cfg
        self.mailConfig = emailConfigChecker.validateConfiguration()

        if self.mailConfig["startTLS"]:
            self.sendSecureEmail(self.mailConfig, __bodyMessage)
