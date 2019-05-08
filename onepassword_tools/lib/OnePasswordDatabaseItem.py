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
        return {
            "notesPlain": self.get('notes'),
            "sections": [
                {
                    "title": "",
                    "name": "Section_%s" % self.opu.generate_op_section_uuid(),
                    "fields": [
                        {
                            "k": "menu",
                            "n": self.opu.generate_op_field_uuid(),
                            "t": "type",
                        },
                        {
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "v": self.hostname,
                            "t": "server"
                        },
                        {
                            "inputTraits": {
                                "keyboard": "NumberPad"
                            },
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "v": self.port,
                            "t": "port"
                        },
                        {
                            "inputTraits": {
                                "autocapitalization": "none",
                                "autocorrection": "no"
                            },
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "v": self.database,
                            "t": "database"
                        },
                        {
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "v": self.username,
                            "t": "username"
                        },
                        {
                            "k": "concealed",
                            "n": self.opu.generate_op_field_uuid(),
                            "v": self.password,
                            "t": "password"
                        },
                        {
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "t": "SID"
                        },
                        {
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "t": "alias"
                        },
                        {
                            "k": "string",
                            "n": self.opu.generate_op_field_uuid(),
                            "t": "connection options"
                        }
                    ]
                }
            ]
        }
