import csv


def load_csv(csv_file_path: str, encoding: str = "shift-jis", errors: str = "ignore"):
    """CSVファイルを読み込み、リスト形式で返す"""
    try:
        with open(csv_file_path, "r", encoding=encoding, errors=errors) as file:
            reader = csv.DictReader(file)
            l = [row for row in reader]
            return l

    except FileNotFoundError:
        raise FileNotFoundError(f"CSVファイルが見つかりません: {csv_file_path}")

    except Exception as e:
        raise Exception(f"CSVファイルの読み込み中に予期しないエラーが発生しました: {e}")
