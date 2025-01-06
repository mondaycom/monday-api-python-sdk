# monday-api-python-sdk

A Python SDK for interacting with Monday"s GraphQL API.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Authentication](#authentication)
- [Response Types](#response-types)

## Installation

To install the SDK, use pip:

```bash
pip install monday-api-python-sdk
```
## Authentication
To use the SDK, you need to authenticate with your Monday API token:

```python
from monday_sdk import MondayClient, MondayApiResponse, Board

client = MondayClient(token="your_token")
```

## Examples

Here are some examples of how to use the SDK:

### Example 1: Create a new item
```python
from monday_sdk import MondayClient

client = MondayClient(token="your_token")

column_values = {
    "status_column_id": "In Progress",  # Replace with your actual status column ID and value
    "date_column_id": "2025-01-06",    # Replace with your actual date column ID and date (YYYY-MM-DD format)
    "text_column_id": "Important task" # Replace with your actual text column ID and value
}

item = client.create_item(
    board_id="your_board_id", 
    group_id="your_group_id", 
    item_name="New Item", 
    column_values=column_values
)

print(item)
```
### Example 2: Create an Update and Update Column Values
```python
from monday_sdk import MondayClient, StatusColumnValue, DateColumnValue

client = MondayClient(token="your_token")

# Create an update for an item
update_response = client.updates.create_update(
    item_id="your_item_id",
    update_value="This is a new update message for the item."
)

# Change a status column value
status_response = client.items.change_status_column_value(
    board_id="your_board_id",
    item_id="your_item_id",
    column_id="status_column_id",  # Replace with the actual column ID
    value="Done"  # Replace with the desired status value
)
print(f"Status column updated: {status_response}")

# Change a date column value
date_response = client.items.change_date_column_value(
    board_id="your_board_id",
    item_id="your_item_id",
    column_id="date_column_id",
    timestamp="2025-01-06" 
)
```

## Response Types

The SDK provides structured types to help you work with API responses more effectively. These types allow you to easily access and manipulate the data returned by the API.

### Available Types

- `MondayApiResponse`: Represents the full response from a Monday API query, including data and account information.
- `Data`: Holds the core data returned from the API, such as boards, items, and complexity details.
- `Board`: Represents a Monday board, including items, updates, and activity logs.
- `Item`: Represents an item on a board, including its details and associated subitems.
- `Column`, `ColumnValue`: Represents columns and their values for an item.
- `Group`: Represents a group within a board.
- `User`: Represents a user associated with an update or activity log.
- `Update`: Represents an update on an item.
- `ActivityLog`: Represents an activity log entry on a board.
- `ItemsPage`: Represents a paginated collection of items.

### Example Usage

Here is an example of how to use these types with the SDK to deserialize API responses:
```python
from monday_sdk import MondayClient, MondayApiResponse
import dacite

client = MondayClient(token="your_token")

# Fetch the raw response data
response_data = client.boards.fetch_all_items_by_board_id(board_id="your_board_id")

# Deserialize the response data into typed objects
monday_response = dacite.from_dict(data_class=MondayApiResponse, data=response_data)

# Access specific fields using the deserialized objects
first_board = monday_response.data.boards[0]
first_item_name = first_board.items_page.items[0].name

print(f"First item name: {first_item_name}")
```
By using these types, you can ensure type safety and better code completion support in your IDE, making your work with the Monday API more efficient and error-free.
