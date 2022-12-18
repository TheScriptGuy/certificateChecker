# Email Configuration Checker
# Author: Nolan Rumble
# Version: 0.01

import sys
import json
import re


class emailConfigurationChecker:
    """
    This class will validate the email configuration file is valid and working.
    If correctly defined, then it will return a True statement.
    If incorrectly defined, an error will be generated and the class will quit.
    """

    def checkConfigHostname(self, __mailConfigJson):
        """Check to see if the hostname field is defined"""
        # Check to see if hostname is defined. This is a mandatory field.
        if "hostname" in __mailConfigJson and __mailConfigJson["hostname"] == "":
            print(f"hostname field is a mandatory field and must be defined in {self.mailConfigurationFile}.")
            sys.exit(1)

    def checkConfigPort(self, __mailConfigJson):
        """Check what the port is configured as. If not defined, assume port 25."""
        # Check to see if port is defined. If not, default it to 25.
        if "port" in __mailConfigJson:
            if __mailConfigJson["port"] == "":
                self.mailConfig["port"] = 25
            else:
                self.mailConfig["port"] = __mailConfigJson["port"]
        else:
            print(f"port configuration not found in {self.mailConfigurationFile}, assuming TCP 25")
            self.mailConfig["port"] = 25

    def checkConfigLogin(self, __mailConfigJson):
        """
        Check to see if login details are defined.
        If username is defined, make sure password is also defined.
        """
        # Check to see if login details are defined.
        if "smtpuser" in __mailConfigJson:
            if __mailConfigJson["smtpuser"] != "":
                self.mailConfig["smtpuser"] = __mailConfigJson["smtpuser"]
            if "smtppass" in __mailConfigJson:
                if __mailConfigJson["smtppass"] == "":
                    print(f"Please set password field (smtppass) for login in {self.mailConfigurationFile} configuration.")
                    sys.exit(1)
                self.mailConfig["smtppass"] = __mailConfigJson["smtppass"]

    def checkConfigEmail(self, __mailConfigJson):
        """Checks the email address provided to make sure it's a valid email."""
        # Email regular expression. If this matches, email is valid.
        emailRegex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        __emailFrom = __mailConfigJson["from"]
        __emailTo = __mailConfigJson["to"]

        # Check to see if the to and from fields are valid email addresses.
        emailValid = bool(re.fullmatch(emailRegex, __emailFrom) and re.fullmatch(emailRegex, __emailTo))

        if not emailValid:
            print("Email address is not in a valid format")
            sys.exit(1)

    def checkConfigBodyTextFile(self, __mailConfigJson):
        """
        Check to see if the bodyTextFile variable exists.
        If it exists, then see if we can load the file.
        """
        if "bodyTextFile" in __mailConfigJson:
            __bodyTextFile = __mailConfigJson["bodyTextFile"]
            try:
                with open(__bodyTextFile) as bodyTextMail:
                    __bodyTextMail = bodyTextMail.read()
            except FileNotFoundError:
                print(f"bodyTextFile defined in {self.mailConfigurationFile} but I cannot find the file.")
                sys.exit(1)

    def checkConfigBodyHtmlFile(self, __mailConfigJson):
        """
        Check to see if bodyHtmlFile variable exists.
        If it exists, then see if we can load the file.
        """
        if "bodyHtmlFile" in __mailConfigJson:
            __bodyHtmlFile = __mailConfigJson["bodyHtmlFile"]
            try:
                with open(__bodyHtmlFile) as bodyHtmlMail:
                    __bodyHtmlMail = bodyHtmlMail.read()
            except FileNotFoundError:
                print(f"bodyHtmlMail defined in {self.mailConfigurationFile} but I cannot find the file.")
                sys.exit(1)

    def checkConfigStartTLS(self, __mailConfigJson):
        """Check StartTLS configuration."""
        if "startTLS" in __mailConfigJson:
            if __mailConfigJson["startTLS"].lower() == "true":
                self.mailConfig["startTLS"] = True
        else:
            print(f"startTLS configuration not found in {self.mailConfigurationFile}, assuming False")
            self.mailConfig["startTLS"] = False

    def checkConfigurationValid(self, __mailConfigJson):
        """
        Perform validation of the configuration object to see if there are any mismatches
        with what's configured and if the program will work.
        """
        self.checkConfigHostname(__mailConfigJson)
        self.checkConfigPort(__mailConfigJson)
        self.checkConfigEmail(__mailConfigJson)
        self.checkConfigLogin(__mailConfigJson)
        self.checkConfigBodyTextFile(__mailConfigJson)
        self.checkConfigBodyHtmlFile(__mailConfigJson)
        self.checkConfigStartTLS(__mailConfigJson)

        # If we get to this point, then the configuration looks good.
        return True

    def printConfigurationFile(self):
        """Print the mail configuration to stdout."""
        print(json.dumps(self.mailConfig))

    @staticmethod
    def loadConfigurationFile(__fileName):
        """
        Reads the mail.cfg file for configuration values.
        Performs some initial syntax checking.
        Returns the configuration in json format to be used.
        """
        try:
            # Open the file and read the configuration file.
            with open(__fileName) as fileNameMail:
                __mailConfig = fileNameMail.read()
            __mailConfigJson = json.loads(__mailConfig)
        except FileNotFoundError:
            print(f"Filename {__fileName} not found")
            sys.exit(1)
        except json.decoder.JSONDecodeError as e:
            print(f"Syntax error in {__fileName} file at line {e.lineno} and column {e.colno}.")
            sys.exit(1)
        return __mailConfigJson

    def validateConfiguration(self):
        """Validate configuration file. If all checks pass successfully, return the json object."""
        if self.checkConfigurationValid(self.mailConfig):
            return self.mailConfig
        return None

    def __init__(self, __mailConfigurationFile="mail.cfg"):
        """Initialize the email configuration checker class."""
        self.initialized = True
        self.mailConfigurationFile = __mailConfigurationFile

        self.mailConfig = {}
        self.mailConfig = self.loadConfigurationFile(self.mailConfigurationFile)
