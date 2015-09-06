"""A mrjob mapreduce wordcount example using EMR HDFS.
"""
import re

from mrjob.job import MRJob

#from cluster_iface.security_context import AwsSecurityContext
#from cluster_iface.configuration import AwsConfiguration

WORD_RE = re.compile(r'[\w]+')
# AWS_SEC = AwsSecurityContext()
# AWS_CONF = AwsConfiguration()

class MRWordFreqCount(MRJob):
    """A HDFS word count interface.
    """
    def mapper(self, _, line):
        """A wordcount mapper.
        """
        for word in WORD_RE.findall(line):
            yield word.lower(), 1

    def combiner(self, word, counts):
        """A wordcount combiner.
        """
        yield word, sum(counts)

    def reducer(self, word, counts):
        """A wordcount reducer.
        """
        yield word, sum(counts)

if __name__ == '__main__':
    MRWordFreqCount.run()


