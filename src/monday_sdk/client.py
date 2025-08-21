from .modules import BoardModule, ItemModule, UpdateModule, CustomModule, ActivityLogModule, DocsModule
from .constants import API_VERSION, DEFAULT_MAX_RETRY_ATTEMPTS
from .graphql_handler import MondayGraphQL

BASE_HEADERS = {"API-Version": API_VERSION}


class MondayClient:
    def __init__(self, token, headers=None, debug_mode=False, max_retry_attempts=DEFAULT_MAX_RETRY_ATTEMPTS):
        headers = headers or BASE_HEADERS.copy()
        
        # Create a single GraphQL client instance
        self._graphql_client = MondayGraphQL(
            token=token,
            headers=headers,
            debug_mode=debug_mode,
            max_retry_attempts=max_retry_attempts
        )

        # Pass the GraphQL client to each module
        self.boards = BoardModule(self._graphql_client)
        self.items = ItemModule(self._graphql_client)
        self.updates = UpdateModule(self._graphql_client)
        self.activity_logs = ActivityLogModule(self._graphql_client)
        self.custom = CustomModule(self._graphql_client)
        self.docs = DocsModule(self._graphql_client)
