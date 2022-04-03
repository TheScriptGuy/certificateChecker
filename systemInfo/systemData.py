import uuid
import sys
import os.path
from os import path

class systemData:

    def setTag(self,tagName):
        f_tag = open(self.tagFilename,'w')
        f_tag.write(tagName)
        f_tag.close()

    def deleteTag(self):
        if path.exists(self.tagFilename):
            os.remove(self.tagFilename)
        else:
            print('Tag file does not exist.')
            sys.exit(1)

    def deleteUuid(self):
        if path.exists(self.uuidFilename):
            os.remove(self.uuidFilename)
        else:
            print('UUID file does not exist.')
            sys.exit(1)
    
    def generateNewUuid(self):
        os.remove(self.uuidFilename)
        self.uuid = self.getUuid()

    def generateUuid(self):
        return str(uuid.uuid4())


    def createUuidIfNotExist(self):
        if not path.exists(self.uuidFilename):
            newUuid = self.generateUuid()
            f_uuid = open(self.uuidFilename,'w')
            f_uuid.write(str(newUuid))
            f_uuid.close()

    def __init__(self):
        self.uuidFilename = 'uuid.cfg'
        self.tagFilename = 'tag.cfg'
