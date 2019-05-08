from onepassword_tools.lib.OnePasswordUtils import OnePasswordUtils
from onepassword_tools.lib.OnePasswordSSHKeyItem import OnePasswordSSHKeyItem
from onepassword_tools.lib.OnePasswordResult import OnePasswordResult
from onepassword_local_search.OnePassword import OnePassword
from onepassword_tools.lib.MiscUtils import generate_password
from onepassword_tools.lib.ClickUtils import ClickUtils
from onepassword_tools.lib.ConfigFile import ConfigFile
from getpass import getuser
from socket import gethostname
from onepassword_tools.lib.Crypto import generate_ssh_key
import click
import sys
import json


def get_defaults():
    _defaults = {}
    config_file = ConfigFile()
    if '.' in __name__:
        command_name = __name__.rsplit('.', 1)[1]
    else:
        command_name = __name__
    command_config = config_file.get_section(command_name)

    # Grab from-host default value from config file or fallback to hostname
    if config_file.keys_exists(command_config, 'defaults', 'from-host'):
        _defaults['from-host'] = command_config['defaults']['from-host']
    else:
        _defaults['from-host'] = gethostname().encode('ascii', 'ignore').decode('ascii')

    # Grab from-user default value from config or fallback to current user name
    if config_file.keys_exists(command_config, 'defaults', 'from-user'):
        _defaults['from-user'] = command_config['defaults']['from-user']
    else:
        _defaults['from-user'] = getuser()
    return _defaults


defaults = get_defaults()


@click.command()
@click.option('--from-host', help='Host from where the SSH connection starts, default current hostname.', prompt=True, default=defaults['from-host'])
@click.option('--from-user', help='User who is responsible from initiating the connection, default current user.', prompt=True, default=defaults['from-user'])
@click.option('--to-host', help='Remote server hostname, prompted if empty.', prompt=True, required=True)
@click.option('--to-user', help='Remote user, prompted if empty.', prompt=True, required=True)
@click.option('--to-host-abbreviated', help='Alias of the remote server hostname used to initialize connection.', required=False)
@click.option('--no-passphrase', help='Create ssh key without passphrase.', prompt=False, required=False, default=False)
@click.option('--passphrase', help='Use this passphrase instead of an autogenerated one.')
@click.option('--passphrase-length', help='Length of the autogenerated passphrase.', default=50, type=int)
@click.option('--port', help='Remote port', required=False, default=22, type=int)
@click.option('--vault', help='1Password vault uuid where to store the SSH key', required=False, default=None)
@click.option('--return-field', required=False, help='Field value to return', default=None)
def new_ssh_key(from_user, from_host, to_user, to_host, passphrase, passphrase_length, vault, port,
                to_host_abbreviated, no_passphrase, return_field):
    """Generates a new SSH key and store it in 1Password. Additional information are stored also to generate SSH config
    file when imported."""
    NewSSHKey(**locals()).run()


class NewSSHKey:

    entryTitleTemplate = 'id_rsa.from__%s@%s__to__%s@%s'
    from_user: str = None
    from_host: str = None
    no_passphrase: bool = None
    onePassword: OnePassword
    onePasswordUtils: OnePasswordUtils
    passphrase: str = None
    passphrase_length: int = None
    port: str = None
    return_field: str = None
    tags = ['Clef SSH']
    title: str = None
    to_user: str = None
    to_host: str = None
    to_host_abbreviated: str = None
    vault: str = None

    def __init__(self, **kwargs):
        self._init(**kwargs)
        self.onePasswordUtils = OnePasswordUtils()
        self.onePassword = OnePassword()
        if not self.no_passphrase and not self.passphrase:
            self.passphrase = generate_password(self.passphrase_length)
        self.title = self.get_title(self.from_user, self.from_host, self.to_user, self.to_host)

    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)

    def _init(self, **kwargs):
        for key, value in kwargs.items():
            self[key] = value

    @staticmethod
    def get_title(from_user, from_host, to_user, to_host):
        return NewSSHKey.entryTitleTemplate % (from_user, from_host, to_user, to_host)

    def run(self):
        if not self.onePasswordUtils.is_authenticated():
            self.onePasswordUtils.authenticate()

        public_key, private_key = generate_ssh_key(passphrase=self.passphrase)
        public_key += " %s" % self.title

        item = self.save_on_1password(public_key=public_key, private_key=private_key)
        if 'uuid' in item.keys():
            result = ''
            if self.return_field is None:
                print(json.dumps(item))
            else:
                if self.return_field in item.keys():
                    result = item[self.return_field]
                else:
                    result = OnePasswordResult(dict(details=item['request_object'])).get(self.return_field)
            print(result)
            sys.exit(0)
        else:
            ClickUtils.error('Unable to save entry in 1Password')
            sys.exit(1)

    def save_on_1password(self, public_key, private_key):
        arguments = vars(self)
        arguments['public_key'] = public_key
        arguments['private_key'] = private_key
        ssh_key_item = OnePasswordSSHKeyItem(**arguments)
        request_object = ssh_key_item.get_request_object()
        title = ssh_key_item.get_title()
        return self.onePasswordUtils.create_item(
            request_object=request_object,
            tags=self.tags,
            template=ssh_key_item.item_type,
            title=title,
            vault=self.vault
        )
