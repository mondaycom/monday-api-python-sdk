import json
import unittest

from monday_sdk.query_templates import (
    change_simple_column_value_query,
    create_item_query,
    create_subitem_query,
    get_item_query,
)
from monday_sdk.utils import format_param_value


class QueryStringTests(unittest.TestCase):
    def test_strings_round_trip(self):
        for value in ('A "quoted" name', 'line one\nline two', r'C:\new\file', 'café'):
            with self.subTest(value=value):
                self.assertEqual(json.loads(format_param_value(value)), value)

    def test_queries_escape_user_text(self):
        for value in ('A "quoted" name', 'line one\nline two', r'C:\new\file'):
            cases = (
                (create_item_query(1, 'group', value, {}, False), 'item_name'),
                (create_subitem_query(1, value, {}, False), 'item_name'),
                (change_simple_column_value_query(1, 2, 'text', value), 'value'),
            )
            for query, argument in cases:
                with self.subTest(value=value, argument=argument, query=query):
                    self.assertIn(f'{argument}: {json.dumps(value)}', query)
            self.assertIn(json.dumps(value), get_item_query(1, 'text', value, 10))

    def test_boolean_literals(self):
        self.assertEqual(format_param_value(True), 'true')
        self.assertEqual(format_param_value(False), 'false')
