from onepassword_tools.lib.OnePasswordUtils import OnePasswordUtils
from onepassword_tools.lib.MiscUtils import remove_null_value_keys_in_dict
import uuid
from abc import ABCMeta, abstractmethod


class OnePasswordItem:
    __metaclass__ = ABCMeta

    createCustomUUID: bool = True

    @property
    @abstractmethod
    def item_type(self) -> str:
        pass

    def __init__(self):
        self.opu = OnePasswordUtils()

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        else:
            return None

    @abstractmethod
    def _request_object(self):
        """
        Static dictionnary reprensenting the request sent to 1Password to create entry
        :return: dict
        """
        return

    def get(self, item):
        if item == 'notes' and getattr(self, item) is None:
            return ""
        else:
            return self[item]

    def get_uuid_section(self, section_uuid):
        return {
            "title": "",
            "name": section_uuid,
        }

    def get_uuid_field(self, section_uuid):
        return {
            "label": "UUID",
            "value": str(uuid.uuid4()),
            "type": "STRING",
            "id": self.opu.generate_op_field_uuid(),
            "section": self.get_uuid_section(section_uuid)
        }

    def get_request_object(self):
        request = self._request_object()

        if self.createCustomUUID:
            section_uuid = "Section_%s" % self.opu.generate_op_section_uuid()
            request['sections'].append(self.get_uuid_section(section_uuid))
            request['fields'].append(self.get_uuid_field(section_uuid))

        request = remove_null_value_keys_in_dict(request)

        return request
