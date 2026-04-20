class MondayError(Exception):
    pass


class MondayQueryError(MondayError):
    """
    Raised when the Monday GraphQL API returns an ``errors`` payload or when
    the response cannot be deserialized. ``request_id`` mirrors Monday's
    top-level ``extensions.request_id`` when present (API version 2024-10+).
    """

    def __init__(self, message, original_errors=None, request_id=None):
        self.original_errors = original_errors or []
        self.request_id = request_id
        if request_id:
            message = f'{message} (request_id="{request_id}")'
        super().__init__(message)
