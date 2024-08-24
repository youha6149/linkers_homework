import csv

from indexing import InvertedIndexManager
from utils import create_2gram, display_results, normalize_key


def main():
    csv_file_path = "./address/zenkoku.csv"
    inverted_index_file = "inverted_index.pkl"

    # 転置インデックスの作成と保存
    try:
        with open(csv_file_path, "r", encoding="shift-jis", errors="ignore") as file:
            reader = csv.DictReader(file)
            inverted_index = build_inverted_index(reader)
            normalized_index = {
                normalize_key(key): value for key, value in inverted_index.items()
            }
            save_inverted_index(inverted_index_file, normalized_index)

    except FileNotFoundError:
        print(f"Error: CSVファイルが見つかりません: {csv_file_path}")
        return

    except Exception as e:
        print(f"Error: {e}")
        return

    # 検索処理
    query = input("検索したい地名や住所の一部を入力してください: ")
    inverted_index = load_inverted_index(inverted_index_file)
    matching_lines = search_inverted_index(inverted_index, query)

    display_results(csv_file_path, matching_lines)
    print(f"検索結果: {len(matching_lines)} 件")


if __name__ == "__main__":
    main()
