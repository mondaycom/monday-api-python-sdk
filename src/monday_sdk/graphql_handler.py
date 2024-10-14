import dacite
import requests
import json
import time

from .exceptions import MondayQueryError
from .constants import API_URL, TOKEN_HEADER
from .types import MondayApiResponse, MondayClientSettings


class MondayGraphQL:
    """
    GraphQL client that handles API interactions, response serialization, and error handling.
    """

    def __init__(self, settings: MondayClientSettings):
        self.endpoint = API_URL
        self.token = settings.token
        self.headers = settings.headers
        self.debug_mode = settings.debug_mode
        self.max_retry_attempts = settings.max_retry_attempts

    def execute(self, query: str) -> MondayApiResponse:
        """
        Executes a GraphQL query and handles errors and rate limits.

        Args:
            query (str): The GraphQL query to execute.

        Returns:
            MondayApiResponse: The deserialized response from the Monday API.
        """
        current_attempt = 0

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
                current_attempt += 1

    def _send(self, query: str):
        payload = {"query": query}
        headers = self.headers.copy()

        if self.token is not None:
            headers[TOKEN_HEADER] = self.token

        return requests.request("POST", self.endpoint, headers=headers, json=payload)
