import json
from enum import Enum
from typing import List, Union, Optional, Mapping, Any

from .types import BoardKind, BoardState, BoardsOrderBy
from .utils import monday_json_stringify, gather_params


# todo: divide into separate files, take into account that multiple resources can use the same query


def get_board_items_query(
    board_ids: Union[int, str],
    limit: int,
    query_params: Optional[Mapping[str, Any]] = None,
    cursor: Optional[str] = None,
) -> str:
    if cursor is None:
        return get_board_items_first_page_query(board_ids, query_params=query_params, limit=limit)
    else:
        return get_board_items_pagination_query(cursor=cursor, limit=limit)


def get_board_items_first_page_query(
    board_id: Union[str, int], limit: int, query_params: Optional[Mapping[str, Any]] = None
) -> str:
    raw_params = locals().items()
    items_page_params = gather_params(raw_params, excluded_params=["board_id"])
    wrapped_params = f"({items_page_params})" if items_page_params else ""

    query = """{
        complexity {
        query
        after
      }
        boards(ids: %s){
            name
            items_page %s {
                cursor
                items {
                    id
                    name
                    group {
                        id
                        title
                    }
                    column_values {
                      ... on MirrorValue {
                        display_value
                      }
                      ... on BoardRelationValue {
                        display_value
                      }
                      ... on DependencyValue {
                        display_value
                      }
                      value
                      text
                      type
                      column {
                        id
                        title
                      }
                    }
                    subitems {
                      name
                      id
                      parent_item {
                        id
                      }
                      group {
                        id
                        title
                      }
                      column_values {
                        ... on MirrorValue {
                          display_value
                        }
                        ... on DependencyValue {
                          display_value
                        }
                        ... on BoardRelationValue {
                          display_value
                        }
                        text
                        type
                        column {
                          id
                          title
                        }
                      }
                    }
                }
            }
        }
    }""" % (
        board_id,
        wrapped_params,
    )
    return query


def get_board_items_pagination_query(cursor: str, limit: int) -> str:

    query = """{
        complexity {
        query
        after
      }
        next_items_page(limit: %s, cursor: "%s") {
            cursor
            items {
                id
                name
                group {
                    id
                    title
                }
                column_values {
                  ... on MirrorValue {
                    display_value
                  }
                  ... on BoardRelationValue {
                    display_value
                  }
                  ... on DependencyValue {
                    display_value
                  }
                  value
                  text
                  type
                  column {
                    id
                    title
                  }
                }
                subitems {
                  name
                  id
                  group {
                    id
                    title
                  }
                  column_values {
                    ... on MirrorValue {
                      display_value
                    }
                    ... on DependencyValue {
                      display_value
                    }
                    ... on BoardRelationValue {
                      display_value
                    }
                    text
                    type
                    column {
                      id
                      title
                    }
                  }
                }
            }
        }
    }""" % (
        limit,
        cursor,
    )
    return query


# ITEM RESOURCE QUERIES
def create_item_query(board_id, group_id, item_name, column_values, create_labels_if_missing):
    # Monday does not allow passing through non-JSON null values here,
    # so if you choose not to specify column values, need to set column_values to empty object.
    column_values = column_values or {}

    query = """mutation
    {
        create_item (
            board_id: %s,
            group_id: "%s",
            item_name: "%s",
            column_values: %s,
            create_labels_if_missing: %s
        ) {
            id
        }
    }""" % (
        board_id,
        group_id,
        item_name,
        monday_json_stringify(column_values),
        str(create_labels_if_missing).lower(),
    )

    return query


def create_subitem_query(parent_item_id, subitem_name, column_values, create_labels_if_missing):
    column_values = column_values or {}

    return """mutation
    {
        create_subitem (
            parent_item_id: %s,
            item_name: "%s",
            column_values: %s,
            create_labels_if_missing: %s
        ) {
            id,
            name,
            column_values {
                id,
                text
            },
            board {
                id,
                name
            }
        }
    }""" % (
        parent_item_id,
        subitem_name,
        monday_json_stringify(column_values),
        str(create_labels_if_missing).lower(),
    )


