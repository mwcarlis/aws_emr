#!/usr/bin/python
"""A simple Cluster job runner.
"""

# Open-Source/Free Imports
import subprocess
import boto3

import datetime
from boto.s3.key import Key
from boto.emr.step import StreamingStep
from boto.emr.instance_group import InstanceGroup

# Private-IP Imports Carlis/Koumis.
from cluster_iface.connection import AwsConnection
from cluster_iface.configuration import AwsConfiguration

class JobRunner(object):
    """An abstract job runner object..
    """
    def __init__(self):
        raise Exception("UnImplemented")

class AwsJobRunner(AwsConnection, JobRunner):
    """An amazon job runner object.
    """

    def __init__(self):
        AwsConnection.__init__(self)
        #super(AwsJobRunner, self).__init__()
        self.steps = []
        self.keys = {}
        self.connect()

    def get_storage(self, name):
        """Get a reference to a AWS S3 bucket.
        """
        self.bucket = self.s3_conn.get_bucket(name)

    def key_from_file(self, key, fname):
        """Create an AWS s3 resource from fname.
        """
        new_key = Key(self.bucket)
        self.keys[key] = new_key
        with open(fname, 'r') as file_d:
            size_stored = key.set_contents_from_file(file_d)
        return size_stored

    def string_from_key(self, key):
        """Turn an AWS s3 resource into a str.
        """
        if key in self.keys:
            interest_key = self.keys[key]
        else:
            interest_key = bucket.get_key(key)
        if not interest_key:
            # We failed to get the bucket from S3.
            return interest_key
        data = interest_key.get_contents_as_string()
        print data
        return data

    def stream_steps(self, name, mapper, reducer, d_in, d_out):
        """A method to initialize the Streaming JobFlow Steps.
        """
        self.step = StreamingStep(name=name,
                                  mapper=mapper,
                                  reducer=reducer,
                                  input=d_in,
                                  output=d_out)

    def init_job_flows(self, name, log_uri):
        """A method to begin the job flow.
        """
        self.job_id = self.emr_conn.run_jobflow(name=name,
                                                log_uri=log_uri,
                                                #availability_zone='us-west-1#$a',
                                                ec2_keyname='key_pair',
                                                master_instance_type='m1.small',
                                                num_instances=1,
                                                action_on_failure='CONTINUE',
                                                job_flow_role="EMR_EC2_DefaultRole",
                                                service_role="EMR_DefaultRole",
                                                enable_debugging=True,
                                                steps=[self.step])

    def terminate_the_connections(self):
        # self.conn
        pass

if __name__ == '__main__':
    # import time
    # job_run = AwsJobRunner()
    aws_conf = AwsConfiguration()
    #print subprocess.check_output(['python', 'mr_job.py', '-r', 'emr',
    #                              'input/data_18.txt', '--output-dir=s3://facedata/testout/'])


