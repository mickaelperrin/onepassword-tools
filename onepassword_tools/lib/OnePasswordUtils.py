from onepassword_tools.lib.ClickUtils import ClickUtils
import os
if os.environ.get('USE_LOCAL'):
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../../../onepassword-local-search")
from onepassword_local_search.OnePassword import OnePassword
from argparse import Namespace
import subprocess
import sys


class OnePasswordUtils:
    latestSignin: str
    onePassword: OnePassword
    sessionKey: str

    def __init__(self):
        self.onePassword = OnePassword(Namespace())

    def is_authenticated(self) -> bool:
        try:
            self.onePassword.is_authenticated()
            return True
        except:
            ClickUtils.error('You are not authenticated.')
            return False

    def authenticate(self):
        try:
            self.sessionKey = subprocess.check_output(['op', 'signin', '--output=raw'])\
                .decode('utf-8') \
                .replace('\n', '')
            self.latestSignin = self.onePassword.configFileService.get_latest_signin()
            os.environ.setdefault('OP_SESSION_' + self.latestSignin, self.sessionKey)
        except subprocess.CalledProcessError:
            ClickUtils.error('Failed to authenticate. You may have written the wrong password ?')
            sys.exit(1)
