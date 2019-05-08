from onepassword_tools.lib.ConfigFile import ConfigFile
import secrets
import string
from uuid import UUID


def generate_password(password_length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for i in range(password_length))


def is_uuid(uuid_string, version=4):
    try:
        uid = UUID(uuid_string, version=version)
        return uid.hex == uuid_string.replace('-', '')
    except ValueError:
        return False


def remove_null_value_keys_in_dict(data, only_keys=None):
    if only_keys is None:
        only_keys = ['v', 'value']
    new_data = {}
    for k, v in data.items():
        if isinstance(v, dict):
            v = remove_null_value_keys_in_dict(v)
        elif isinstance(v, list):
            clean_list = []
            for el in v:
                clean_list.append(remove_null_value_keys_in_dict(el))
            v = clean_list
        if k in only_keys and v in (u'', None, {}):
            continue
        new_data[k] = v
    return new_data


class SimpleFormatter(string.Formatter):

    def get_value(self, key, args, kwargs):
        return args[0].get(key)
