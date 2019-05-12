from onepassword_tools.lib.Log import Log
from onepassword_tools.lib.OnePasswordUtils import OnePasswordUtils
from onepassword_tools.lib.ClickUtils import ClickUtils
from onepassword_local_search.OnePassword import OnePassword
from onepassword_local_search.models.Item import Item
from plumbum import local
from string import Template
import click
import pexpect
import sys
import os
import textwrap


@click.command()
@click.argument('search', required=False, default=None)
@click.option('-D', help='cleanup ssh agent and remove all 1Password managed keys and configuration', is_flag=True)
@click.option('--no-ssh-config', help='Do not create ssh config file', default=False)
def ssh_add(search, d, no_ssh_config):
    """Loads a SSH key stored in 1Password by searching [SEARCH] in uuid or in item title, and creates a ssh
    configuration file of the following format:

    Match originalhost <Hostname>,<IP>,<Alias> user <Remote user>\n
      IdentitiesOnly yes\n
      IdentityFile <path to key file>\n
      Hostname <Hostname>\n
      User <Remote user>\n
      Port <Port>
    """
    if d:
        SSHAdd().cleanup()
    else:
        if not search:
            Log.error('Error: Missing argument "SEARCH".')
            sys.exit(1)
        SSHAdd(no_ssh_config=no_ssh_config).add(search)


sshadd = local['ssh-add']


