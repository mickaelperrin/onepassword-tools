import click
import copy
import json
import sys
from onepassword_tools.lib.OnePasswordUtils import OnePasswordUtils
from onepassword_local_search.OnePassword import OnePassword
from onepassword_tools.lib.MiscUtils import generate_password
from onepassword_tools.lib.MiscUtils import SimpleFormatter
from onepassword_tools.lib.OnePasswordResult import OnePasswordResult
from onepassword_tools.lib.ClickUtils import ClickUtils
from abc import ABCMeta, abstractmethod


def new_item_command_options(function):
    function = click.option('--notes', help='Note')(function)
    function = click.option('--title', help='Name of the 1Password item', default='')(function)
    function = click.option('--vault', help='Vault uuid where to store the information')(function)
    function = click.option('--account', help='Account to use (shorthand)')(function)
    function = click.option('--return-field', help='Field value to return', default=None)(function)
    return function


def new_item_command_password(function):
    function = click.option('--password', help='Password to use, default autogenerated')(function)
    function = click.option('--password-length', help='Autogenerated password length, default 25', default=25, type=int)(function)
    return function


class NewItemCommand:
    __metaclass__ = ABCMeta
    account: str = None
    notes: str = None
    onePassword: OnePassword
    onePasswordUtils: OnePasswordUtils
    password: str = None
    password_length: int = 25
    return_field: str = None
    title: str = None
    vault: str = None

    @property
    @abstractmethod
    def titleTemplate(self) -> str:
        pass

    @property
    @abstractmethod
    def onePasswordItemClass(self) -> str:
        pass

    def __init__(self, **kwargs):
        self.onePasswordUtils = OnePasswordUtils()
        self.onePassword = OnePassword()
        self._init(**kwargs)
        if self.password is None:
            self.password = generate_password(self.password_length)

    def _init(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def authenticate_if_needed(self):
        if not self.onePasswordUtils.is_authenticated():
            self.onePasswordUtils.authenticate()

    def get(self, attr):
        return getattr(self, attr)

    def save_on_1password(self, one_password_item_class):
        arguments = vars(copy.copy(self))
        del arguments['onePassword']
        del arguments['onePasswordUtils']
        server_item = one_password_item_class(**arguments)
        request_object = server_item.get_request_object()
        return self.onePasswordUtils.create_item(
            account=self.account,
            request_object=request_object,
            template=server_item.item_type,
            title=self.get_title(server_item),
            vault=self.vault
        )

    def get_title(self, item=None):
        template = self.titleTemplate if (self.title is None or self.title == '') else self.title
        if item is None:
            item = self
        sf = SimpleFormatter()
        return sf.format(template, item).strip()

    def run(self):

        self.authenticate_if_needed()

        item = self.save_on_1password(self.onePasswordItemClass)
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