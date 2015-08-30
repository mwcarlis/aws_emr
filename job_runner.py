#!/usr/bin/python
"""A simple Cluster job runner.
"""

import os, sys, inspect
from cluster_iface.connection import AwsConnection

class JobRunner(object):
    """An abstract job runner object..
    """
    def __init__(self):
        raise Exception("UnImplemented")

class AwsJobRunner(AwsConnection, JobRunner):
    """An amazon job runner object.
    """
    def __init__(self):
        super(AwsJobRunner, self).__init__()
        self.connect()

if __name__ == '__main__':
    job_run = AwsJobRunner()
    print job_run.emr_conn

