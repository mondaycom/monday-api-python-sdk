import json
import time

from enum import Enum
from typing import List, Iterable, Tuple, Any, Optional, Union
from .types import Item, Operator
from .constants import MAX_COMPLEXITY


def extract_column_value_by_title(item: Item, column_name: str) -> Union[str, bool]:
    item_column_values = item.column_values
    for column_value in item_column_values:
        if column_value.column.title == column_name:
            if column_value.type == "checkbox":
                # Parse the JSON string into a dictionary
                value_dict = json.loads(column_value.value)
                return value_dict["checked"]
            elif column_value.type in ["mirror", "board_relation", "dependency"]:
                return column_value.display_value or ""
            else:
                return column_value.text
    return ""


def extract_column_value_by_id(item: Item, column_id: str) -> Union[str, bool]:
    item_column_values = item.column_values
    for column_value in item_column_values:
        if column_value.column.id == column_id:
            if column_value.type == "checkbox":
                # Parse the JSON string into a dictionary
                value_dict = json.loads(column_value.value)
                return value_dict["checked"]
            elif column_value.type in ["mirror", "board_relation", "dependency"]:
                return column_value.display_value or ""
            else:
                return column_value.text
    return ""


def extract_column_id_by_title(item: Item, column_name: str) -> Union[str, None]:
    item_column_values = item.column_values
    for column_value in item_column_values:
        if column_value.column.title == column_name:
            return column_value.column.id
    return None


def monday_json_stringify(value):
    # Monday's required format: "{\"label\":\"Done\"}"
    return json.dumps(json.dumps(value))


def gather_params(params: Iterable[Tuple[str, Any]], excluded_params: Optional[List[str]] = None, exclude_none: bool = True) -> str:
    valid_params = [
        f"{param}: {format_param_value(value)}"
        for param, value in params
        if not ((excluded_params and param in excluded_params) or (value is None and exclude_none))
    ]
    return ", ".join(valid_params)


def format_param_value(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, str):
        return f'"{value}"'
    if isinstance(value, Enum):
        return str(value.value)
    if isinstance(value, dict):
        return f"{{{gather_params(value.items(), exclude_none=False)}}}"
    if isinstance(value, list):
        return f"[{', '.join(format_param_value(val) for val in value)}]"
    return str(value)


def sleep_according_to_complexity(query_complexity) -> None:
    """
    monday complexity is limited per minute, so the sleep is according to the "cost" of the current query
    """
    sleep_time = (query_complexity / MAX_COMPLEXITY) * 60
    time.sleep(sleep_time)


def construct_updated_at_query_params(start_date: str, end_date: str) -> dict:
    query_params = {"rules": []}
    if start_date:
        query_params["rules"].append(
            {
                "column_id": "__last_updated__",
                "compare_value": ["EXACT", start_date],
                "operator": Operator.GREATER_THAN_OR_EQUALS,
                "compare_attribute": "UPDATED_AT",
            }
        )
    if end_date:
        query_params["rules"].append(
            {
                "column_id": "__last_updated__",
                "compare_value": ["EXACT", end_date],
                "operator": Operator.LESS_THAN_OR_EQUALS,
                "compare_attribute": "UPDATED_AT",
            }
        )
    return query_params
