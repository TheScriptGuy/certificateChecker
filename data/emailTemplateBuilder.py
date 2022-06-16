# Email Template builder class
# Version: 0.01
# Author: Nolan Rumble

from .emailConfigurationChecker import emailConfigurationChecker


class emailTemplateBuilder:
    """
    Email template builder class.

    This class is designed to take the results from all the queries and build resulting emails from the defined templates
    to send them out.
    """
    def getEmailTemplate(self, __fileName):
        """Retrieves the email text template from the mail configuration file."""
        emailTemplateFileName = __fileName

        with open(emailTemplateFileName) as emailTemplateFile:
            emailContents = emailTemplateFile.read()

        return emailContents


    def monitoredHostsText(self, __jsonData):
        """Builds out the text template for monitored hosts."""
        __newBodyText = ""

        # Work out the maximum length for the hostnames we're monitoring (for formatting purposes)
        maxHostname = max(len(entry["hostname"]) for entry in __jsonData["certResults"]) + 3

        # Ports can only be a maximum of 65535 (length = 5), so add 1 for additional spacing
        maxPort = 6

        # Max Time Left
        maxTimeLeft = max(len(entry["certificateInfo"]["timeLeft"]) for entry in __jsonData["certResults"]) + 3

        # Max Percentage Utilization. Max number of digits including decimal is 6.
        maxPercentageUtilization = 6

        # The filler is the buffer between columns. In this case, a space character.
        filler = " "
        
        # Create the headers for the text.
        bodyTextHeaders = f'{"Hostname":{filler}<{maxHostname}}{"Port":{filler}<6}{"Time Left":{filler}<{maxTimeLeft}}{"Utilization":{filler}<{maxPercentageUtilization}}\n'
        monitoredHostsFormattedText = ""
        
        # Iterate through all the entries in __jsonData
        for entry in __jsonData["certResults"]:
            iHostname = entry["hostname"]
            iPort = entry["port"]
            iTimeLeft = entry["certificateInfo"]["timeLeft"]
            iPercentageUtilization = entry["certificateInfo"]["percentageUtilization"]
            
            # Build the string from all of the components above with the correct formatting.
            monitoredHostsFormattedText += f"{iHostname:{filler}<{maxHostname}}{iPort:{filler}<6}{iTimeLeft:{filler}<{maxTimeLeft}}{iPercentageUtilization:{filler}<{maxPercentageUtilization}}" + "\n"
        
        # Go through the body text message and replace the MONITOREDHOSTS field with the newly formatted hostnames and ports.
        __newBodyText = bodyTextHeaders + monitoredHostsFormattedText

        return __newBodyText


    def monitoredHostsHtml(self, __jsonData):
        """Builds out the html template for monitored hosts."""
        __newBodyHtml = ""
        monitoredHostsFormattedHtmlHeaders = ""
        monitoredHostsFormattedHtmlHeaders = "<tr><th>Hostname</th><th>Port</th><th>Time Left</th><th>Utilization</th></tr>\n"

        monitoredHostsFormattedHtml = ""

        for entry in __jsonData["certResults"]:
            iHostname = entry["hostname"]
            iPort = entry["port"]
            iTimeLeft = entry["certificateInfo"]["timeLeft"]
            iPercentageUtilization = entry["certificateInfo"]["percentageUtilization"]

            monitoredHostsFormattedHtml += f"<tr><td>{iHostname}</td><td>{iPort}</td><td>{iTimeLeft}</td><td>{iPercentageUtilization}</td></tr>\n"
        __newBodyHtml = "<table>\n" + monitoredHostsFormattedHtmlHeaders + monitoredHostsFormattedHtml + "</table>\n"

        return __newBodyHtml


    def buildEmailFromTextTemplate(self, __jsonData):
        """Modifies a text file template based off the submitted hosts."""
        self.bodyMessage["text"] = self.bodyMessage["text"].replace("MONITOREDHOSTS", self.monitoredHostsText(__jsonData))


    def buildEmailFromHtmlTemplate(self, __jsonData):
        """Modifies a HTML template based off the submitted hosts."""
        self.bodyMessage["html"] = self.bodyMessage["html"].replace("MONITOREDHOSTS", self.monitoredHostsHtml(__jsonData))


    def setConfigDefaults(self):
        """Sets the defaults for the variables/config options."""
        self.bodyMessage = {
            "text": "MONITOREDHOSTS",
            "html": "MONITOREDHOSTS"
        }


    def returnBodyMessage(self):
        """Returns the contents of the self.bodyMessage variable."""
        return self.bodyMessage


    def printBodyMessageText(self):
        """Print the text body message of the email."""
        print(self.bodyMessage["text"])


    def printBodyMessageHtml(self):
        """Print the html body message of the email."""
        print(self.bodyMessage["html"])


    def __init__(self, __jsonScriptData, __mailConfigurationFile="mail.cfg"):
        """Initialize the class."""
        self.initialized = True
        self.setConfigDefaults()

        emailConfig = emailConfigurationChecker(__mailConfigurationFile)
        
        self.mailConfig = emailConfig.validateConfiguration()
        
        self.bodyMessage["text"] = self.getEmailTemplate(self.mailConfig["bodyTextFile"])
        self.bodyMessage["html"] = self.getEmailTemplate(self.mailConfig["bodyHtmlFile"])
