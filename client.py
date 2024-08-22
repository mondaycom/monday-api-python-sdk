from .modules import BoardModule, ItemModule, UpdateModule, CustomModule, ActivityLogModule
from .settings import API_VERSION

BASE_HEADERS = {"API-Version": API_VERSION}


class MondayClient:
    def __init__(self, token, headers=None):

        headers = headers or BASE_HEADERS.copy()

        self.boards = BoardModule(token, headers)
        self.items = ItemModule(token, headers)
        self.updates = UpdateModule(token, headers)
        self.activity_logs = ActivityLogModule(token, headers)
        self.custom = CustomModule(token, headers)
