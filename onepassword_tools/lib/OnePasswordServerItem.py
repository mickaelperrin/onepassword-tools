from onepassword_tools.lib.OnePasswordItem import OnePasswordItem


class OnePasswordServerItem(OnePasswordItem):

    hostname: str = None
    item_type: str = 'Server'
    notes: str = None
    password: str = None
    tags: [] = ['Compte utilisateur']
    url: str = None
    username: str = None

    def __getitem__(self, item):
        if item == 'url':
            return self._get_url()
        else:
            return super().__getitem__(item)

    def __init__(self, **kwargs):
        super().__init__()
        for key, value in kwargs.items():
            if hasattr(self, key):
                self.__setattr__(key, value)

    def _get_url(self):
        if self.username and self.hostname:
            return "ssh://%s@%s" % (self.username, self.hostname)
        elif self.hostname:
            return "ssh://%s" % self.hostname
        else:
            return None

    def _request_object(self):
        """
        Return the dict object with the request sent to 1Password
        :return: dict
        """
        return {
            "notesPlain": self.get('notes'),
            "sections": [
                {
                    "title": "",
                    "name": "Section_%s" % self.opu.generate_op_section_uuid(),
                    "fields": [
                        {
                            "inputTraits": {
                                "keyboard": "URL"
                            },
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "v": self.get('url'),
                            "t": "URL"
                        },
                        {
                            "inputTraits": {
                                "autocapitalization": "none",
                                "autocorrection": "no"
                            },
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "v": self.get('username'),
                            "t": "username"
                        },
                        {
                            "k": "concealed",
                            "n": self.opu.generate_op_field_uuid(),
                            "v": self.get('password'),
                            "t": "password"
                        }
                    ]
                },
                {
                    "title": "Admin Console",
                    "name": "Section_%s" % self.opu.generate_op_section_uuid(),
                    "fields": [
                        {
                            "inputTraits": {
                                "keyboard": "URL"
                            },
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "t": "admin console URL"
                        },
                        {
                            "inputTraits": {
                                "autocapitalization": "none",
                                "autocorrection": "no"
                            },
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "t": "admin console username"
                        },
                        {
                            "k": "concealed",
                            "n": self.opu.generate_op_field_uuid(),
                            "t": "console password"
                        }
                    ]
                },
                {
                    "title": "Hosting Provider",
                    "name": "Section_%s" % self.opu.generate_op_section_uuid(),
                    "fields": [
                        {
                            "inputTraits": {
                                "autocapitalization": "Words"
                            },
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "t": "name"
                        },
                        {
                            "inputTraits": {
                                "keyboard": "URL"
                            },
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "t": "website"
                        },
                        {
                            "inputTraits": {
                                "keyboard": "URL"
                            },
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "t": "support URL"
                        },
                        {
                            "inputTraits": {
                                "keyboard": "NamePhonePad"
                            },
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "t": "support phone"
                        }
                    ]
                }
            ]
        }

