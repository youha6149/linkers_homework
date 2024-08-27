from indexing.indexing import InvertedIndexManager
from utils.csv_downloader import CsvDownloader
from utils.csv_loader import load_csv


def create_inverted_index(
    csv_file_path: str = "./address/zenkoku.csv",
    inverted_index_file: str = "./db/inverted_index.pkl",
) -> None:
    """転置インデックスを作成してファイルに保存する"""
    try:
        inverted_index_manager = InvertedIndexManager()
        downloader = CsvDownloader()
        downloader.download()
        downloader.extract()

        csv_data = load_csv(csv_file_path)

        inverted_index_manager.build(csv_data)
        inverted_index_manager.save(inverted_index_file)

    except Exception as e:
        print(f"Error: {e}")
        return


def search_inverted_index(
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
        matching_lines = inverted_index_manager.search(query)

        if not matching_lines:
            print("該当する住所が見つかりませんでした。")
            return

        for line in matching_lines:
            print(f"{line[0]} {line[1]}")

    except Exception as e:
        print(f"Error: {e}")
        return

    print(f"検索結果: {len(matching_lines)} 件")
