# Description:        Certificate Data Handling
# Author:             TheScriptGuy
# Version:            0.10
# Last modified:      2023/10/14

import sys
from os import path
import requests
import socket
import ast


class certData:
    """certData class"""

    @staticmethod
    def getFileFromURL(fileURL: str) -> list:
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
            print(f'Could not connect to URL - {fileURL}\n')
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
    def parse_line(line: str) -> dict:
        """Create a collection of connection information based off the line string."""
        # Default values
        hostname = ''
        port = 443
        options = None

        # Remove newline character if it exists
        line = line.rstrip()

        # Check if options exist
        if '[' in line:
            line, options = line.split('[', 1)
            # Remove the closing bracket and convert to a list
            options = ast.literal_eval('[' + options)

        # Check if port number exists
        if ':' in line:
            hostname, port = line.split(':')
            port = int(port.rstrip(','))
        else:
            hostname = line.rstrip(',')

        return {"hostname": hostname, "port": port, "options": options}

    @staticmethod
    def loadQueriesFile(queriesFile: str) -> list:
        """
        This will load the queries that need to be performed against each name server.
        One hostname entry per line.
        """
        queries = []

        # Check to see if queriesFile is a URL and if it is, attempt to download it.
        if queriesFile.startswith('http://') or queriesFile.startswith('https://'):
            myQueries = certData.getFileFromURL(queriesFile)
            for line in myQueries:
                hostEntry = certData.parse_line(line)
                queries.append(hostEntry)

        elif path.exists(queriesFile) and not (queriesFile.startswith('http://') or queriesFile.startswith('https://')):
            with open(queriesFile, "r", encoding="utf-8") as f_queryFile:
                queryFile = f_queryFile.readlines()
                for line in queryFile:
                    hostEntry = certData.parse_line(line)
                    queries.append(hostEntry)
        else:
            print(f'I cannot get file {queriesFile}')
            sys.exit(1)
        return queries

    def __init__(self):
        """Initialize the certData class."""
        self.initialized = True
        self.version = "0.10"
