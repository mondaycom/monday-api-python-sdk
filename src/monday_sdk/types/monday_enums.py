from __future__ import annotations

from enum import Enum


class ColumnType(Enum):
    AUTO_NUMBER = "auto_number"  # Number items according to their order in the group/board
    BOARD_RELATION = "board_relation"  # Link items between boards
    BUTTON = "button"  # Trigger automations or integrations from a button
    CHECKBOX = "checkbox"  # Check off items and see what's done at a glance
    COUNTRY = "country"  # Choose a country
    COLOR_PICKER = "color_picker"  # Manage a design system using a color palette
    CREATION_LOG = "creation_log"  # Add the item's creator and creation date automatically
    DATE = "date"  # Add dates like deadlines to ensure you never drop the ball
    DEPENDENCY = "dependency"  # Set up dependencies between items in the board
    DROPDOWN = "dropdown"  # Create a dropdown list of options
    EMAIL = "email"  # Email team members and clients directly from your board
    FILE = "file"  # Add files & docs to your item
    FORMULA = "formula"  # Computed values from other columns
    HOUR = "hour"  # Add times to manage and schedule tasks, shifts and more
    ITEM_ID = "item_id"  # Show a unique ID for each item
    LAST_UPDATED = "last_updated"  # Add the person that last updated the item and the date
    LINK = "link"  # Simply hyperlink to any website
    LOCATION = "location"  # Place multiple locations on a geographic map
    LONG_TEXT = "long_text"  # Add large amounts of text without changing column width
    MIRROR = "mirror"  # Mirror values from a connected board
    NUMBERS = "numbers"  # Add revenue, costs, time estimations and more
    PEOPLE = "people"  # Assign people to improve team work
    PHONE = "phone"  # Call your contacts directly from monday.com
    PROGRESS = "progress"  # Show progress by combining status columns in a battery
    PULSE_ID = "pulse_id"  # Legacy alias for the item-id column
    PULSE_LOG = "pulse_log"  # Activity log for the item
    PULSE_UPDATED_VALUE = "pulse_updated_value"  # Last-updated value summary for the item
    RATING = "rating"  # Rate or rank anything visually
    STATUS = "status"  # Get an instant overview of where things stand
    SUBTASKS = "subtasks"  # Manage subitems on the row
    TEAM = "team"  # Assign a full team to an item
    TAGS = "tags"  # Add tags to categorize items across multiple boards
    TEXT = "text"  # Add textual information e.g. addresses, names or keywords
    TIMELINE = "timeline"  # Visually see a breakdown of your team's workload by time
    TIME_TRACKING = "time_tracking"  # Easily track time spent on each item, group, and board
    VOTE = "vote"  # Vote on an item e.g. pick a new feature or a favorite lunch place
    WEEK = "week"  # Select the week on which each item should be completed
    WORLD_CLOCK = "world_clock"  # Keep track of the time anywhere in the world

    @property
    def is_readonly(self) -> bool:
        """True if this column type cannot be written via ``column_values`` on
        ``change_column_value`` / ``change_multiple_column_values`` mutations.

        Includes system-managed columns (creation_log, last_updated,
        auto_number, pulse_*, item_id), computed columns (mirror, formula,
        progress), UI-only columns (button), and columns that require a
        dedicated mutation rather than column_values (file uploads,
        board_relation, dependency, subtasks).

        Note: ``people`` / ``multiple-person`` / ``location`` are NOT in this
        set — they are writable via column_values but require specific JSON
        shapes (people IDs, lat/lng) rather than free-text input.
        """
        return self in _READONLY_COLUMN_TYPES

    @property
    def is_writable(self) -> bool:
        """Inverse of :attr:`is_readonly`."""
        return not self.is_readonly


_READONLY_COLUMN_TYPES: frozenset[ColumnType] = frozenset(
    {
        ColumnType.AUTO_NUMBER,
        ColumnType.BOARD_RELATION,
        ColumnType.BUTTON,
        ColumnType.CREATION_LOG,
        ColumnType.DEPENDENCY,
        ColumnType.FILE,
        ColumnType.FORMULA,
        ColumnType.ITEM_ID,
        ColumnType.LAST_UPDATED,
        ColumnType.MIRROR,
        ColumnType.PROGRESS,
        ColumnType.PULSE_ID,
        ColumnType.PULSE_LOG,
        ColumnType.PULSE_UPDATED_VALUE,
        ColumnType.SUBTASKS,
    }
)


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


class ItemsOrderByDirection(Enum):
    """Direction for ordering items"""

    ASC = "asc"
    DESC = "desc"
