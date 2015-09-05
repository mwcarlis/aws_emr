"""A configuration module.
"""
import os
import yaml

from security_context import AwsSecurityContext

class Configuration(object):
    """
    """
    def __init__(self):
        pass

class AwsConfiguration(Configuration):
    AWS_SEC = AwsSecurityContext()
    TABS = 2
    PEM_KEYS = '.ssh/key_pair.pem'
    CONFIGURATIONS = {
        'runners': {
            'emr': {
                'aws-region': 'us-east-1',
                'num_ec2_instances': 3,
                'ec2_core_instance_type': 'm1.small',
                'ec2_key_pair': 'key_pair',
                'ec2_key_pair_file': os.path.join(AWS_SEC.HOME, PEM_KEYS),
                'ssh_tunnel_to_job_tracker': True
                # 'python_archives': None
            },
            'inline': {
                'base_tmp_dir': os.path.join(AWS_SEC.HOME, '.tmp')
            }
        }
    }
    CONFIG_FILE = '.mrjob.conf'
    mrjob_conf = ''

    def __init__(self):
        self.conf_file = os.path.join(self.AWS_SEC.HOME, self.CONFIG_FILE)
        if not self.mrjob_conf:
            initiate = 0
            self.mrjob_conf = self._init_config(self.CONFIGURATIONS)
        self._write_config()

    def _init_config(self, config):
        """
        """
        return yaml.dump(config, default_flow_style=False)

    def _write_config(self):
        """
        """
        if not os.path.isfile(self.conf_file):
            # If it doesn't exist write it.
            with open(self.conf_file, 'w') as file_d:
                file_d.write(self.mrjob_conf)
        else:
            # If it does exist and is different write the new config.
            with open(self.conf_file, 'w+') as file_d:
                config = file_d.read()
                if config != self.conf_file:
                    # Write the new config.
                    file_d.write(self.mrjob_conf)


if __name__ == '__main__':
    AWS_CONF = AwsConfiguration()


