from typing import List, Optional, Union, Any, Mapping

from ..graphql_handler import MondayGraphQL
from ..query_templates import get_boards_query, get_board_by_id_query, get_board_items_query, get_columns_by_board_query
from ..types import MondayApiResponse, Item, BoardKind, BoardState, BoardsOrderBy, Operator, ItemsOrderByDirection
from ..utils import sleep_according_to_complexity, construct_updated_at_query_params
from ..constants import DEFAULT_PAGE_LIMIT_BOARDS, DEFAULT_PAGE_LIMIT_ITEMS


def is_cursor_expired_error(error: Exception) -> bool:
    """Check if the exception is a CursorExpiredError."""
    return "CursorExpiredError" in str(error)


class BoardModule:
    def __init__(self, graphql_client: MondayGraphQL):
        self.client = graphql_client

    def fetch_boards(
        self,
        limit: Optional[int] = DEFAULT_PAGE_LIMIT_BOARDS,
        page: Optional[int] = None,
        ids: Optional[List[int]] = None,
        board_kind: Optional[BoardKind] = None,
        state: Optional[BoardState] = None,
        order_by: Optional[BoardsOrderBy] = None,
    ) -> MondayApiResponse:
        query = get_boards_query(ids=ids, limit=limit, page=page, board_kind=board_kind, state=state, order_by=order_by)
        return self.client.execute(query)

    def fetch_boards_by_id(self, board_id: Union[int, str]) -> MondayApiResponse:
        query = get_board_by_id_query(board_id)
        return self.client.execute(query)

    def fetch_all_items_by_board_id(
        self,
        board_id: Union[int, str],
        query_params: Optional[Mapping[str, Any]] = None,
        limit: Optional[int] = DEFAULT_PAGE_LIMIT_ITEMS,
    ) -> List[Item]:
        """
        Fetches all items from a board by board ID, includes paginating
        todo: add support for multiple board IDs
        """
        items: List[Item] = []
        cursor = None

        while True:
            query = get_board_items_query(board_id, query_params=query_params, cursor=cursor, limit=limit)
            response = self.client.execute(query)
            items_page = response.data.boards[0].items_page if cursor is None else response.data.next_items_page

            items.extend(items_page.items)
            complexity = response.data.complexity.query
            cursor = items_page.cursor

            if cursor:
                sleep_according_to_complexity(complexity)
            else:
                break

        return items

    def fetch_all_items_by_board_id_large_board(
        self,
        board_id: Union[int, str],
        query_params: Optional[Mapping[str, Any]] = None,
        limit: Optional[int] = DEFAULT_PAGE_LIMIT_ITEMS,
    ) -> List[Item]:
        """
        Fetches all items from a board by board ID, with cursor expiration handling.
        Uses updated_at tracking to recover from CursorExpiredError and continue fetching.
        Suitable for large boards where cursor might expire during pagination.

        When a cursor expires, the function rebuilds the query using the last known
        updated_at timestamp to continue from where it left off.

        Note: Custom order_by in query_params is not supported. This function always
        orders by __last_updated__ ascending to ensure correct cursor recovery.
        """
        items: List[Item] = []
        cursor = None
        last_updated_at: Optional[str] = None
        last_updated_at_to_use = None
        page = 0
        while True:
            # Build query params with updated_at filter if recovering from cursor expiration
            print(f"Fetching page {page} with cursor: {cursor} and last_updated_at: {last_updated_at_to_use}")
            effective_query_params = self._merge_query_params_with_updated_at(query_params, last_updated_at_to_use)
            last_updated_at_to_use = None
            try:
                query = get_board_items_query(board_id, query_params=effective_query_params, cursor=cursor, limit=limit)
                response = self.client.execute(query)
                items_page = response.data.boards[0].items_page if cursor is None else response.data.next_items_page

                # Track the last updated_at for potential recovery
                if items_page.items:
                    last_updated_at = items_page.items[-1].updated_at

                items.extend(items_page.items)
                complexity = response.data.complexity.query
                cursor = items_page.cursor
                if not cursor:
                    break
                sleep_according_to_complexity(complexity)
                page += 1

            except Exception as e:
                if is_cursor_expired_error(e):
                    print(f"Cursor expired - resetting cursor and using updated_at filter to continue")
                    cursor = None
                    last_updated_at_to_use = last_updated_at
                    continue
                raise e

        return items

    def _merge_query_params_with_updated_at(
        self,
        query_params: Optional[Mapping[str, Any]],
        updated_after: Optional[str],
    ) -> Mapping[str, Any]:
        """
        Merges existing query_params with an updated_at filter and order_by clause.
        Always includes order_by to sort by updated_at ascending.
        If updated_after is provided, adds a filter to fetch items updated after that timestamp.
        """
        merged_params = query_params or {}
        merged_params["order_by"] = [{"column_id": "__last_updated__", "direction": ItemsOrderByDirection.ASC}]

        if updated_after is not None:
            updated_at_rule = {
                "column_id": "__last_updated__",
                "compare_value": ["EXACT", updated_after],
                "operator": Operator.GREATER_THAN_OR_EQUALS,
                "compare_attribute": "UPDATED_AT",
            }
            existing_rules = list(merged_params.get("rules", []))
            existing_rules.append(updated_at_rule)
            merged_params["rules"] = existing_rules

        return merged_params

    def fetch_item_by_board_id_by_update_date(
        self,
        board_id: Union[int, str],
        updated_after: str,
        updated_before: str,
        limit: Optional[int] = DEFAULT_PAGE_LIMIT_ITEMS,
    ) -> List[Item]:
        """
        Fetches items from a board by board ID by update date, useful for incremental fetching
        todo: add type hints for updated_after and updated_before and validate them
        """
        if not updated_after and not updated_before:
            raise ValueError(
                "Either updated_after or updated_before must be provided when fetching items by update date"
            )
        query_params = construct_updated_at_query_params(updated_after, updated_before)
        return self.fetch_all_items_by_board_id(board_id, query_params=query_params, limit=limit)

    def fetch_columns_by_board_id(self, board_id: Union[int, str]) -> MondayApiResponse:
        query = get_columns_by_board_query(board_id)
        return self.client.execute(query)
