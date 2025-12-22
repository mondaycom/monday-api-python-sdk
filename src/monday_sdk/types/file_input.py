from dataclasses import dataclass
from typing import Optional


@dataclass
class FileInput:
    """Represents a file to be uploaded via multipart/form-data."""
    name: str                           # The variable name in the GraphQL mutation (e.g., "file")
    file_path: str                      # Path to the file
    filename: Optional[str] = None      # Override filename (defaults to basename of file_path)
    mimetype: Optional[str] = None      # MIME type (auto-detected if not provided)

