from datetime import datetime
from typing import List, Optional

from ..query_templates import create_update_query, delete_update_query, get_update_query, get_updates_for_item_query, get_updates_for_board
from ..types import MondayApiResponse, Update
from ..graphql_handler import MondayGraphQL

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

    def fetch_board_updates_page(self, board_id, limit=100, page=1) -> List[Update]:
        query = get_updates_for_board(board_id, limit, page)
        response: MondayApiResponse = self.execute(query)
        return response.data.boards[0].updates

    def fetch_board_updates(
        self,
        board_ids: str,
        updated_after: Optional[str] = None,
        updated_before: Optional[str] = None,
    ) -> List[Update]:
        """
        Fetches all updates from a board (with optional date filtering).
        - Paginates through all pages until no more updates.
        - If from_date or to_date are provided, filters out updates outside that window.
        """
        start_dt = datetime.fromisoformat(updated_after) if updated_after else None
        end_dt = datetime.fromisoformat(updated_before) if updated_before else None

        all_updates = []
        page = 1

        while True:
            updates = self.fetch_board_updates_page(board_ids, page=page)
            if not updates:
                break

            if start_dt or end_dt:
                updates = [
                    u for u in updates
                    if (
                            u.updated_at
                            and (start_dt is None or datetime.fromisoformat(u.updated_at) >= start_dt)
                            and (end_dt is None or datetime.fromisoformat(u.updated_at) <= end_dt)
                    )
                ]

            all_updates.extend(updates)
            page += 1

        return all_updates