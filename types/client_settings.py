from dataclasses import dataclass
from typing import Dict


@dataclass
class MondayClientSettings:
    token: str
    headers: Dict[str, str]
    debug_mode: bool
    max_retry_attempts: int
