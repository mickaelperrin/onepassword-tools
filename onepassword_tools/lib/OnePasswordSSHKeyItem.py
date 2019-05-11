from onepassword_tools.lib.OnePasswordItem import OnePasswordItem


class OnePasswordSSHKeyItem(OnePasswordItem):

    from_user: str = None
    from_host: str = None
    to_host: str = None
    to_host_abbreviated: str = None
    to_ip: str = None
    to_user: str = None
    passphrase: str = None
    public_key: str = None
    private_key: str = None
    item_type: str = 'Server'
    title: str = None
    notes: str = ''
    tags: [] = ['Clef SSH']
    url: str = None
    username: str
    port: str = None

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
        if self.to_host and self.to_user:
            return "ssh://%s@%s" % (self.to_user, self.to_host)
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
                            "k": "concealed",
                            "n": self.opu.generate_op_field_uuid(),
                            "v": self.get('passphrase'),
                            "t": "Passphrase"
                        },
                        {
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "v": self.get('to_host'),
                            "t": "Hostname"
                        },
                        {
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "v": self.get('to_ip'),
                            "t": "IP"
                        },
                        {
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "v": self.get('public_key'),
                            "t": "Public Key"
                        },
                        {
                            "k": "string",
                            "a": {
                                "multiline": "yes"
                            },
                            "n": self.opu.generate_op_field_uuid(),
                            "v": self.get('private_key'),
                            "t": "Private Key"
                        },
                        {
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "v": self.get('url'),
                            "t": "url"
                        },
                        {
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "v": str(self.get('port')),
                            "t": "port"
                        },
                        {
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "v": self.get('to_host_abbreviated'),
                            "t": "Hostname abbreviated"
                        },
                        {
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "v": self.get('to_user'),
                            "t": "Remote user"
                        },
                        {
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "v": self.get('from_user'),
                            "t": "Local user"
                        },
                        {
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "v": self.get('from_host'),
                            "t": "Local host"
                        }
                    ]
                }
            ]
        }
