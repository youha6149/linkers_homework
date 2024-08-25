import csv
from pathlib import Path

from indexing import InvertedIndexManager


def create_inverted_index(
    csv_file_path: str = "./address/zenkoku.csv",
    inverted_index_file: str = "./db/inverted_index.pkl",
) -> None:
    """転置インデックスを作成してファイルに保存する"""
    try:
        inverted_index_manager = InvertedIndexManager()

        if not Path(csv_file_path).exists():
            raise FileNotFoundError(f"CSVファイルが見つかりません: {csv_file_path}")

        with open(csv_file_path, "r", encoding="shift-jis", errors="ignore") as file:
            reader = csv.DictReader(file)
            inverted_index_manager.build(reader)
            inverted_index_manager.save(inverted_index_file)

    except Exception as e:
        print(f"Error: {e}")
        return


def search_inverted_index(
    inverted_index_file: str = "./db/inverted_index_row_data.pkl",
) -> None:
    """転置インデックスを使用して検索を行う"""
    query = input("検索したい地名や住所の一部を入力してください: ").strip()

    if not query:
        print("Error: クエリが空です。適切な地名や住所を入力してください。")
        return

    inverted_index_manager = InvertedIndexManager()

    try:
        inverted_index_manager.load(inverted_index_file)
        matching_lines = inverted_index_manager.search(query)

        if not matching_lines:
            print("該当する住所が見つかりませんでした。")
            return

        for line in matching_lines:
            print(
                f"{line[0]} {line[1]} {line[2]} {line[3]} "
                f"{line[4]} {line[5]} {line[6]} {line[7]}"
            )

    except Exception as e:
        print(f"Error: {e}")
        return

    print(f"検索結果: {len(matching_lines)} 件")


def main():

    # 転置インデックスの作成
    create_inverted_index()

    # 検索処理
    search_inverted_index()


if __name__ == "__main__":
    main()
