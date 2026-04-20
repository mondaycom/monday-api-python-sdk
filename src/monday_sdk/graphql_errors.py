"""Monday GraphQL API error helpers: ``request_id`` extraction and ``MondayQueryError`` raising."""
import json
from typing import Any, NoReturn, Optional, Tuple

import requests

from .exceptions import MondayQueryError


def extract_monday_request_id_from_body(data: Any) -> Optional[str]:
    """
    Monday documents ``extensions.request_id`` on the JSON root (API 2024-10+).
    Fall back to per-error extensions when present.
    """
    if not isinstance(data, dict):
        return None
    ext = data.get("extensions")
    if isinstance(ext, dict):
        rid = ext.get("request_id")
        if rid is not None and str(rid).strip():
            return str(rid)
    for err in data.get("errors") or []:
        if not isinstance(err, dict):
            continue
        eext = err.get("extensions")
        if isinstance(eext, dict):
            rid = eext.get("request_id")
            if rid is not None and str(rid).strip():
                return str(rid)
    return None


def extract_monday_request_id_from_response(response: Optional[requests.Response]) -> Optional[str]:
    """Resolve request id from JSON body (``extensions.request_id``) or response headers."""
    if response is None:
        return None
    data = None
    try:
        data = response.json()
    except (ValueError, json.JSONDecodeError):
        pass
    if isinstance(data, dict):
        rid = extract_monday_request_id_from_body(data)
        if rid:
            return rid
    header_rid = response.headers.get("x-request-id") or response.headers.get("X-Request-Id")
    if header_rid:
        return str(header_rid).strip() or None
    return None


def update_retry_context_from_exception(
    exc: BaseException,
    response: Optional[requests.Response],
    last_status_code: Optional[int],
    last_request_id: Optional[str],
) -> Tuple[Optional[int], Optional[str]]:
    """
    Derive HTTP status and Monday ``request_id`` from a failed request attempt
    for retry / final error messaging.
    """
    status_code = last_status_code
    request_id = last_request_id

    if isinstance(exc, MondayQueryError) and exc.request_id:
        request_id = exc.request_id
    elif isinstance(exc, requests.HTTPError) and exc.response is not None:
        status_code = exc.response.status_code
        rid = extract_monday_request_id_from_response(exc.response)
        if rid:
            request_id = rid
    elif isinstance(exc, json.JSONDecodeError) and response is not None:
        rid = extract_monday_request_id_from_response(response)
        if rid:
            request_id = rid

    if hasattr(exc, "response") and exc.response is not None:
        status_code = exc.response.status_code

    return status_code, request_id


def throw_monday_error(
    response_body: dict,
    message: Optional[str] = None,
    *,
    original_errors: Any = None,
) -> NoReturn:
    """
    Raise ``MondayQueryError`` from a parsed Monday API JSON object.

    Extracts ``request_id`` from ``extensions`` / per-error ``extensions`` when
    present (API version 2024-10+). By default, ``original_errors`` is the
    ``errors`` list from the body; pass ``original_errors`` explicitly when the
    payload is not a standard GraphQL error response (e.g. deserialization
    failures where the full body should be preserved).

    Args:
        response_body: Parsed JSON from ``response.json()``.
        message: If set, used as the exception message. Otherwise the first
            GraphQL error's ``message``, or a generic fallback if missing.
        original_errors: Optional override for ``MondayQueryError.original_errors``.
    """
    if not isinstance(response_body, dict):
        raise TypeError("response_body must be a dict")

    request_id = extract_monday_request_id_from_body(response_body)

    if original_errors is not None:
        err_payload = original_errors
    else:
        err_payload = response_body.get("errors")
        if not isinstance(err_payload, list):
            err_payload = []

    if message is None:
        if isinstance(err_payload, list) and err_payload:
            first = err_payload[0]
            if isinstance(first, dict) and first.get("message"):
                message = str(first["message"])
            else:
                message = "Monday API returned errors"
        else:
            message = "Monday API returned errors"

    raise MondayQueryError(message, err_payload, request_id=request_id)
