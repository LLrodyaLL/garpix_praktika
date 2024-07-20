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

        self.data4 = []

        self.data5 = [
            {"id": 1},
            {"id": 2},
            {"id": 3}
        ]

        self.data6 = [
            {"id": 1, "name": "Alice"},
            {"id": 2, "name": "Alice"},
            {"id": 3, "name": "Alice"}
        ]

        self.data7 = [
            {"id": 1, "name": "Alice", "age": 30},
            {"id": 2, "name": "Alice", "age": 30},
            {"id": 3, "name": "Alice", "age": 30}
        ]

    def test_find_minimal_unique_columns(self):
        # Тестируем функцию на простом наборе данных
        result = find_minimal_unique_columns(self.data1)
        self.assertEqual(result, ['id'])

    def test_find_minimal_unique_columns_with_duplicates(self):
        # Тестируем функцию на наборе данных с дубликатами
        result = find_minimal_unique_columns(self.data2)
        self.assertIn('id', result)
        self.assertTrue(len(result) >= 1)

    def test_find_minimal_unique_columns_multiple_columns(self):
        # Тестируем функцию на наборе данных с несколькими столбцами
        result = find_minimal_unique_columns(self.data3)
        self.assertIn('id', result)
        self.assertTrue(len(result) >= 1)

    def test_find_minimal_unique_columns_empty_data(self):
        # Тестируем функцию на пустом наборе данных
        result = find_minimal_unique_columns(self.data4)
        self.assertEqual(result, [])

    def test_find_minimal_unique_columns_single_column(self):
        # Тестируем функцию на наборе данных с одним столбцом
        result = find_minimal_unique_columns(self.data5)
        self.assertEqual(result, ['id'])

    def test_find_minimal_unique_columns_same_values(self):
        # Тестируем функцию на наборе данных с одинаковыми значениями
        result = find_minimal_unique_columns(self.data6)
        self.assertEqual(result, ['id'])

    def test_find_minimal_unique_columns_non_unique_but_different(self):
        # Тестируем функцию на наборе данных с неуникальными значениями, но разными идентификаторами
        result = find_minimal_unique_columns(self.data7)
        self.assertEqual(result, ['id'])


class TestMainFunction(unittest.TestCase):

    def test_main_function(self):
        # Тестируем функцию main на корректных JSON данных
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
        # Тестируем функцию main на пустом JSON
        empty_json_data = json.dumps([])
        with self.assertRaises(ValueError) as context:
            main(empty_json_data)
        self.assertTrue("The JSON data is empty." in str(context.exception))

    def test_main_function_invalid_json(self):
        # Тестируем функцию main на некорректном JSON
        invalid_json_data = "Invalid JSON"
        with self.assertRaises(json.JSONDecodeError):
            main(invalid_json_data)

    def test_main_function_no_unique_columns(self):
        # Тестируем функцию main на данных без уникальных столбцов
        json_data = json.dumps([
            {"name": "Alice", "age": 30},
            {"name": "Bob", "age": 25},
            {"name": "Alice", "age": 25}
        ])

        expected_output = pd.DataFrame({"Признак": ["name", "age"]})
        expected_output.index = expected_output.index + 1

        result_df = main(json_data)
        pd.testing.assert_frame_equal(result_df, expected_output)


if __name__ == '__main__':
    unittest.main()
