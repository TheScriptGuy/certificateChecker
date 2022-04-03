import socket
import os.path
from os import path

class systemInfo:

    uuidFilename = 'uuid.cfg'
    tagFilename = 'tag.cfg'

    def getHostname(self):
        return socket.gethostname()

    def getUuid(self):
        if path.exists(self.uuidFilename):
            f_uuid = open(self.uuidFilename,'r')
            myUuid = f_uuid.readline()
            f_uuid.close()
            return myUuid
        else:
            return ""

    def getTag(self):
        if path.exists(self.tagFilename):
            f_tag = open(self.tagFilename,'r')
            myTag = f_tag.readline().rstrip()
            f_tag.close()
            return myTag
        else:
            return ""

    def __init__(self):
        self.hostname = self.getHostname()
        self.uuid = self.getUuid()
        self.deviceTag = self.getTag()

