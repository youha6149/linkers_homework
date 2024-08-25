import csv

from indexing import InvertedIndexManager
from utils import display_results


def create_inverted_index(
    csv_file_path: str = "./address/zenkoku.csv",
    inverted_index_file: str = "./db/inverted_index.pkl",
) -> None:
    """転置インデックスを作成してファイルに保存する"""
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
        print(f"Error: 転置インデックスの作成中にエラーが発生しました: {e}")
        return


def search_inverted_index(
    csv_file_path: str = "./address/zenkoku.csv",
    inverted_index_file: str = "./db/inverted_index.pkl",
) -> None:
    """転置インデックスを使用して検索を行う"""
    query = input("検索したい地名や住所の一部を入力してください: ").strip()

    if not query:
        print("Error: クエリが空です。適切な地名や住所を入力してください。")
        return

    inverted_index_manager = InvertedIndexManager()

    try:
        inverted_index_manager.load(inverted_index_file)

    except Exception as e:
        print(f"Error: 転置インデックスの読み込み中にエラーが発生しました: {e}")
        return

    matching_lines = inverted_index_manager.search(query)

    with open(csv_file_path, "r", encoding="shift-jis", errors="ignore") as file:
        reader = csv.DictReader(file)
        display_results(reader, matching_lines)

    print(f"検索結果: {len(matching_lines)} 件")


def main():

    # 転置インデックスの作成
    create_inverted_index()

    # 検索処理
    search_inverted_index()


if __name__ == "__main__":
    main()