class SSHAdd:

    item: Item
    keyFilePath: str
    keyStoragePath: str
    no_ssh_config: bool
    onePassword: OnePassword
    onePasswordUtils: OnePasswordUtils
    passPhrase: str
    privateKey: {}
    publicKey: {}
    sessionKey: str
    sshConfigFilePath: str
    sshConfigStoragePath: str
    suggestions: [] = []
    title: str

    def __init__(self, no_ssh_config=False):
        self.onePasswordUtils = OnePasswordUtils()
        self.onePassword = OnePassword()
        self.keyStoragePath = os.path.expandvars(os.path.join('$HOME', '.ssh', 'keys.1password.d'))
        self.sshConfigStoragePath = os.path.expandvars(os.path.join('$HOME', '.ssh', 'config.1password.d'))
        self.init_path(self.keyStoragePath)
        self.init_path(self.sshConfigStoragePath)
        self.no_ssh_config = no_ssh_config

    def _get_ssh_config_match_original_host(self):
        hosts = [ self.item.get('Hostname', strict=False) ]
        alias = self.item.get('Alias', strict=False)
        if alias:
            hosts.append(alias)
        ip = self.item.get('IP', strict=False)
        if ip:
            hosts.append(ip)
        return 'originalhost %s' % ','.join(hosts)

    def _get_ssh_config_match_user(self):
        to_user = self.item.get('Remote user', strict=False)
        if to_user:
            if os.environ.get('USER') == to_user:
                return ''
            else:
                return 'user %s' % to_user
        return ''

    def add(self, search):

        if not self.onePasswordUtils.is_authenticated(check_mode='local'):
            self.onePasswordUtils.authenticate()

        item = self.onePasswordUtils.try_to_grab_item(search)
        if isinstance(item, list):
            items = item
            if len(items) > 0:
                import inquirer
                choices = [
                    inquirer.List('results', message='Which key do you want ?', choices=['%s %s' % (key.uuid, key.overview['title']) for key in items])
                ]
                uuid = inquirer.prompt(choices)['results'].split(' ')[0]
                item = self.onePassword.get(uuid, output=False)
                if item is None:
                    ClickUtils.error('Unable to find any item matching your selection')
                    sys.exit(1)
            else:
                ClickUtils.error('Unable to find any items matching your search')
                sys.exit(1)
        self.title = item.get('title')
        self.item = item

        if self.key_has_been_registered(self.title):
            ClickUtils.success('Key %s already registered.' % self.title)
            sys.exit(0)

        self.publicKey = self.get_public_key(item)
        self.privateKey = self.get_private_key(item)
        self.passPhrase = self.get_pass_phrase(item)
        self.register_ssh_key(self.privateKey, self.passPhrase, self.publicKey)

        if not self.no_ssh_config:
            self.create_ssh_config_file()

        if self.key_has_been_registered(self.title):
            ClickUtils.success('Key %s has been added to agent successfully.' % self.title)
            sys.exit(0)
        else:
            if os.path.isfile(self.keyFilePath):
                os.unlink(self.keyFilePath)
            if os.path.isfile(self.sshConfigStoragePath):
                os.unlink(self.sshConfigStoragePath)
            ClickUtils.error('Unable to add key %s to agent' % self.title)
            sys.exit(1)

    def cleanup(self):

        for file in os.scandir(self.sshConfigStoragePath):
            if file.name.endswith('.cfg'):
                os.unlink(file.path)

        for file in os.scandir(self.keyStoragePath):
            if file.name.endswith('.key'):
                os.unlink(file.path)

        sshadd['-D']()
        ClickUtils.success('All dynamic keys and SSH configurations have been removed.')

    def create_ssh_config_file(self):

        to_hostname = self.item.get('IP', strict=False)
        if to_hostname is None or to_hostname == '':
            to_hostname = self.item.get('Hostname', strict=False)

        config = textwrap.dedent(Template("""\
            #uuid: $uuid
            Match $original_host $user
              IdentitiesOnly yes
              IdentityFile $private_key_file_path
              Hostname $to_host""").substitute(
            uuid=self.item.get('uuid'),
            original_host=self._get_ssh_config_match_original_host(),
            private_key_file_path=self.keyFilePath,
            to_host=to_hostname,
            user=self._get_ssh_config_match_user()
        ))

        to_user = self.item.get('Remote user', strict=False)
        if to_user:
            config += '\n  User %s' % to_user

        port = self.item.get('port', strict=False)
        if port:
            config += '\n  Port %s' % port

        ssh_config_file_path = os.path.join(self.sshConfigStoragePath, self.title.replace('id_rsa.', '') + '.cfg')
        with open(ssh_config_file_path, 'w+') \
                as config_file:
            config_file.write(config)
            config_file.flush()
            os.chmod(config_file.name, 0o600)
            self.sshConfigFilePath = ssh_config_file_path

    @staticmethod
    def get_private_key(key):
        private_key = key.get('Private Key', strict=False)
        if private_key:
            return private_key
        ClickUtils.error('unable to get private key')
        sys.exit(1)

    @staticmethod
    def get_public_key(key):
        public_key = key.get('Public Key', strict=False)
        if public_key:
            return public_key
        ClickUtils.error('unable to get public key')
        sys.exit(1)

    @staticmethod
    def get_pass_phrase(key):
        passphrase = key.get('Passphrase', strict=False)
        if passphrase:
            return passphrase
        ClickUtils.error('unable to get passphrase')
        sys.exit(1)

    @staticmethod
    def init_path(path):
        path = os.path.expandvars(path)
        if not os.path.isdir(path):
            os.mkdir(path, 0o700)
        elif (os.stat(path).st_mode & 0o777) != 0o700:
            os.chmod(path, 0o700)

    @staticmethod
    def key_has_been_registered(name):
        registered_keys = sshadd('-l', retcode=None)
        return name.replace('id_rsa.', '') in registered_keys

    def register_ssh_key(self, private_key, passphrase, public_key):

        with open(os.path.join(self.keyStoragePath, self.title + '.key'), 'w+') as key_file:
            key_file.write(private_key)
            key_file.flush()
            self.keyFilePath = key_file.name
            os.chmod(self.keyFilePath, 0o600)

        with open(os.path.join(self.keyStoragePath, self.title + '.key.pub'), 'w+') as pub_file:
            pub_file.write(public_key)
            pub_file.flush()
            os.chmod(pub_file.name, 0o600)

        if passphrase:
            command = 'ssh-add %s' % self.keyFilePath
            bash = pexpect.spawn('bash', ['-c', command])
            bash.expect_exact('Enter passphrase')
            bash.sendline(passphrase)
            bash.expect_exact(pexpect.EOF)
        else:
            sshadd[self.keyFilePath]()

