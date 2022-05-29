import uuid
import sys
from os import path
import os.path


class systemData:
    """systemData class"""

    def setTag(self, tagName):
        """Set the tag for data aggregation purposes."""
        with open(self.tagFilename, 'w') as f_tag:
            f_tag.write(tagName)

    def deleteTag(self):
        """Delete the tag."""
        if path.exists(self.tagFilename):
            os.remove(self.tagFilename)
        else:
            print('Tag file does not exist.')
            sys.exit(1)

    def deleteUuid(self):
        """Delete the unique uuid file."""
        if path.exists(self.uuidFilename):
            os.remove(self.uuidFilename)
        else:
            print('UUID file does not exist.')
            sys.exit(1)

    def generateNewUuid(self):
        """Generate a new uuid."""
        os.remove(self.uuidFilename)
        self.uuid = self.getUuid()

    def generateUuid(self):
        """Generate a uuid."""
        return str(uuid.uuid4())

    def createUuidIfNotExist(self):
        """Check to see if uuid doesn't exist first."""
        if not path.exists(self.uuidFilename):
            newUuid = self.generateUuid()
            with open(self.uuidFilename, 'w') as f_uuid:
                f_uuid.write(str(newUuid))

    def __init__(self):
        """Initialize the class."""
        self.uuidFilename = 'uuid.cfg'
        self.tagFilename = 'tag.cfg'
