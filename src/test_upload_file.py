import os
from datetime import datetime
from monday_sdk import MondayClient

# Configuration
BOARD_ID = 18392575661

# Column IDs from the board
ARTIST_COLUMN_ID = "text_mkyr4ms"
UPLOAD_DATE_COLUMN_ID = "date_mkyr4e14"
FILE_COLUMN_ID = "file_mkyr6m1h"


def main():
    # Get API token from environment variable
    api_token = os.getenv("MONDAY_TOKEN")
    if not api_token:
        print("Error: MONDAY_TOKEN environment variable is not set")
        return

    # Initialize the client
    client = MondayClient(api_token)

    # Get user input
    track_name = input("Enter track name: ").strip()
    if not track_name:
        print("Error: Track name cannot be empty")
        return

    artist_name = input("Enter artist name: ").strip()
    if not artist_name:
        print("Error: Artist name cannot be empty")
        return

    file_path = input("Enter path to local file: ").strip()
    if not file_path:
        print("Error: File path cannot be empty")
        return

    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return

    # Get the first group from the board
    print("\nFetching board information...")
    board_response = client.boards.fetch_boards_by_id(BOARD_ID)
    
    if not board_response.data.boards:
        print("Error: Board not found")
        return
    
    board = board_response.data.boards[0]
    if not board.groups:
        print("Error: No groups found in the board")
        return
    
    group_id = board.groups[0].id
    print(f"Using group: {board.groups[0].title} (id: {group_id})")

    # Create the item with track name, artist, and upload date
    print(f"\nCreating item '{track_name}'...")
    now = datetime.now()
    column_values = {
        ARTIST_COLUMN_ID: artist_name,
        UPLOAD_DATE_COLUMN_ID: {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S")
        }
    }
    
    create_response = client.items.create_item(
        board_id=BOARD_ID,
        group_id=group_id,
        item_name=track_name,
        column_values=column_values
    )
    
    item_id = create_response.data.create_item.id
    print(f"Item created successfully! Item ID: {item_id}")

    # Upload the file to the file column
    print(f"\nUploading file '{os.path.basename(file_path)}'...")
    upload_response = client.items.upload_file_to_column(
        item_id=item_id,
        column_id=FILE_COLUMN_ID,
        file_path=file_path,
        mimetype="audio/mp4"
    )
    
    print("File uploaded successfully!")
    print(f"Asset info: {upload_response}")


if __name__ == "__main__":
    main()
