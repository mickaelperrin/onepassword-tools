from onepassword_tools.lib.ClickUtils import ClickUtils
from onepassword_tools.lib.ConfigFile import ConfigFile
from onepassword_tools.lib.Log import Log
from onepassword_tools.lib.MiscUtils import is_uuid
import json
import os
import secrets
import string
import subprocess
import sys
if os.environ.get('USE_LOCAL'):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../../../onepassword-local-search")
from onepassword_local_search.models.Item import Item
from onepassword_local_search.OnePassword import OnePassword
from onepassword_local_search.exceptions.ManagedException import ManagedException
import re
import tempfile


class OnePasswordUtils:

    onePassword: OnePassword
    suggestions: [] = []

    def __init__(self):
        self.onePassword = OnePassword()
        self.config = ConfigFile()

    @staticmethod
    def _communicate(subproc, inputstr=None):
        """
        Encode the input given to the subprocess if any
        :param subproc:
        :param inputstr:
        :return: A tuple of (stdout, stderr)
        """
        if inputstr is None:
            return subproc.communicate()
        if not inputstr:
            inputstr = ''
        return subproc.communicate(inputstr.encode())

    def _authenticate(self, shorthand=''):
        """
        Authenticate over 1Password and register the session key in the environment variable
        :return: Nothing
        """
        try:

            sessionKey = subprocess.check_output([
                'op',
                'signin',
                '--account', self.onePassword.configFileService.get_account_uuid_from_account_shorthand(shorthand),
                '--raw'
            ]) \
                .decode('utf-8') \
                .replace('\n', '')
            os.environ[
                'OP_SESSION_' + self.onePassword.configFileService.get_user_uuid_from_account_shorthand(shorthand)
            ] = sessionKey

        except subprocess.CalledProcessError:
            ClickUtils.error('Failed to authenticate. You may have written the wrong password ?')
            sys.exit(1)

    def authenticate(self, shorthand=None):
        if shorthand is None:
            shorthands = self.config.get_section('accounts')
            if len(shorthands) > 0:
                for shorthand in shorthands:
                    self._authenticate(shorthand)
            else:
                self._authenticate(self.onePassword.configFileService.get_latest_signin())
        else:
            self._authenticate(shorthand)
        self.onePassword.accountService.init()

    def create_item(self, request_object, category, title, tags=None, url='', vault='', account=''):
        if tags is None:
            tags = []
        try:
            Log.debug(request_object, 'request data')
            data = json.dumps(request_object)
            with tempfile.NamedTemporaryFile() as requestFile:
                requestFile.write(data.encode('utf-8'))
                requestFile.seek(0)

                command = 'item create --no-color --format json'
                if title and title != '':
                    command += ' --title="%s"' % title
                if type(tags).__name__ != 'list':
                    tags = [tags]
                if tags and len(tags) > 0:
                    command += ' --tags="%s"' % ','.join(tags)
                if vault and vault != '':
                    command += ' --vault="%s"' % vault
                if account and account != '':
                    command += ' --account=%s' % account

                Log.debug(command, 'op command : %s', command)
                rc, output, error = self.op_cli(command, inputfile=requestFile)
                requestFile.close()

                if output is not None and len(output) > 1:
                    created_item = json.loads(output.replace('\n', ''))
                    if not created_item.get('id'):
                        Log.error(error)
                        raise Exception("Error while creating onepassword entry")
                    else:
                        created_item['request_object'] = request_object
                        Log.debug(created_item)
                        return created_item
                else:
                    Log.error(error)
                    raise Exception("Error while creating onepassword entry")

        except Exception:
            if requestFile:
                requestFile.close()
            raise Exception("Error while creating onepassword entry")

    def is_authenticated(self, account=None, check_mode=None) -> bool:
        """
        Check if we are authenticated over 1Password by decrypting local keys
        and trying to grab a template remotely
        :return: bool
        """
        if check_mode is None or check_mode == 'local':
            if not self.onePassword.is_authenticated():
                return False

        if check_mode is None or check_mode == 'remote':
            if account is None:
                accounts = self.config.get_section('accounts')
                if len(accounts) > 0:
                    for account_ in accounts:
                        if not self.op_cli('account get --account="%s"' % account_)[0] == 0:
                            return False
                else:
                    if not self.op_cli('account get')[0] == 0:
                        return False
            else:
                if not self.op_cli('account get --account="%s"' % account)[0] == 0:
                    return False
        return True

    def generate_op_field_uuid(self):
        return self.generate_op_uuid(26)

    def generate_op_section_uuid(self):
        return self.generate_op_uuid(29)

    @staticmethod
    def generate_op_uuid(length=26):
        return ''.join(secrets.choice(string.ascii_lowercase) for _ in range(length))

    def get_alias(self, search):
        """
        Search if the input string is aliases to an uuid in the config file
        :param search:
        :return:
        """
        if self.config.config_key_exists('aliases', search):
            return self.config.config['aliases'][search]
        else:
            return search

    def op_cli(self, cmd, inputstr=None, inputfile=None):
        """
        Call the 1Password cli (op)
        :param cmd: the op arguments and options
        :param inputstr: the input given to the command
        :return: A tuple of (returncode, stdout, stderr)
        """
        e = os.environ.copy()
        p = subprocess.Popen('op ' + cmd,
                             bufsize=0,
                             close_fds=True,
                             env=e,
                             shell=True,
                             stdin=inputfile or subprocess.PIPE,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE
                             )
        try:
            out, err = self._communicate(p, inputstr=inputstr)
        except subprocess.CalledProcessError:
            out = ''
            err = ''
        rc = p.returncode
        return rc, out.decode('utf-8'), err.decode('utf-8')

    def search_item_uuid_by_title(self, search, search_operator='AND'):
        """
        Search an item by title
        :param search:
        :return: Item if only one match, None either
        """
        items = self.onePassword.get_items(search, search_operator)
        if len(items) == 1:
            return self.onePassword.get(items[0].uuid, output=False)
        else:
            return items

    def try_to_grab_item(self, search, search_operator='AND') -> Item:
        """
        First try to grab by using 1Password or custom UUID, then fallback to
        search item by title.
        :param search:
        :return: Item or None
        """
        if search[0] != self.get_alias(search[0]):
            search = [self.get_alias(search[0])]
        try:
            item = self.onePassword.get(search[0], output=False)
        except ManagedException:
            item = self.search_item_uuid_by_title(search, search_operator)
        return item
