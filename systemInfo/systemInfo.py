import socket
import os.path
from os import path


class systemInfo:
    """systemInfo class"""

    uuidFilename = 'uuid.cfg'
    tagFilename = 'tag.cfg'

    def getHostname(self):
        """Get the hostname of the device performing the checks."""
        return socket.gethostname()

    def getUuid(self):
        """Get the uuid."""
        if path.exists(self.uuidFilename):
            with open(self.uuidFilename) as f_uuid:
                myUuid = f_uuid.readline()
            return myUuid
        else:
            return ""

    def getTag(self):
        """Get the tag."""
        if path.exists(self.tagFilename):
            with open(self.tagFilename, 'r') as f_tag:
                myTag = f_tag.readline().rstrip().split(',')
            return myTag
        else:
            return []

    def __init__(self):
        """Initialize the class."""
        self.hostname = self.getHostname()
        self.uuid = self.getUuid()
        self.deviceTag = self.getTag()
        self.classVersion = "0.02"
