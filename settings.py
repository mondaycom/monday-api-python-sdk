API_URL = "https://api.monday.com/v2"
API_VERSION = "2023-10"
TOKEN_HEADER = "Authorization"
MAX_COMPLEXITY = 10000000  # Monday's API complexity limit per minute
DEBUG_MODE = True
MAX_RETRY_ATTEMPTS = 3

DEFAULTS = {
    "API_URL": "https://api.monday.com/v2",
    "API_VERSION": "v2",
    "DEFAULT_PAGE_LIMIT_ITEMS": 500,
    "DEFAULT_PAGE_LIMIT_UPDATES": 1000,
    "DEFAULT_PAGE_LIMIT_BOARDS": 50,
    "DEFAULT_PAGE_LIMIT_ACTIVITY_LOGS": 1000,
}
