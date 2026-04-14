"""Tests for propagating Monday ``request_id`` through GraphQL errors."""
import unittest
from unittest.mock import MagicMock, patch

from monday_sdk.exceptions import MondayQueryError
from monday_sdk.graphql_errors import (
    extract_monday_request_id_from_body,
    extract_monday_request_id_from_response,
    throw_monday_error,
    update_retry_context_from_exception,
)
from monday_sdk.graphql_handler import MondayGraphQL


class TestExtractRequestId(unittest.TestCase):
    def test_top_level_extensions(self):
        body = {
            "errors": [{"message": "Internal server error"}],
            "extensions": {"request_id": "abc-123"},
        }
        self.assertEqual(extract_monday_request_id_from_body(body), "abc-123")

    def test_per_error_extensions_fallback(self):
        body = {
            "errors": [
                {
                    "message": "boom",
                    "extensions": {"request_id": "err-rid"},
                }
            ],
        }
        self.assertEqual(extract_monday_request_id_from_body(body), "err-rid")

    def test_body_extensions_preferred_over_header(self):
        resp = MagicMock()
        resp.headers = {"x-request-id": "from-header"}
        resp.json.return_value = {"extensions": {"request_id": "from-body"}}
        self.assertEqual(extract_monday_request_id_from_response(resp), "from-body")

    def test_header_used_when_body_has_no_request_id(self):
        resp = MagicMock()
        resp.headers = {"x-request-id": "header-only"}
        resp.json.return_value = {"errors": [{"message": "x"}]}
        self.assertEqual(extract_monday_request_id_from_response(resp), "header-only")


class TestUpdateRetryContextFromException(unittest.TestCase):
    def test_monday_query_error_sets_request_id_only(self):
        exc = MondayQueryError("x", [], request_id="rid-a")
        status, rid = update_retry_context_from_exception(exc, None, None, None)
        self.assertIsNone(status)
        self.assertEqual(rid, "rid-a")

class TestThrowMondayError(unittest.TestCase):
    def test_raises_with_body_message_and_request_id(self):
        body = {
            "errors": [{"message": "Internal server error"}],
            "extensions": {"request_id": "rid-1"},
        }
        with self.assertRaises(MondayQueryError) as ctx:
            throw_monday_error(body)
        self.assertEqual(ctx.exception.request_id, "rid-1")
        self.assertEqual(ctx.exception.original_errors, body["errors"])
        self.assertIn("Internal server error", str(ctx.exception))

    def test_optional_message_override(self):
        body = {"errors": [{"message": "ignored"}], "extensions": {"request_id": "r2"}}
        with self.assertRaises(MondayQueryError) as ctx:
            throw_monday_error(body, message="Custom client message")
        self.assertIn("Custom client message", str(ctx.exception))
        self.assertIn('request_id="r2"', str(ctx.exception))

    def test_deserialization_style_original_errors(self):
        body = {"data": {}, "extensions": {"request_id": "r3"}}
        with self.assertRaises(MondayQueryError) as ctx:
            throw_monday_error(
                body,
                message="Error while deserializing response",
                original_errors=body,
            )
        self.assertIs(ctx.exception.original_errors, body)
        self.assertEqual(ctx.exception.request_id, "r3")

    def test_non_dict_body_raises_type_error(self):
        with self.assertRaises(TypeError):
            throw_monday_error([])  # not a dict


class TestMondayQueryError(unittest.TestCase):
    def test_message_includes_request_id(self):
        err = MondayQueryError("Internal server error", [], request_id="rid-9")
        self.assertEqual(err.request_id, "rid-9")
        self.assertIn('request_id="rid-9"', str(err))


class TestMondayGraphQLExecute(unittest.TestCase):
    @patch("monday_sdk.graphql_handler.requests.request")
    def test_final_exception_includes_request_id_after_retries(self, mock_request):
        payload = {
            "errors": [{"message": "Internal server error"}],
            "extensions": {"request_id": "support-me-42"},
        }
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.headers = {}
        mock_resp.json.return_value = payload
        mock_request.return_value = mock_resp

        client = MondayGraphQL(token="t", headers={}, max_retry_attempts=2)

        with self.assertRaises(Exception) as ctx:
            client.execute("{ __typename }")

        msg = str(ctx.exception)
        self.assertIn("Internal server error", msg)
        self.assertIn('request_id="support-me-42"', msg)
        self.assertIn("monday.com support", msg)
        self.assertEqual(mock_request.call_count, 2)


if __name__ == "__main__":
    unittest.main()
