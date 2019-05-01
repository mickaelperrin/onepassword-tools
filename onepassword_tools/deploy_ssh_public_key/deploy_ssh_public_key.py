import click
import pexpect
import tempfile

from onepassword_tools.lib.OnePasswordUtils import OnePasswordUtils
from onepassword_local_search.OnePassword import OnePassword
from onepassword_tools.new_ssh_key.new_ssh_key import get_defaults, NewSSHKey
from onepassword_tools.lib.Log import Log

defaults = get_defaults()


@click.command()
@click.option('--uuid', prompt=True, required=True)
def deploy_ssh_public_key(uuid):
    DeploySSHPublicKey(**locals()).run()


class DeploySSHPublicKey:
    uuid: str = None
    port: str = None
    admin: str = None
    publicKeyField: str = 'Public Key'

    def __init__(self, **kwargs):
        self.onePasswordUtils = OnePasswordUtils()
        self.onePassword = OnePassword()
        self._init(**kwargs)

    def __setitem__(self, key, value):
        if hasattr(self, key):
            setattr(self, key, value)

    def _init(self, **kwargs):
        for key, value in kwargs.items():
            self[key] = value

    def ssh_copy_id(self, item):
        key_file = tempfile.NamedTemporaryFile()
        key_file.write(item.get(self.publicKeyField).encode('ascii'))
        key_file.flush()
        key_file_path = key_file.name

        user = item.get('to_user')

        pass

    def run(self):
        ssh_key_item = self.onePassword.get(self.uuid)
        if not self.admin:
            self.ssh_copy_id(ssh_key_item)


