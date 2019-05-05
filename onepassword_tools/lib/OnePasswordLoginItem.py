from onepassword_tools.lib.OnePasswordItem import OnePasswordItem


class OnePasswordLoginItem(OnePasswordItem):

    item_type: str = 'Login'
    notes: str = None
    password: str = None
    tags: [] = ['Compte utilisateur']
    url: str = None
    username: str = None

    def __getitem__(self, item):
        return super().__getitem__(item)

    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            if hasattr(self, key):
                self.__setattr__(key, value)

    def _request_object(self):
        """
        Return the dict object with the request sent to 1Password
        :return: dict
        """
        return {
            "notesPlain": self.get('notes'),
            "sections": [],
            "fields": [
                {
                    "value": self.username,
                    "name": "username",
                    "type": "T",
                    "designation": "username"
                },
                {
                    "value": self.password,
                    "name": "password",
                    "type": "P",
                    "designation": "password"
                }
            ]
        }

