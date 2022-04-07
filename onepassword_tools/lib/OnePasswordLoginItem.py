from onepassword_tools.lib.OnePasswordItem import OnePasswordItem
from urllib.parse import urlsplit,urlunsplit


class OnePasswordLoginItem(OnePasswordItem):

    item_type: str = 'LOGIN'
    notes: str = None
    password: str = None
    tags: [] = ['Compte utilisateur']
    url: str = None
    username: str = None
    tld_variations: str = None

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

        tld_variations = self.tld_variations.split(',')
        url_splitted = urlsplit(self.url)
        url_variations = [
            {
                "label": "",
                "primary": True,
                "href": self.url
            }
        ]

        for tld_variation in tld_variations:
            url_splitted_tld = url_splitted
            url_splitted_tld = url_splitted_tld._replace(netloc=url_splitted.hostname + '.' + tld_variation)
            url_variations.append(
                    {
                        "label": "",
                        "primary": False,
                        "href": urlunsplit(url_splitted_tld)
                    }
            )

        return {
            "sections": [],
            "urls": url_variations,
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
