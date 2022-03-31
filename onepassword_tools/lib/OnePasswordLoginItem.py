from onepassword_tools.lib.OnePasswordItem import OnePasswordItem


class OnePasswordLoginItem(OnePasswordItem):

    item_type: str = 'LOGIN'
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
            "sections": [],
            "category": "LOGIN",
            "fields": [
                {
                    "id": "username",
                    "type": "STRING",
                    "purpose": "USERNAME",
                    "label": "username",
                    "value": self.username
                },
                {
                    "id": "password",
                    "type": "CONCEALED",
                    "purpose": "PASSWORD",
                    "label": "password",
                    "password_details": {
                        "strength": "TERRIBLE"
                    },
                    "value": self.password
                },
                {
                    "id": "notesPlain",
                    "type": "STRING",
                    "purpose": "NOTES",
                    "label": "notesPlain",
                    "value": self.get('notes')
                }
            ]
        }
