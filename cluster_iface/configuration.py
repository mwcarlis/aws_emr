"""A configuration module.
"""
import os
import yaml

from security_context import AwsSecurityContext

class Configuration(object):
    """Abstract Configuration class.
    """
    def __init__(self):
        pass


##  Possible opencv library dependancies.
#'sudo apt-get install -y cmake libgtk2.0-dev pkg-config libavcodec-dev libavformat-devlibswscale-dev libamd2.2.0 libblas3gf libc6 libgcc1 libgfortran3 liblapack3gf libumfpack5.4.0 libstdc++6 build-essential gfortran libatlas-dev libatlas3-base libblas-dev liblapack-dev libjpeg-dev libpng-dev libtiff-devlibjasper-dev'

class AwsConfiguration(Configuration):
    """An AwsConfiguration for environment configuration control.
    """
    AWS_SEC = AwsSecurityContext()
    CONFIG_FILE = '.mrjob.conf'
    PEM_KEYS = '.ssh/key_pair.pem'
    CONFIGURATIONS = {
        'runners': {
            'emr': {
                # 'aws-region': 'us-east-1',
                ##### Cost Factors #####
                'num_ec2_instances': 1,
                'ec2_core_instance_type': 'm1.small',
                'max_hours_idle': 1,
                'mins_to_end_of_hour': 10,
                'pool_emr_job_flows': True,
                # 'pool_name': '',

                ##### Security Factors #####
                'ec2_key_pair': 'key_pair',
                'ec2_key_pair_file': os.path.join(AWS_SEC.HOME, PEM_KEYS),

                ##### Other #####
                'label': 'mcmc_konix',
                'ssh_tunnel_to_job_tracker': True,
                'bootstrap': [
                    # Update the apt-repo/OS/libraries.
                    'sudo apt-get -y update',
                    #'sudo apt-get -y upgrade',

                    # Switch to Python 2.7.10
                    #'curl -kL https://raw.github.com/utahta/pythonbrew/master/pythonbrew-install | bash',
                    #'. $HOME/.pythonbrew/etc/bashrc',
                    #'pythonbrew install 2.7.10',
                    #'pythonbrew switch 2.7.10',

                    # Get common python libraries.
                    # python2.7-dev is missing something. Do we need it?
                    #'sudo apt-get install -y python2.7-dev',
                    'sudo apt-get install -y python-pip',
                    'sudo pip install numpy',
                    'sudo apt-get install -y python-opencv'
                ]
                # 'python_archives': None
            },
            'inline': {
                'base_tmp_dir': os.path.join(AWS_SEC.HOME, '.tmp')
            }
        }
    }
    if 'matt' not in os.path.basename(AWS_SEC.HOME):
        # If it's not matt it's alex. Hopefully.
        CONFIGURATIONS['runners']['emr']['owner'] = 'konixmusic'

    # The configured/formatted string resrouce.
    mrjob_conf = ''

    def __init__(self):
        self.conf_file = os.path.join(self.AWS_SEC.HOME, self.CONFIG_FILE)
        if not self.mrjob_conf:
            # We haven't config'd env b/c don't have the config'd format string.
            self.mrjob_conf = self._install_config(self.CONFIGURATIONS)
        # Control the environment.
        self._master_config_ctrlr()

    def _install_config(self, config):
        """Dump the config file.
        """
        return yaml.dump(config, default_flow_style=False)

    def _master_config_ctrlr(self):
        """Master environment config controller.
        """
        self._setenv_mrjob_config()
        self._setenv_aws_config()

    def _setenv_aws_config(self):
        """AWS uses a hidden directory with config files.
        """
        aws_hdir = '.aws'
        conf_file = 'config'
        cred_file = 'credentials'
        acc_kid = 'aws_access_key_id'
        sec_kid = 'aws_secret_access_key'

        aws_path = os.path.join(self.AWS_SEC.HOME, aws_hdir)
        if not os.path.isdir(aws_path):
            # We cant modify files in an dir that doesn't exist.
            os.mkdir(aws_path)

        aws_conf = os.path.join(aws_path, conf_file)
        if not os.path.isfile(aws_conf):
            # If the conf file doesn't exist write to it.
            conf = '[default]\nregion = us-east-1\n'
            with open(aws_conf, 'w+') as file_d:
                file_d.write(conf)

        aws_cred = os.path.join(aws_path, cred_file)
        if not os.path.isfile(aws_cred):
            # If the cred file doesn't exist write to it.
            cred = '[default]\n{} = {}\n{} = {}\n'
            data = cred.format(acc_kid,
                               self.AWS_SEC.access_key_id,
                               sec_kid,
                               self.AWS_SEC.secret_access_key)
            with open(aws_cred, 'w+') as file_d:
                file_d.write(data)

    def _setenv_mrjob_config(self):
        """Write the mrjob configuration file.
        """
        if not os.path.isfile(self.conf_file):
            # If it doesn't exist write it.
            with open(self.conf_file, 'w') as file_d:
                file_d.write(self.mrjob_conf)
        else:
            with open(self.conf_file, 'w+') as file_d:
                config = file_d.read()
                if config != self.conf_file:
                    # If it exists, but outdated, write the new config.
                    file_d.write(self.mrjob_conf)


if __name__ == '__main__':
    AWS_CONF = AwsConfiguration()


