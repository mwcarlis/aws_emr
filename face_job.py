"""
"""

import re

from mrjob.job import MRJob

#from cluster_iface.security_context import AwsSecurityContext
#from cluster_iface.configuration import AwsConfiguration
# AWS_SEC = AwsSecurityContext()
# AWS_CONF = AwsConfiguration()

# Totally isn't a face_re.  More like a word_re
FACE_RE = re.compile(r'[\w]+')

class MRFaceTask(MRJob):
    """Do face tasks here.
    """
    def mapper(self, _, line):
        """Map out stuff.
        """
        for face in FACE_RE.findall(line):
            # face some stuff.
            yield face.lower(), 1

    def combiner(self, face, counts):
        """Combine something here.
        """
        yield face, sum(counts)

    def reducer(self, face, counts):
        """What do we do here?
        """
        yield face, sum(counts)

if __name__ == '__main__':
    """Do a Face Task
    """
    MRFaceTask.run()


