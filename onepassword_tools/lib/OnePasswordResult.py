from onepassword_local_search.models.Item import Item


class OnePasswordResult(Item):

    overview: str
    details: str
    uuid: str
    vaultUuid: str

    def __init__(self, response):
        for attr in response.keys():
            setattr(self, attr, response[attr])


