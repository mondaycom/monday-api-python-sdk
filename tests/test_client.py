"""Tests for the headers MondayClient sends with every request."""
import unittest

from monday_sdk.client import BASE_HEADERS, MondayClient
from monday_sdk.constants import API_VERSION


class MondayClientHeadersTest(unittest.TestCase):
    def test_no_headers_gives_base_headers(self):
        client = MondayClient(token="token")
        self.assertEqual(client._graphql_client.headers, BASE_HEADERS)

    def test_custom_headers_keep_api_version(self):
        client = MondayClient(token="token", headers={"X-Custom": "value"})
        self.assertEqual(
            client._graphql_client.headers,
            {"API-Version": API_VERSION, "X-Custom": "value"},
        )

    def test_caller_api_version_wins(self):
        client = MondayClient(token="token", headers={"API-Version": "2025-10", "X-Custom": "value"})
        self.assertEqual(
            client._graphql_client.headers,
            {"API-Version": "2025-10", "X-Custom": "value"},
        )

    def test_base_headers_and_caller_headers_are_not_mutated(self):
        caller_headers = {"X-Custom": "value"}
        client = MondayClient(token="token", headers=caller_headers)
        client._graphql_client.headers["X-Other"] = "other"
        self.assertEqual(caller_headers, {"X-Custom": "value"})
        self.assertEqual(BASE_HEADERS, {"API-Version": API_VERSION})


if __name__ == "__main__":
    unittest.main()