def get_item_query(board_id, column_id, value, limit, cursor=None):
    columns = [{"column_id": str(column_id), "column_values": [str(value)]}] if not cursor else None

    raw_params = locals().items()
    items_page_params = gather_params(raw_params, excluded_params=["column_id", "value"])

    query = (
        """query
        {
            items_page_by_column_values (%s) {
                cursor
                items {
                    id
                    name
                    updates {
                        id
                        body
                    }
                    group {
                        id
                        title
                    }
                    column_values {
                        id
                        text
                        value
                    }                
                }
            }
        }"""
        % items_page_params
    )

    return query


def get_item_by_id_query(ids):
    query = """{
            complexity {
            query
            after
          }
            items(ids: %s){
                id
                name
                state
                group {
                    id
                    title
                }
                column_values {
                  ... on MirrorValue {
                    display_value
                  }
                  ... on BoardRelationValue {
                    display_value
                  }
                  ... on DependencyValue {
                    display_value
                  }
                  value
                  text
                  type
                  column {
                    id
                    title
                  }
                }
                subitems {
                  name
                  id
                  parent_item {
                    id
                  }
                  group {
                    id
                    title
                  }
                  column_values {
                    ... on MirrorValue {
                      display_value
                    }
                    ... on DependencyValue {
                      display_value
                    }
                    ... on BoardRelationValue {
                      display_value
                    }
                    text
                    type
                    column {
                      id
                      title
                    }
                  }
                }
            }
        }""" % (
        ids
    )

    return query


def change_column_value_query(board_id, item_id, column_id, value):
    query = """mutation
        {
            change_column_value(
                board_id: %s,
                item_id: %s,
                column_id: "%s",
                value: %s
            ) {
                id
                name
                column_values {
                    id
                    text
                    value
                }
            }
        }""" % (
        board_id,
        item_id,
        column_id,
        monday_json_stringify(value),
    )

    return query


def change_simple_column_value_query(board_id, item_id, column_id, value):
    query = """mutation
    {
        change_simple_column_value (
            board_id: %s,
            item_id: %s,
            column_id: "%s",
            value: "%s"
        ) {
            id
        }
    }""" % (
        board_id,
        item_id,
        column_id,
        value,
    )

    return query


def move_item_to_group_query(item_id, group_id):
    query = """
    mutation
    {
        move_item_to_group (item_id: %s, group_id: "%s")
        {
            id
        }
    }""" % (
        item_id,
        group_id,
    )
    return query


def archive_item_query(item_id):
    query = (
        """
    mutation
    {
        archive_item (item_id: %s)
        {
            id
        }
    }"""
        % item_id
    )
    return query


def delete_item_query(item_id):
    query = (
        """
    mutation
    {
        delete_item (item_id: %s)
        {
            id
        }
    }"""
        % item_id
    )
    return query


def get_columns_by_board_query(board_id):
    return (
        """query
        {
            boards(ids: %s) {
                id
                name
                groups {
                    id
                    title
                }
                columns {
                    title
                    id
                    type
                    settings_str
                 }
            }
        }"""
        % board_id
    )


def update_multiple_column_values_query(board_id, item_id, column_values, create_labels_if_missing=False):
    query = """mutation
        {
            change_multiple_column_values (
                board_id: %s,
                item_id: %s,
                column_values: %s,
                create_labels_if_missing: %s
            ) {
                id
                name
                column_values {
                  id
                  text
                }
            }
        }""" % (
        board_id,
        item_id,
        monday_json_stringify(column_values),
        str(create_labels_if_missing).lower(),
    )

    return query


# UPDATE RESOURCE QUERIES
def create_update_query(item_id, update_value):
    query = """mutation
        {
            create_update(
                item_id: %s,
                body: %s
            ) {
                id
            }
        }""" % (
        item_id,
        json.dumps(update_value),
    )

    return query


