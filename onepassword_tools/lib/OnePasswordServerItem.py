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
        main_section_uuid = {
            "title": "",
            "name": "Section_%s" % self.opu.generate_op_section_uuid()
        }
        admin_section_uuid = {
            "title": "",
            "name": "Section_%s" % self.opu.generate_op_section_uuid()
        }

        hosting_provider_section_uuid = {
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
                    "value": self.get('notes')
                },
                {
                    "inputTraits": {
                        "keyboard": "URL"
                    },
                    "type": "string",
                    "id": self.opu.generate_op_field_uuid(),
                    "value": self.get('url'),
                    "label": "URL",
                    "section": main_section_uuid
                },
                {
                    "inputTraits": {
                        "autocapitalization": "none",
                        "autocorrection": "no"
                    },
                    "type": "string",
                    "id": self.opu.generate_op_field_uuid(),
                    "value": self.get('username'),
                    "label": "username",
                    "section": main_section_uuid
                },
                {
                    "type": "concealed",
                    "id": self.opu.generate_op_field_uuid(),
                    "value": self.get('password'),
                    "label": "password",
                    "section": main_section_uuid
                },
                {
                    "inputTraits": {
                        "keyboard": "URL"
                    },
                    "type": "string",
                    "id": self.opu.generate_op_field_uuid(),
                    "label": "admin console URL",
                    "section": admin_section_uuid
                },
                {
                    "inputTraits": {
                        "autocapitalization": "none",
                        "autocorrection": "no"
                    },
                    "type": "string",
                    "id": self.opu.generate_op_field_uuid(),
                    "label": "admin console username",
                    "section": admin_section_uuid
                },
                {
                    "type": "concealed",
                    "id": self.opu.generate_op_field_uuid(),
                    "label": "console password",
                    "section": admin_section_uuid
                },
                {
                    "inputTraits": {
                        "autocapitalization": "Words"
                    },
                    "type": "string",
                    "id": self.opu.generate_op_field_uuid(),
                    "label": "name",
                    "section": hosting_provider_section_uuid
                },
                {
                    "inputTraits": {
                        "keyboard": "URL"
                    },
                    "type": "string",
                    "id": self.opu.generate_op_field_uuid(),
                    "label": "website",
                    "section": hosting_provider_section_uuid
                },
                {
                    "inputTraits": {
                        "keyboard": "URL"
                    },
                    "type": "string",
                    "id": self.opu.generate_op_field_uuid(),
                    "label": "support URL",
                    "section": hosting_provider_section_uuid
                },
                {
                    "inputTraits": {
                        "keyboard": "NamePhonePad"
                    },
                    "type": "string",
                    "id": self.opu.generate_op_field_uuid(),
                    "label": "support phone",
                    "section": hosting_provider_section_uuid
                }
            ],
            "sections": [
                main_section_uuid,
                admin_section_uuid,
                hosting_provider_section_uuid
            ]
        }

