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

## API Methods

### Get Boards
```python
boards = client.boards.fetch_boards()
print(boards)
```
### Create Item
```python
item = client.items.create_item(board_id='your_board_id', group_id='your_group_id', item_name='New Item')
print(item)
```
## Examples

Here are some examples of how to use the SDK:

### Example 1: List all boards
```python
from monday_sdk import MondayClient

client = MondayClient(api_token='your_api_token')
boards = client.boards.fetch_boards()
for board in boards:
    print(board['name'])
```
### Example 2: Create a new item
```python
from monday_sdk import MondayClient

client = MondayClient(api_token='your_api_token')
item = client.create_item(board_id='your_board_id', item_name='New Item')
print(item)
```


# monday-python-sdk

A Python SDK for interacting with Monday's GraphQL API.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Authentication](#authentication)
- [API Methods](#api-methods)
- [Response Types](#response-types)
- [Examples](#examples)

## Installation

To install the SDK, use pip:
```python
pip install monday-python-sdk
```
## Usage

### Authentication
To use the SDK, you need to authenticate with your Monday API token:
```bash
from monday_sdk import MondayClient

client = MondayClient(api_token='your_api_token')
```
## API Methods

### Get Boards
```python
boards = client.Boards.fetch_boards()
print(boards)
```
### Create Item
```python
item = client.items.create_item(board_id='your_board_id', item_name='New Item')
print(item)
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

client = MondayClient(api_token='your_api_token')

# Fetch the raw response data
response_data = client.Boards.get_board_items(board_id='your_board_id')

# Deserialize the response data into typed objects
monday_response = dacite.from_dict(data_class=MondayApiResponse, data=response_data)

# Access specific fields using the deserialized objects
first_board = monday_response.data.boards[0]
first_item_name = first_board.items_page.items[0].name

print(f"First item name: {first_item_name}")
```
By using these types, you can ensure type safety and better code completion support in your IDE, making your work with the Monday API more efficient and error-free.

## Examples

Here are some examples of how to use the SDK:

### Example 1: List all boards
```python
from monday_sdk import MondayClient

client = MondayClient(api_token='your_api_token')
boards = client.Boards.fetch_boards()
for board in boards:
    print(board['name'])
```
### Example 2: Create a new item
```python
from monday_sdk import MondayClient

client = MondayClient(api_token='your_api_token')
item = client.items.create_item(board_id='your_board_id', item_name='New Item')
print(item)
```
### Example 3: Create an update
```python
from monday_sdk import MondayClient

client = MondayClient(api_token='your_api_token')
```