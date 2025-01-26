import configparser
import os

# Instantiate the ConfigParser object
config = configparser.ConfigParser()

# Read the configuration file
config.read(os.path.join(os.path.abspath(os.curdir), 'configuration', 'config.ini'))


class ReadConfig:
    @staticmethod
    def getApplicationUrl():
        url = config.get('commonInfo', 'baseUrl')
        return url

    @staticmethod
    def getText():
        text = config.get('commonInfo', 'Text')
        return text

