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
    to_port: str = None

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
        section = {
            "title": "",
            "name": "Section_%s" % self.opu.generate_op_section_uuid()
        }

        return {
            "category": "SERVER",
            "fields": [
                {
                    "id": "notesPlain",
                    "type": "STRING",
                    "purpose": "NOTES",
                    "label": "notesPlain",
                    "value": self.get('notes'),
                },
                {
                    "type": "concealed",
                    "id": self.opu.generate_op_field_uuid(),
                    "value": self.get('passphrase'),
                    "label": "Passphrase",
                    "section": section
                },
                {
                    "type": "string",
                    "id": self.opu.generate_op_field_uuid(),
                    "value": self.get('to_host'),
                    "label": "Hostname",
                    "section": section
                },
                {
                    "type": "string",
                    "id": self.opu.generate_op_field_uuid(),
                    "value": self.get('to_ip'),
                    "label": "IP",
                    "section": section
                },
                {
                    "type": "string",
                    "id": self.opu.generate_op_field_uuid(),
                    "value": self.get('public_key'),
                    "label": "Public Key",
                    "section": section
                },
                {
                    "id": "private_key",
                    "type": "UNKNOWN",
                    "value": self.get('private_key'),
                    "label": "private key",
                    "section": section
                },
                {
                    "type": "string",
                    "a": {
                        "multiline": "yes"
                    },
                    "id": self.opu.generate_op_field_uuid(),
                    "value": self.get('private_key'),
                    "label": "Private Key",
                    "section": section
                },
                {
                    "type": "string",
                    "id": self.opu.generate_op_field_uuid(),
                    "value": self.get('url'),
                    "label": "url",
                    "section": section
                },
                {
                    "type": "string",
                    "id": self.opu.generate_op_field_uuid(),
                    "value": str(self.get('to_port')),
                    "label": "Port",
                    "section": section
                },
                {
                    "type": "string",
                    "id": self.opu.generate_op_field_uuid(),
                    "value": self.get('to_host_abbreviated'),
                    "label": "Hostname abbreviated",
                    "section": section
                },
                {
                    "type": "string",
                    "id": self.opu.generate_op_field_uuid(),
                    "value": self.get('to_user'),
                    "label": "Remote user",
                    "section": section
                },
                {
                    "type": "string",
                    "id": self.opu.generate_op_field_uuid(),
                    "value": self.get('from_user'),
                    "label": "Local user",
                    "section": section
                },
                {
                    "type": "string",
                    "id": self.opu.generate_op_field_uuid(),
                    "value": self.get('from_host'),
                    "label": "Local host",
                    "section": section
                },
                {
                    "type": "string",
                    "id": self.opu.generate_op_field_uuid(),
                    "value": '',
                    "label": "SSH Config",
                    "section": section
                }
            ],
            "sections": [
                section
            ]
        }
