# monday-python-sdk

A Python SDK for interacting with Monday's GraphQL API.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Authentication](#authentication)
- [API Methods](#api-methods)
- [Examples](#examples)

## Installation

To install the SDK, use pip:

```bash
pip install monday-python-sdk
```
## Usage

### Authentication
To use the SDK, you need to authenticate with your Monday API token:

```python
from monday_sdk import MondayClient

client = MondayClient(api_token='your_api_token')
```

You can also enable debug mode to see the raw API requests and responses:
```python
client = MondayClient(api_token='your_api_token', debug=True)
```


## API Methods

### Get Boards
```python
boards = client.boards.fetch_boards()
```

### Get Board Items
```python
items = client.boards.fetch_all_items_by_board_id(board_id='your_board_id')
```

### Create Item
```python
item = client.items.create_item(board_id='your_board_id', item_name='New Item', column_values={'status': 'Done'})
```

### Create Update
```python
update = client.updates.create_update(item_id='your_item_id', body='This is an update')
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
from monday_sdk import MondayClient, Item

client = MondayClient(api_token='your_api_token')

# Fetch the raw response data
items: List[Item] = client.Boards.fetch_all_items_by_board_id(board_id='your_board_id')

# Access specific fields using the deserialized objects
first_item_name = items[0].name
```
By using these types, you can ensure type safety and better code completion support in your IDE, making your work with the Monday API more efficient and error-free.
Note, some methods return a `MondayApiResponse` object while others return a specific data type directly. Be sure to check the method definition hints for the expected return type.