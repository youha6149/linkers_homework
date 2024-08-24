import csv

from indexing import InvertedIndexManager
from utils import create_2gram, display_results, normalize_key


def main():
    csv_file_path = "./address/zenkoku.csv"
    inverted_index_file = "inverted_index.pkl"
    inverted_index_manager = InvertedIndexManager()
    try:

        with open(csv_file_path, "r", encoding="shift-jis", errors="ignore") as file:
            reader = csv.DictReader(file)
            inverted_index_manager.build(reader)
            inverted_index_manager.save(inverted_index_file)

    except FileNotFoundError:
        print(f"Error: CSVファイルが見つかりません: {csv_file_path}")
        return

    except Exception as e:
        print(f"Error: {e}")
        return

    # 検索処理
    query = input("検索したい地名や住所の一部を入力してください: ")
    query_params = [normalize_key(q) for q in create_2gram(query)]

    inverted_index_manager.load(inverted_index_file)
    matching_lines = inverted_index_manager.search(query_params)

    with open(csv_file_path, "r", encoding="shift-jis", errors="ignore") as file:
        reader = csv.DictReader(file)
        display_results(reader, matching_lines)

    print(f"検索結果: {len(matching_lines)} 件")


if __name__ == "__main__":
    main()
