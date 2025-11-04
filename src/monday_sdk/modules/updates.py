from datetime import datetime
from typing import List, Optional

from ..query_templates import create_update_query, delete_update_query, get_update_query, get_updates_for_item_query, get_updates_for_board
from ..types import MondayApiResponse, Update
from ..graphql_handler import MondayGraphQL

class UpdateModule:
    def __init__(self, graphql_client: MondayGraphQL):
        self.client = graphql_client
    def create_update(self, item_id, update_value) -> MondayApiResponse:
        query = create_update_query(item_id, update_value)
        return self.client.execute(query)

    def delete_update(self, item_id) -> MondayApiResponse:
        query = delete_update_query(item_id)
        return self.client.execute(query)

    def fetch_updates(self, limit, page=None) -> MondayApiResponse:
        query = get_update_query(limit, page)
        return self.client.execute(query)

    def fetch_updates_for_item(self, item_id, limit=100) -> MondayApiResponse:
        query = get_updates_for_item_query(item_id=item_id, limit=limit)
        return self.client.execute(query)

    def fetch_board_updates_page(self, board_id, limit=100, page=1, from_date: Optional[str] = None, to_date: Optional[str] = None) -> List[Update]:
        """
        Fetches a single page of updates from a board.
        
        Note: from_date and to_date parameters require Monday API version 2026-01+
        """
        query = get_updates_for_board(board_id, limit, page, from_date, to_date)
        response: MondayApiResponse = self.client.execute(query)
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
        - Uses API-level date filtering (requires API version 2026-01+) when dates are provided.
        - Also applies client-side filtering as additional safety/fallback.
        """
        start_dt = datetime.fromisoformat(updated_after) if updated_after else None
        end_dt = datetime.fromisoformat(updated_before) if updated_before else None

        all_updates = []
        page = 1

        while True:
            updates = self.fetch_board_updates_page(
                board_ids, 
                page=page, 
                from_date=updated_after, 
                to_date=updated_before
            )
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

    def fetch_board_updates_incremental(
        self,
        board_id: str,
        limit: int = 100,
        page: int = 1,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> List[Update]:
        """
        Fetches updates from a board using Monday's native incremental fetch API.
        Uses the API's built-in date filtering instead of client-side filtering.
        
        **Requires API version 2026-01 or later**
        
        Args:
            board_id: The board ID to fetch updates from
            limit: Maximum number of updates per page (default: 100)
            page: Page number to fetch (default: 1)
            from_date: Start date in ISO format (e.g., "2025-10-10T00:00:00Z")
            to_date: End date in ISO format (e.g., "2025-11-11T00:00:00Z")
        
        Returns:
            List of Update objects
            
        Note:
            The from_date and to_date parameters require Monday API version 2026-01+.
            If using an older API version, use fetch_board_updates() instead which 
            provides client-side date filtering.
        """
        return self.fetch_board_updates_page(board_id, limit, page, from_date, to_date)