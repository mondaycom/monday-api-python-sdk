from typing import Optional, Union, List

from ..query_templates import get_activity_logs_query
from ..types import MondayApiResponse, ActivityLog
from ..graphql_handler import MondayGraphQL
from ..settings import DEFAULTS

ACTIVITY_LOGS_DEFAULT_LIMIT = DEFAULTS["DEFAULT_PAGE_LIMIT_ACTIVITY_LOGS"]

class ActivityLogModule(MondayGraphQL):
    def fetch_activity_logs_from_board(
        self,
        board_ids: Union[int, str],
        page: Optional[int] = 1,
        limit: Optional[int] = ACTIVITY_LOGS_DEFAULT_LIMIT,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
    ) -> MondayApiResponse:
        query = get_activity_logs_query(board_ids, limit, page, from_date, to_date)
        return self.execute(query)

    def fetch_all_activity_logs_from_board(
        self,
        board_ids: Union[int, str],
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        limit: Optional[int] = ACTIVITY_LOGS_DEFAULT_LIMIT,
        events_filter: Optional[List[str]] = None,
    ) -> List[ActivityLog]:
        page = 1
        activity_logs = []
        while True:
            response = self.fetch_activity_logs_from_board(
                board_ids=board_ids, limit=limit, page=page,
                from_date=from_date,to_date=to_date
            )
            current_activity_logs = response.data.boards[0].activity_logs
            if not current_activity_logs:  # ATM is the only way to check if there are no more activity logs
                break
            else:
                relevant_activity_logs = current_activity_logs if events_filter is None else
                    [log for log in current_activity_logs if log.event in events_filter]
                activity_logs.extend(relevant_activity_logs)
                page += 1

        return activity_logs
