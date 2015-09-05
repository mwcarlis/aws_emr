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
        pass


def read_external_keyfile(key_file, mapping):
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
        aws_acess_kenv = 'AWS_ACCESS_KEY_ID'
        aws_secret_kenv = 'AWS_SECRET_ACCESS_KEY'

        if not self.KEY_FILE:
            self._set_keyfile_path()
            read_external_keyfile(self.KEY_FILE, self.AWS_KEYS)
            self.access_key_id = self.AWS_KEYS[self.ACCESS_KEY]
            self.secret_access_key = self.AWS_KEYS[self.SECRET_KEY]

        # Maintain environmental variables.
        if not (os.getenv(aws_acess_kenv) and os.getenv(aws_secret_kenv)):
            os.environ[aws_acess_kenv] = self.AWS_KEYS[self.ACCESS_KEY]
            os.environ[aws_secret_kenv] = self.AWS_KEYS[self.SECRET_KEY]

    def _set_keyfile_path(self):
        """Set environmental variables.
        """
        if not self.KEY_FILE:
            self.HOME = os.environ['HOME']
            self.KEY_FILE = os.path.join(self.HOME,
                                         '.ssh/rootkey.csv')


