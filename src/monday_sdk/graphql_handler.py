import dacite
import requests
import json
import time

from .constants import API_URL, TOKEN_HEADER, DEFAULT_MAX_RETRY_ATTEMPTS
from .types import MondayApiResponse
from .exceptions import MondayQueryError


class MondayGraphQL:
    """
    GraphQL client that handles API interactions, response serialization, and error handling.
    """

    def __init__(self, token: str, headers: dict, debug_mode: bool = False, max_retry_attempts: int = DEFAULT_MAX_RETRY_ATTEMPTS):
        self.endpoint = API_URL
        self.token = token
        self.headers = headers
        self.debug_mode = debug_mode
        self.max_retry_attempts = max_retry_attempts

    def execute(self, query: str) -> MondayApiResponse:
        """
        Executes a GraphQL query and handles errors and rate limits.

        Args:
            query (str): The GraphQL query to execute.

        Returns:
            MondayApiResponse: The deserialized response from the Monday API.
        """
        current_attempt = 0
        last_error = None
        last_status_code = None

        while current_attempt < self.max_retry_attempts:

            if self.debug_mode:
                print(f"[debug_mode] about to execute query: {query}")

            try:
                response = self._send(query)

                if self.debug_mode:
                    print(f"[debug_mode] response: {response}")

                if response.status_code == 429:
                    print("Rate limit exceeded, response code 429 - sleeping for 30 seconds")
                    time.sleep(30)
                    current_attempt += 1
                    continue

                response.raise_for_status()
                response_data = response.json()

                if response_data.get("error_code") == "ComplexityException":
                    time.sleep(2)
                    print("ComplexityException: retrying query")
                    current_attempt += 1
                    continue

                if "errors" in response_data:
                    raise MondayQueryError(response_data["errors"][0]["message"], response_data["errors"])

                try:
                    serialized_result = dacite.from_dict(data_class=MondayApiResponse, data=response_data)
                    return serialized_result

                except dacite.DaciteError as e:
                    print(f"Error while deserializing response: {e}")
                    raise MondayQueryError("Error while deserializing response", response_data)

            except (requests.HTTPError, json.JSONDecodeError, MondayQueryError) as e:
                print(f"Error while executing query: {e}")
                last_error = e
                if hasattr(e, 'response') and e.response is not None:
                    last_status_code = e.response.status_code
                current_attempt += 1

        # All retries exhausted - raise appropriate error based on the last failure
        if last_status_code == 504:
            raise Exception(
                f"Monday API server encountered an internal error (HTTP 504 Gateway Timeout) "
                f"for {self.max_retry_attempts} consecutive attempts. The server was unable to process "
                f"the request within the timeout period. Please try again later or contact support "
                f"if the issue persists."
            )
        elif last_status_code is not None:
            raise Exception(
                f"Monday API request failed with HTTP {last_status_code} after {self.max_retry_attempts} attempts. "
                f"Error: {str(last_error)}"
            )
        else:
            raise Exception(
                f"Monday API request failed after {self.max_retry_attempts} attempts. "
                f"Error: {str(last_error)}"
            )

    def _send(self, query: str):
        payload = {"query": query}
        headers = self.headers.copy()

        if self.token is not None:
            headers[TOKEN_HEADER] = self.token

        return requests.request("POST", self.endpoint, headers=headers, json=payload)