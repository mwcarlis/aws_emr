#!/usr/bin/python
"""A security context module.
"""

# Open-Source/Free Imports
import csv
import os

# Private-IP Imports Carlis/Koumis.
# import private_ip_lib

class SecurityContext(object):
    """Abstract Security Context Object.
    """
    def __init__(self):
        raise Exception("Unimplemented")


def read_keyfile(key_file, mapping):
    """Read a key_file into a mapping.
    """
    with open(key_file, 'r') as file_d:
        key_reader = csv.reader(file_d, delimiter='=')
        for key, value in key_reader:
            mapping[key] = value

class AwsSecurityContext(SecurityContext):
    """A Security Context for AWS services.
    """
    ACCESS_KEY = 'AWSAccessKeyId'
    SECRET_KEY = 'AWSSecretKey'
    AWS_KEYS = {ACCESS_KEY: None, SECRET_KEY: None}
    KEY_FILE = None

    def __init__(self):
        if not self.KEY_FILE:
            self.KEY_FILE = os.path.join(os.environ['HOME'],
                                         '.ssh/rootkey.csv')

        read_keyfile(self.KEY_FILE, self.AWS_KEYS)
        self.access_key_id = self.AWS_KEYS[self.ACCESS_KEY]
        self.secret_access_key = self.AWS_KEYS[self.SECRET_KEY]


