#!/usr/bin/python
"""A Connection module.
"""

# Open-Source/Free Imports
import os

from boto3.session import Session

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
    region = 'us-west-1'
    def __int__(self):
        super(AwsConnection, self).__init__()

    def connect(self):
        """Master connect initiation.
        """
        self.sesh = Session(self.access_key_id,
                            self.secret_access_key,
                            'us-west-1')
        # self._emr_connect()
        self._s3_connect()


    def _emr_connect(self):
        """Connect to emr.
        """
        self.emr_conn = EmrConnection(aws_access_key_id=self.access_key_id,
                                      aws_secret_access_key=self.secret_access_key)
    def _s3_connect(self):
        """Connect to S3
        """
        self.s3_conn = S3Connection(aws_access_key_id=self.access_key_id,
                                    aws_secret_access_key=self.secret_access_key)


