from typing import List

from ..query_templates import create_update_query, delete_update_query, get_update_query, get_updates_for_item_query, get_updates_for_board  # type: ignore
from ..types import MondayApiResponse, Update  # type: ignore
from ..graphql_handler import MondayGraphQL  # type: ignore

class UpdateModule(MondayGraphQL):
    def create_update(self, item_id, update_value) -> MondayApiResponse:
        query = create_update_query(item_id, update_value)
        return self.execute(query)

    def delete_update(self, item_id) -> MondayApiResponse:
        query = delete_update_query(item_id)
        return self.execute(query)

    def fetch_updates(self, limit, page=None) -> MondayApiResponse:
        query = get_update_query(limit, page)
        return self.execute(query)

    def fetch_updates_for_item(self, item_id, limit=100) -> MondayApiResponse:
        query = get_updates_for_item_query(item_id=item_id, limit=limit)
        return self.execute(query)

    def fetch_board_updates(self, board_id, limit=100, page=1) -> List[Update]:
        query = get_updates_for_board(board_id, limit, page)
        response: MondayApiResponse = self.execute(query)
        return response.data.boards[0].updates
