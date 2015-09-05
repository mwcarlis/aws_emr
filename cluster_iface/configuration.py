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
        self._write_mrjob_config()
        self._write_aws_config()

    def _write_aws_config(self):
        aws_path = os.path.join(self.AWS_SEC.HOME, '.aws')
        if not os.path.isdir(aws_path):
            os.mkdir(aws_path)

        aws_conf = os.path.join(aws_path, 'config')
        if not os.path.isfile(aws_conf):
            conf = '[default]\nregion = us-east-1\n'
            with open(aws_conf, 'w+') as file_d:
                file_d.write(conf)

        aws_cred = os.path.join(aws_path, 'credentials')
        if not os.path.isfile(aws_cred):
            cred = '[default]\n{} = {}\n{} = {}\n'
            acc_kid = 'aws_access_key_id'
            sec_kid = 'aws_secret_access_key'
            data = cred.format(acc_kid,
                               self.AWS_SEC.access_key_id,
                               sec_kid,
                               self.AWS_SEC.secret_access_key)
            with open(aws_cred, 'w+') as file_d:
                file_d.write(data)


    def _write_mrjob_config(self):
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


