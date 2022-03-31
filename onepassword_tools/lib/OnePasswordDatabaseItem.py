from onepassword_tools.lib.OnePasswordItem import OnePasswordItem


class OnePasswordDatabaseItem(OnePasswordItem):

    database: str = None
    hostname: str = None
    item_type: str = 'Database'
    notes: str = None
    password: str = None
    port: str = None
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
        section = {
            "title": "",
            "name": "Section_%s" % self.opu.generate_op_section_uuid()
        }


        return {
            "sections": [
                section
            ],
            "category": "DATABASE",
            "fields": [
                {
                    "id": "notesPlain",
                    "type": "STRING",
                    "purpose": "NOTES",
                    "label": "notedPlain",
                    "value": self.get('notes')
                },
                {
                    "type": "MENU",
                    "id": "database_type",
                    "label": "type",
                    "value": ""
                },
                {
                    "type": "STRING",
                    "id": "hostname",
                    "value": self.hostname,
                    "label": "server"
                },
                {
                    "inputTraits": {
                        "keyboard": "NumberPad"
                    },
                    "type": "STRING",
                    "id": "port",
                    "value": self.port,
                    "label": "port"
                },
                {
                    "inputTraits": {
                        "autocapitalization": "none",
                        "autocorrection": "no"
                    },
                    "type": "string",
                    "id": "database",
                    "value": self.database,
                    "label": "database"
                },
                {
                    "type": "STRING",
                    "id": "username",
                    "value": self.username,
                    "label": "username"
                },
                {
                    "type": "concealed",
                    "id": "password",
                    "value": self.password,
                    "label": "password"
                },
                {
                    "type": "STRING",
                    "id": "sid",
                    "label": "SID",
                    "value": ""
                },
                {
                    "type": "STRING",
                    "id": "alias",
                    "label": "alias",
                    "value": ""
                },
                {
                    "type": "STRING",
                    "id": "options",
                    "label": "connection options",
                    "value": ""
                }
            ]
        }
