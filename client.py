from types import MondayClientSettings
from modules import BoardModule, ItemModule, UpdateModule, CustomModule, ActivityLogModule
from constants import API_VERSION, DEFAULT_MAX_RETRY_ATTEMPTS

BASE_HEADERS = {"API-Version": API_VERSION}


class MondayClient:
    def __init__(self, token, headers=None, debug_mode=False, max_retry_attempts=DEFAULT_MAX_RETRY_ATTEMPTS):

        headers = headers or BASE_HEADERS.copy()
        self.settings = MondayClientSettings(token, headers, debug_mode, max_retry_attempts)

        self.boards = BoardModule(self.settings)
        self.items = ItemModule(self.settings)
        self.updates = UpdateModule(self.settings)
        self.activity_logs = ActivityLogModule(self.settings)
        self.custom = CustomModule(self.settings)
