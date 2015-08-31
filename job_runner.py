#!/usr/bin/python
"""A simple Cluster job runner.
"""

# Open-Source/Free Imports
from boto.s3.key import Key
from boto.emr.step import StreamingStep

# Private-IP Imports Carlis/Koumis.
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
        self.steps = []
        self.keys = {}
        self.emr_connect()
        self.s3_connect()

    def get_storage(self, name):
        self.bucket = self.s3_conn.get_bucket(name)

    def key_from_file(self, key, fname):
        new_key = Key(self.bucket)
        self.keys[key] = new_key
        with open(fname, 'r') as file_d:
            size_stored = key.set_contents_from_file(fname)
        return size_stored

    def string_from_key(self, key):
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
        self.steps.append(StreamingStep(name=name,
                                        mapper=mapper,
                                        reducer=reducer,
                                        input=d_in,
                                        output=d_out))

    def init_job_flows(self, name, log_uri):
        """A method to begin the job flow.
        """
        print self.steps
        print '\n'
        self.job_id = self.emr_conn.run_jobflow(name=name,
                                                log_uri=log_uri,
                                                steps=self.steps)

    def terminate_the_connections(self):
        # self.conn
        pass

if __name__ == '__main__':
    job_run = AwsJobRunner()
    job_run.stream_steps('My wordcount example',
                         's3n://facedata/wordSplitter.py',
                         'aggregate',
                         's3n://facedata/word_18',
                         's3n://facedata/output')

    job_run.init_job_flows('My Jobflow',
                           's3n://facedata/logs/')
    print job_run.emr_conn



