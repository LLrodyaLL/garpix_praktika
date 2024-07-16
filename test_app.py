import unittest
import pandas as pd
import json
from app import find_minimal_unique_columns, main


class TestFindMinimalUniqueColumns(unittest.TestCase):

    def setUp(self):
        self.data1 = [
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Bob", "age": 25},
            {"id": 3, "name": "Charlie", "age": 35}
        ]

        self.data2 = [
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Alice", "age": 25},
            {"id": 3, "name": "Bob", "age": 30},
            {"id": 4, "name": "Charlie", "age": 25},
        ]

        self.data3 = [
            {"id": 1, "name": "Alice", "age": 30, "city": "New York"},
            {"id": 2, "name": "Bob", "age": 25, "city": "Los Angeles"},
            {"id": 3, "name": "Charlie", "age": 35, "city": "Chicago"},
            {"id": 4, "name": "Alice", "age": 30, "city": "Miami"},
            {"id": 5, "name": "Bob", "age": 25, "city": "Dallas"},
        ]

    def test_find_minimal_unique_columns(self):
        result = find_minimal_unique_columns(self.data1)
        self.assertEqual(result, ['id'])

    def test_find_minimal_unique_columns_with_duplicates(self):
        result = find_minimal_unique_columns(self.data2)
        self.assertIn('id', result)
        self.assertTrue(len(result) >= 1)

    def test_find_minimal_unique_columns_multiple_columns(self):
        result = find_minimal_unique_columns(self.data3)
        self.assertIn('id', result)
        self.assertTrue(len(result) >= 1)


class TestMainFunction(unittest.TestCase):

    def test_main_function(self):
        json_data = json.dumps([
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Bob", "age": 25},
            {"id": 3, "name": "Charlie", "age": 35}
        ])

        expected_output = pd.DataFrame({"Признак": ["id"]})
        expected_output.index = expected_output.index + 1

        result_df = main(json_data)
        pd.testing.assert_frame_equal(result_df, expected_output)

    def test_main_function_empty_json(self):
        empty_json_data = json.dumps([])
        with self.assertRaises(ValueError) as context:
            main(empty_json_data)
        self.assertTrue("The JSON data is empty." in str(context.exception))


if __name__ == '__main__':
    unittest.main()
