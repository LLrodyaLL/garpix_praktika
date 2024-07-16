import pandas as pd
import json
import sys
from itertools import combinations


def find_minimal_unique_columns(data):
    df = pd.DataFrame(data)
    if df.empty:
        return []

    columns = df.columns.tolist()
    n_rows = len(df)

    for r in range(1, len(columns) + 1):
        for subset in combinations(columns, r):
            if df[list(subset)].drop_duplicates().shape[0] == n_rows:
                return list(subset)

    return columns


def main(json_string):
    data = json.loads(json_string)
    if not data:
        raise ValueError("The JSON data is empty.")

    unique_columns = find_minimal_unique_columns(data)
    if not unique_columns:
        return pd.DataFrame()

    # Создание DataFrame только с колонкой "Признак"
    df = pd.DataFrame({"Признак": unique_columns})
    df.index = df.index + 1

    # Сохранение результатов в CSV файл
    csv_filename = 'result.csv'
    try:
        df.to_csv(csv_filename, index=True, header=False, sep='\t', encoding='utf-8', index_label='Номер')
        print(f"Результаты сохранены в файл: {csv_filename}")
    except Exception as e:
        print(f"Ошибка при сохранении в CSV файл: {e}")
        sys.exit(1)

    return df


if __name__ == "__main__":
    if len(sys.argv) > 1:
        json_file_path = sys.argv[1]
        try:
            with open(json_file_path, 'r', encoding='utf-8') as file:
                json_input = file.read()
                if not json_input.strip():  # Проверка на пустоту файла
                    raise ValueError("The JSON file is empty.")
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            sys.exit(1)

        result = main(json_input)
        print(result)
    else:
        print("Usage: python app.py <path_to_json_file>")
