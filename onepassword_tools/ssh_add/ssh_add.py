import click
from onepassword_tools.lib.OnePasswordUtils import OnePasswordUtils
from onepassword_local_search.OnePassword import OnePassword
from argparse import Namespace
from os import environ, path
from onepassword_tools.lib.ClickUtils import ClickUtils
from onepassword_local_search.models.Item import Item
import sys
import pexpect
import tempfile
from plumbum import local


@click.command()
@click.argument('search')
def ssh_add(search):
    SSHAdd().run(search)


sshadd = local['ssh-add']


class SSHAdd:

    sessionKey: str
    onePasswordUtils: OnePasswordUtils
    onePassword: OnePassword
    suggestions: [] = []
    privateKey: {}
    passPhrase: str
    title: str

    def __init__(self):
        self.onePasswordUtils = OnePasswordUtils()
        self.onePassword = OnePassword(Namespace())

    def search_ssh_key_uuid_by_title(self, search):
        items = self.onePassword.get_items(search)
        if len(items) == 1:
            return self.onePassword.get(items[0].uuid, output=False)
        else:
            self.suggestions += items
            return None

    def try_to_grab_ssh_key(self, search) -> Item:
        try:
            # First try with uuid
            private_key = self.onePassword.get(search, output=False)
        except:
            try:
                # Then try with uuid mapping
                private_key = OnePassword(use_custom_uuid=True).get(search, output=False)
            except:
                # Fallback to search by title
                private_key = self.search_ssh_key_uuid_by_title(search)
                if not private_key:
                    # Fallback to specific title format
                    private_key = self.search_ssh_key_uuid_by_title('from_%s@pcp_to_%s@%s'
                                                               % (environ.get('USER'), environ.get('USER'), search))
        return private_key

    def get_private_key(self, key):
        try:
            privateKey = key.get('Private Key')
            return privateKey
        except:
            ClickUtils.error('unable to get private key')

    def get_pass_phrase(self, key):
        try:
            return key.get('Passphrase')
        except:
            ClickUtils.error('unable to get passphrase')

    def register_ssh_key(self, name, private_key, passphrase):
        key_file_path = None
        key_file = None

        if environ.get('KEY_STORAGE_PATH'):
            key_path = environ.get('KEY_STORAGE_PATH')
            if path.isdir(key_path) and path.isfile(path.join(key_path, name)):
                key_file_path = path.join(key_path, name)

        if not key_file_path and private_key:
            key_file = tempfile.NamedTemporaryFile()
            key_file.write(private_key.encode('ascii'))
            key_file.flush()
            key_file_path = key_file.name

        command = 'ssh-add %s' % key_file_path
        bash = pexpect.spawn('bash', ['-c', command])
        bash.expect_exact('Enter passphrase')
        bash.sendline(passphrase)
        bash.expect_exact(pexpect.EOF)

        if key_file:
            key_file.close()

    def ensure_key_has_been_registered(self, name):
        registered_keys = sshadd('-l')
        return name in registered_keys

    def run(self, search):
        if not self.onePasswordUtils.is_authenticated():
            self.onePasswordUtils.authenticate()
        private_key = self.try_to_grab_ssh_key(search)
        if private_key is None:
            if len(self.suggestions) > 0:
                ClickUtils.error('Unable to find proper match. Please refine your search')
                #TODO: use percol to select entry
                ClickUtils.info('Matching entries:')
                for suggestion in self.suggestions:
                    ClickUtils.info('%s %s' % (suggestion.uuid, suggestion.overview['title']))
            elif len(self.suggestions) == 0:
                ClickUtils.error('Unable to find any items matching your search')
            sys.exit(1)
        self.title = private_key.get('title')
        if self.ensure_key_has_been_registered(self.title):
            ClickUtils.success('Key %s already registered.' % self.title)
            sys.exit(0)
        self.privateKey = self.get_private_key(private_key)
        self.passPhrase = self.get_pass_phrase(private_key)
        self.register_ssh_key(self.title, self.privateKey, self.passPhrase)
        if self.ensure_key_has_been_registered(self.title):
            ClickUtils.success('Key %s has been added to agent successfully.' % self.title)
            sys.exit(0)
        else:
            ClickUtils.error('Unable to add key %s to agent' % self.title)
            sys.exit(1)




