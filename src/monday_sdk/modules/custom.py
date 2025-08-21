from ..graphql_handler import MondayGraphQL


class CustomModule:
    def __init__(self, graphql_client: MondayGraphQL):
        self.client = graphql_client
    def execute_custom_query(self, custom_query):
        return self.client.execute(custom_query)
