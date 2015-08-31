#!/usr/bin/python
"""A Connection module.
"""

# Open-Source/Free Imports
from boto.emr.connection import EmrConnection
from boto.s3.connection import S3Connection

# Private-IP Imports Carlis/Koumis.
from security_context import SecurityContext, AwsSecurityContext

class Connection(SecurityContext):
    """Abstract Connection Object.
    """
    def __init__(self):
        raise Exception("UnImplemented")
    def connect(self):
        raise Exception("UnImplemented")

class AwsConnection(AwsSecurityContext, Connection):
    """AWS Connection Object.
    """
    def __int__(self):
        super(AwsConnection, self).__init__()
    def emr_connect(self):
        self.emr_conn = EmrConnection(self.access_key_id,
                                      self.secret_access_key)
    def s3_connect(self):
        self.s3_conn = S3Connection(self.access_key_id,
                                      self.secret_access_key)


