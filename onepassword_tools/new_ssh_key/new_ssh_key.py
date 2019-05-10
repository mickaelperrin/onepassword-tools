from onepassword_tools.lib.OnePasswordSSHKeyItem import OnePasswordSSHKeyItem
from onepassword_tools.lib.NewItemCommand import NewItemCommand, new_item_command_options, new_item_command_password
from onepassword_tools.lib.MiscUtils import generate_password
from onepassword_tools.lib.Crypto import generate_ssh_key
from onepassword_tools.lib.ConfigFile import ConfigFile
from getpass import getuser
from socket import gethostname
import click


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
@new_item_command_options
@click.option('--from-user', help='User who is responsible from initiating the connection, default current user.', prompt=True, default=defaults['from-user'])
@click.option('--from-host', help='Host from where the SSH connection starts, default current hostname.', prompt=True, default=defaults['from-host'])
@click.option('--to-user', help='Remote user, prompted if empty.', prompt=True, required=True)
@click.option('--to-host', help='Remote server hostname, prompted if empty.', prompt=True, required=True)
@click.option('--to-host-abbreviated', help='Alias of the remote server hostname used to initialize connection.', required=False)
@click.option('--no-passphrase', help='Create ssh key without passphrase.', prompt=False, required=False, default=False, is_flag=True)
@click.option('--passphrase', help='Use this passphrase instead of an autogenerated one.')
@click.option('--passphrase-length', help='Length of the autogenerated passphrase.', default=50, type=int)
@click.option('--port', help='Remote port', required=False, default=22, type=int)
def new_ssh_key(from_user, from_host, to_user, to_host, to_host_abbreviated, no_passphrase, passphrase, passphrase_length,
                port, account, notes, return_field, title, vault, do_not_ask_credentials):
    """Generates a new SSH key and store it in 1Password. Additional information are stored also to generate SSH config
    file when imported."""
    NewSSHKey(**locals()).run()


class NewSSHKey(NewItemCommand):

    database: str = None
    from_user: str = None
    from_host: str = None
    no_passphrase: bool = None
    onePasswordItemClass = OnePasswordSSHKeyItem
    passphrase: str = None
    passphrase_length: int = None
    port: str = None
    public_key: str
    private_ey: str
    tags = ['Clef SSH']
    titleTemplate = 'id_rsa.from__{from_user}@{from_host}__to__{to_user}@{to_host}'
    to_user: str = None
    to_host: str = None
    to_host_abbreviated: str = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.no_passphrase and not self.passphrase:
            self.passphrase = generate_password(self.passphrase_length)
        self.public_key, self.private_key = generate_ssh_key(passphrase=self.passphrase)
        self.public_key += " %s" % self.get_title()