def delete_update_query(item_id):
    query = (
        """mutation {
        delete_update (id: %s) {
            id
        }
    }"""
        % item_id
    )

    return query


def get_updates_for_item_query(item_id, limit: int):
    query = """query{                
        items(ids: %s){
            updates (limit: %s) {
                id,
                body,
                created_at,
                updated_at,
                creator {
                  id,
                  name,
                  email
                },
                assets {
                  id,
                  name,
                  url,
                  file_extension,
                  file_size
                },
                replies {
                    id,
                    body,
                    creator{
                        id,
                        name,
                        email
                    },
                    created_at,
                    updated_at
                }
            }
        }
    }""" % (
        item_id,
        limit,
    )

    return query


def get_updates_for_board(board_id, limit: int, page=1):
    query = """query
    {
        boards(ids: %s) {
            updates(limit: %s, page: %s) {
                id,
                text_body,
                item_id,
                created_at,
                creator {
                    name,
                    id
                }
            }
        }
    }""" % (
        board_id,
        limit,
        page,
    )

    return query


def get_update_query(limit, page=1):
    query = """query
        {
            updates (
                limit: %s,
                page: %s
            ) {
                id,
                body
            }
        }""" % (
        limit,
        page,
    )

    return query


def get_boards_query(
    ids: List[int],
    limit: int,
    page: int = 1,
    board_kind: BoardKind = None,
    state: BoardState = None,
    order_by: BoardsOrderBy = None,
):
    parameters = locals().items()
    query_params = []
    for k, v in parameters:
        if v is not None:
            value = v
            if isinstance(v, Enum):
                value = v.value
            query_params.append("%s: %s" % (k, value))
    joined_params = f"({', '.join(query_params)})" if query_params else ""

    query = (
        """query
    {
        boards %s {
            id
            name
            permissions
            tags {
              id
              name
            }
            groups {
                id
                title
            }
            columns {
                id
                title
                type
            }
        }
    }"""
        % joined_params
    )

    return query


def get_board_by_id_query(board_id: Union[int, str]):
    return (
        """query
    {
        boards (ids: %s) {
            id
            name
            permissions
            tags {
              id
              name
            }
            groups {
                id
                title
            }
            columns {
                id
                title
                type
                settings_str
            }
        }
    }"""
        % board_id
    )


def get_items_by_group_query(board_id: Union[int, str], group_id: str, limit: int, cursor: Optional[str] = None):
    raw_params = locals().items()
    items_page_params = gather_params(raw_params, excluded_params=["board_id", "group_id"])
    wrapped_params = f"({items_page_params})" if items_page_params else ""

    query = """query
    {
        boards(ids: %s) {
            groups(ids: "%s") {
                id
                title
                items_page %s {
                    cursor
                    items {
                        id
                        name
                    }
                }
            }
        }
    }""" % (
        board_id,
        group_id,
        wrapped_params,
    )
    return query


def get_complexity_query():
    query = """
    query
    {
        complexity {
            after,
            reset_in_x_seconds
        }
    }"""

    return query


def get_activity_logs_query(
    board_id: Union[int, str],
    limit: int,
    page: Optional[int] = 1,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
):
    raw_params = locals().items()
    activity_logs_params = gather_params(raw_params, excluded_params=["board_id", "from_date", "to_date"])

    # Monday API excepts "from" and "to" and the function parameters couldn't be named that way because of Python's reserved words
    if from_date:
        activity_logs_params += f', from: "{from_date}"'
    if to_date:
        activity_logs_params += f', to: "{to_date}"'

    wrapped_params = f"({activity_logs_params})" if activity_logs_params else ""

    query = """{
        complexity {
            query
            after
        }
        boards(ids: %s) {
            activity_logs %s {
                id
                account_id
                created_at
                data
                entity
                event
                user_id
            }
        }
    }""" % (
        board_id,
        wrapped_params,
    )

    return query
