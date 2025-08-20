from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Column:
    id: Optional[str] = field(default=None)
    title: Optional[str] = field(default=None)
    type: Optional[str] = field(default=None)


@dataclass
class ColumnValue:
    value: Optional[str] = field(default=None)
    text: Optional[str] = field(default=None)
    type: Optional[str] = field(default=None)
    column: Optional[Column] = field(default=None)
    display_value: Optional[str] = field(default=None)


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
class Workspace:
    name: Optional[str] = field(default=None)


@dataclass
class DocumentBlock:
    type: Optional[str] = field(default=None)
    content: Optional[str] = field(default=None)
    position: Optional[float] = field(default=None)
    updated_at: Optional[str] = field(default=None)


@dataclass
class Document:
    id: Optional[str] = field(default=None)
    created_at: Optional[str] = field(default=None)
    created_by: Optional[User] = field(default=None)
    doc_folder_id: Optional[str] = field(default=None)
    doc_kind: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    url: Optional[str] = field(default=None)
    workspace: Optional[Workspace] = field(default=None)
    workspace_id: Optional[str] = field(default=None)
    object_id: Optional[str] = field(default=None)
    settings: Optional[str] = field(default=None)
    blocks: Optional[List[DocumentBlock]] = field(default_factory=list)


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
    id: Optional[str] = field(default=None)
    name: Optional[str] = field(default=None)
    items_page: Optional[ItemsPage] = field(default=None)
    updates: Optional[List[Update]] = field(default_factory=list)
    activity_logs: Optional[List[ActivityLog]] = field(default_factory=list)
    columns: Optional[List[Column]] = field(default_factory=list)
    groups: Optional[List[Group]] = field(default_factory=list)


@dataclass
class Data:
    complexity: Optional[Complexity] = field(default=None)
    boards: Optional[List[Board]] = field(default_factory=list)
    items: Optional[List[Item]] = field(default_factory=list)
    next_items_page: Optional[ItemsPage] = field(default=None)
    items_page_by_column_values: Optional[ItemsPage] = field(default=None)
    create_item: Optional[CreatedItem] = field(default=None)
    docs: Optional[List[Document]] = field(default_factory=list)


@dataclass
class MondayApiResponse:
    data: Data
    account_id: Optional[int] = field(default=None)