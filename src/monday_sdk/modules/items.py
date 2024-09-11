from typing import Union, Dict, Any, List
import datetime

from ..graphql_handler import MondayGraphQL
from ..query_templates import create_item_query, get_item_query, change_column_value_query, get_item_by_id_query, update_multiple_column_values_query, create_subitem_query, delete_item_query, archive_item_query, move_item_to_group_query, change_simple_column_value_query  # type: ignore
from ..types import MondayApiResponse, Item

class ItemModule(MondayGraphQL):
    """ "
    todo: add types for this module
    """

    def change_custom_column_value(
        self, board_id: Union[str, int], item_id: Union[str, int], column_id: str, value: Dict[str, Any]
    ):
        """
        for text columns, use change_simple_column_value
        for status columns, use change_status_column_value
        for date columns, use change_date_column_value
        for other columns, use this method, for example, for checkbox columns pass {'checked': True}
        """
        query = change_column_value_query(board_id, item_id, column_id, value)
        return self.execute(query)

    def change_simple_column_value(
        self, board_id: Union[str, int], item_id: Union[str, int], column_id: str, value: str
    ):
        query = change_simple_column_value_query(board_id, item_id, column_id, value)
        return self.execute(query)

    def change_status_column_value(
        self, board_id: Union[str, int], item_id: Union[str, int], column_id: str, value: str
    ):
        dict_value = {"label": value}
        return self.change_custom_column_value(board_id, item_id, column_id, dict_value)

    def change_date_column_value(
        self, board_id: Union[str, int], item_id: Union[str, int], column_id: str, timestamp: datetime
    ):
        dict_value = {"date": timestamp.strftime("%Y-%m-%d"), "time": timestamp.strftime("%H:%M:%S")}
        return self.change_custom_column_value(board_id, item_id, column_id, dict_value)

    def create_item(
        self,
        board_id: Union[str, int],
        group_id: Union[str, int],
        item_name: str,
        column_values: Dict[str, Any] = None,
        create_labels_if_missing=False,
    ):
        query = create_item_query(board_id, group_id, item_name, column_values, create_labels_if_missing)
        return self.execute(query)

    def create_subitem(
        self,
        parent_item_id: Union[str, int],
        subitem_name: str,
        column_values: Dict[str, Any] = None,
        create_labels_if_missing=False,
    ):
        query = create_subitem_query(parent_item_id, subitem_name, column_values, create_labels_if_missing)
        return self.execute(query)

    def fetch_items_by_column_value(
        self, board_id: Union[str, int], column_id: str, value: str, limit: int = None, cursor: str = None
    ):
        query = get_item_query(board_id, column_id, value, limit, cursor)
        return self.execute(query)

    def fetch_items_by_id(self, ids: Union[str, int, List[Union[str, int]]]) -> List[Item]:
        if isinstance(ids, (list, set)):
            ids_str = ", ".join(map(str, ids))
            ids_str = f"[{ids_str}]"
        else:
            ids_str = str(ids)
        query = get_item_by_id_query(ids_str)
        response = self.execute(query)
        return response.data.items

    def change_multiple_column_values(
        self,
        board_id: Union[str, int],
        item_id: Union[str, int],
        column_values: Dict[str, Any],
        create_labels_if_missing: bool = False,
    ):
        query = update_multiple_column_values_query(board_id, item_id, column_values, create_labels_if_missing)
        return self.execute(query)

    def move_item_to_group(self, item_id: Union[str, int], group_id: Union[str, int]):
        query = move_item_to_group_query(item_id, group_id)
        return self.execute(query)

    def archive_item_by_id(self, item_id: Union[str, int]):
        query = archive_item_query(item_id)
        return self.execute(query)

    def delete_item_by_id(self, item_id: Union[str, int]):
        query = delete_item_query(item_id)
        return self.execute(query)
