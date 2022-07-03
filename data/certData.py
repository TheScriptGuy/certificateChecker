# Certificate Data Handling
# Version: 0.06

import sys
from os import path
import requests
import json
import socket


class certData:
    """certData class"""

    @staticmethod
    def getFileFromURL(fileURL):
        """This function will download the contents of fileURL and return a list with the contents."""
        tmpData = []
        try:
            urlData = requests.get(fileURL)
            if urlData.status_code == 200:
                tmpData = urlData.text.split('\n')
                try:
                    # Attempt to remove any blank entries in the dict
                    tmpData.remove('')
                except ValueError:
                    pass
            else:
                tmpData = ['Error while retrieving URL']
        except socket.gaierror:
            print('Invalid hostname')
            tmpData = ['URL error']
        except requests.exceptions.Timeout:
            print('Timeout while retrieving URL.')
            tmpData = ['URL Timeout']
        except requests.exceptions.TooManyRedirects:
            print('Too many redirects while accessing the URL')
            tmpData = ['URL Redirects too many']
        except requests.exceptions.ConnectionError:
            print('Could not connect to URL - ' + fileURL + '\n')
            tmpData = ['URL connection error']

        return tmpData

    @staticmethod
    def uploadJsonHTTP(url, jsonData):
        """
        This will upload the json data to a URL via a POST method.
        If the verbose argument is set, it'll display what URL it's being
        submitted to as well as the json data (jsonData).
        When the response is returned, it'll return the X-Headers that are sent back
        from the server.
        """
        x = requests.post(url, json=jsonData)
        return x.headers

    @staticmethod
    def loadQueriesFile(queriesFile):
        """
        This will load the queries that need to be performed against each name server.
        One hostname entry per line.
        """
        queries = []

        # Check to see if queriesFile is a URL and if it is, attempt to download it.
        if queriesFile.startswith('http://') or queriesFile.startswith('https://'):
            myQueries = certData.getFileFromURL(queriesFile)
            for line in myQueries:
                if ":" in line:
                    tmpLine = line.split(':')
                    queries.append({"hostname": tmpLine[0], "port": int(tmpLine[1])})
                else:
                    queries.append({"hostname": line, "port": 443})

            return queries

        # Check to see if if the file exists. If not, exit with error code 1.
        if not path.exists(queriesFile):
            print('I cannot find file ' + queriesFile)
            sys.exit(1)

        queryFile = open(queriesFile, "r", encoding="utf-8")

        for line in queryFile:
            if ":" in line:
                tmpLine = line.rstrip('\n').split(':')
                queries.append({"hostname": tmpLine[0], "port": int(tmpLine[1])})
            else:
                queries.append({"hostname": line.rstrip('\n'), "port": 443})

        queryFile.close()

        return queries

    def __init__(self):
        """Initialize the certData class."""
        self.initialized = True
        self.version = "0.06"
