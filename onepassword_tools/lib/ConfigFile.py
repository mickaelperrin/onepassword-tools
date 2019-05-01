import yaml
import os


class ConfigFile:

    path: str
    config: {} = {}

    def __init__(self):
        self.path = self.get_path()
        if os.path.isfile(self.path):
            with open(self.path, 'r') as ymlconfig:
                self.config = yaml.load(ymlconfig, yaml.SafeLoader)

    def config_key_exists(self, *keys):
        return self.keys_exists(self.config, *keys)

    @staticmethod
    def get_path():
        return os.path.expandvars(os.path.join('$HOME', '.onepassword-tools.yml'))

    def get_section(self, section):
        if section in self.config.keys():
            return self.config[section]
        return None

    @staticmethod
    def keys_exists(element, *keys):
        if type(element) is not dict:
            return False
        if len(keys) == 0:
            return False

        _element = element
        for key in keys:
            try:
                _element = _element[key]
            except KeyError:
                return False
        return True
