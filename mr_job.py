import re

from mrjob.job import MRJob

#from cluster_iface.security_context import AwsSecurityContext
#from cluster_iface.configuration import AwsConfiguration

WORD_RE = re.compile(r'[\w]+')
# AWS_SEC = AwsSecurityContext()
# AWS_CONF = AwsConfiguration()

class MRWordFreqCount(MRJob):
    def mapper(self, _, line):
        for word in WORD_RE.findall(line):
            yield word.lower(), 1

    def combiner(self, word, counts):
        yield word, sum(counts)

    def reducer(self, word, counts):
        yield word, sum(counts)

if __name__ == '__main__':
    MRWordFreqCount.run()


