from security_context import SecurityContext, AwsSecurityContext
from boto.emr.connection import EmrConnection


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
    def connect(self):
        self.emr_conn = EmrConnection(self.access_key_id,
                                      self.secret_access_key)



