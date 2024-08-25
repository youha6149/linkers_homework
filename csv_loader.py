import csv


def load_csv(csv_file_path: str, encoding: str = "shift-jis", errors: str = "ignore"):
    """CSVファイルを読み込み、DictReaderを返す"""
    try:
        with open(csv_file_path, "r", encoding=encoding, errors=errors) as file:
            reader = csv.DictReader(file)
            l = [row for row in reader]
            return l
    except FileNotFoundError:
        print(f"Error: CSVファイルが見つかりません: {csv_file_path}")
        return None
    except Exception as e:
        print(f"Error: CSVファイルの読み込み中にエラーが発生しました: {e}")
        return None
