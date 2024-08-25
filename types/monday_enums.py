from enum import Enum


class Operator(Enum):
    GREATER_THAN_OR_EQUALS = "greater_than_or_equals"
    LESS_THAN_OR_EQUALS = "lower_than_or_equal"


class BoardKind(Enum):
    """Board kinds"""

    PUBLIC = "public"
    PRIVATE = "private"
    SHARE = "share"


class BoardState(Enum):
    """Board available states"""

    ALL = "all"
    ACTIVE = "active"
    ARCHIVED = "archived"
    DELETED = "deleted"


class BoardsOrderBy(Enum):
    """Order to retrieve boards"""

    CREATED_AT = "created_at"
    USED_AT = "used_at"
