from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Column:
    id: Optional[str] = field(default=None)
    title: Optional[str] = field(default=None)


@dataclass
class ColumnValue:
    value: Optional[str] = field(default=None)
    text: Optional[str] = field(default=None)
    type: Optional[str] = field(default=None)
    column: Optional[Column] = field(default=None)


@dataclass
class Group:
    id: Optional[str] = field(default=None)
    title: Optional[str] = field(default=None)


@dataclass
class Item:
    id: Optional[str] = field(default=None)
    state: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    updated_at: Optional[str] = field(default=None)
    group: Optional[Group] = field(default=None)
    subitems: Optional[List["Item"]] = field(default_factory=list)
    parent_item: Optional["Item"] = field(default=None)  # only relevant for subitems
    column_values: Optional[List[ColumnValue]] = field(default_factory=list)


@dataclass
class CreatedItem:
    id: Optional[str] = field(default=None)


@dataclass
class User:
    name: Optional[str] = field(default=None)
    id: Optional[str] = field(default=None)


@dataclass
class Update:
    id: Optional[str] = field(default=None)
    text_body: Optional[str] = field(default=None)
    item_id: Optional[str] = field(default=None)
    created_at: Optional[str] = field(default=None)
    updated_at: Optional[str] = field(default=None)
    creator: Optional[User] = field(default=None)


@dataclass
class ItemsPage:
    cursor: Optional[str] = field(default=None)
    items: Optional[List[Item]] = field(default_factory=list)


@dataclass
class Complexity:
    query: Optional[int] = field(default=None)
    after: Optional[int] = field(default=None)


@dataclass
class ActivityLog:
    id: str
    account_id: str
    created_at: str
    data: str
    entity: str
    event: str
    user_id: str


@dataclass
class Board:
    name: Optional[str] = field(default=None)
    items_page: Optional[ItemsPage] = field(default=None)
    updates: Optional[List[Update]] = field(default_factory=list)
    activity_logs: Optional[List[ActivityLog]] = field(default_factory=list)


@dataclass
class Data:
    complexity: Optional[Complexity] = field(default=None)
    boards: Optional[List[Board]] = field(default_factory=list)
    items: Optional[List[Item]] = field(default_factory=list)
    next_items_page: Optional[ItemsPage] = field(default=None)
    items_page_by_column_values: Optional[ItemsPage] = field(default=None)
    create_item: Optional[CreatedItem] = field(default=None)


@dataclass
class MondayApiResponse:
    data: Data
    account_id: int