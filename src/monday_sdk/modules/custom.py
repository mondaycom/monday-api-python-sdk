from ..graphql_handler import MondayGraphQL


class CustomModule(MondayGraphQL):
    def execute_custom_query(self, custom_query):
        return self.execute(custom_query)
