from typing import List

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

    def fetch_board_updates(self, board_id, limit=100, page=1) -> List[Update]:
        query = get_updates_for_board(board_id, limit, page)
        response: MondayApiResponse = self.execute(query)
        return response.data.boards[0].updates

    def fetch_all_board_updates(
        self,
        board_id: int,
        limit: int = 100,
        updated_before: Optional[datetime] = None,
        updated_after: Optional[datetime] = None,
    ) -> List[Update]:
        """
        Fetches updates from the given board across ALL pages, automatically
        paginating until no more updates are returned. Optionally filters by
        `updated_before` and/or `updated_after`.

        :param board_id: The ID of the board to retrieve updates from.
        :param limit: The number of updates per page.
        :param updated_before: Return only updates with `updated_at` <= this datetime.
        :param updated_after:  Return only updates with `updated_at` >= this datetime.
        :return: A list of updates, each represented as a dict (or your custom Update type).
        """
        all_updates: List[Update] = []
        page = 1

        while True:
            # 1) Fetch a single page of updates using the existing method
            updates = self.fetch_board_updates(board_id, limit=limit, page=page)
            if not updates:
                # If we get an empty list, we've reached the end of the results
                break

            # 2) Filter by updated_before / updated_after if provided
            filtered_updates = []
            for update in updates:
                updated_at_str = update.get("updated_at")
                if not updated_at_str:
                    # If somehow there's no 'updated_at', skip it
                    continue

                updated_time = dateutil.parser.isoparse(updated_at_str)
                # If updated_before is provided, skip if update is AFTER that date
                if updated_before and updated_time > updated_before:
                    continue
                # If updated_after is provided, skip if update is BEFORE that date
                if updated_after and updated_time < updated_after:
                    continue

                filtered_updates.append(update)

            # 3) Accumulate the filtered updates
            all_updates.extend(filtered_updates)

            # 4) Move to next page
            page += 1

        return all_updates