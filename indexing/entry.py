import io
import sys
import traceback as tb

from indexing.indexing import InvertedIndex
from log.logger import LoggerSetup
from utils.csv_downloader import CsvDownloader
from utils.csv_loader import load_csv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8")

logger = LoggerSetup().get_logger()


def create_inverted_index(
    csv_file_path: str = "./address/zenkoku.csv",
    inverted_index_file: str = "./db/inverted_index.pkl",
) -> None:
    """転置インデックスデータを作成してファイルに保存する"""
    try:
        inverted_index = InvertedIndex()
        downloader = CsvDownloader()
        downloader.download()
        downloader.extract()

        csv_data = load_csv(csv_file_path)

        inverted_index.build(csv_data)
        inverted_index.save(inverted_index_file)

    except Exception as e:
        error_message = f"Error: 検索値不備以外のエラーは管理者までご連絡いただければ幸いです。\n{e}"
        print(error_message)
        logger.error(error_message)
        logger.error(tb.format_exc())
        return


def search_inverted_index(
    inverted_index_file: str = "./db/inverted_index.pkl",
) -> None:
    """転置インデックスデータから検索を行う"""
    try:
        query = input("検索したい地名や住所の一部を入力してください: ").strip()

        if not query:
            raise ValueError("クエリが空です。適切な地名や住所を入力してください。")

        inverted_index = InvertedIndex()

        inverted_index.load(inverted_index_file)
        matching_lines = inverted_index.search(query)

        if not matching_lines:
            raise ValueError("該当する住所が見つかりませんでした。")

        for line in matching_lines:
            print(f"{line[0]} {line[1]}")

    except Exception as e:
        error_message = f"Error: 検索値不備以外のエラーは管理者までご連絡いただければ幸いです。\n{e}"
        print(error_message)
        logger.error(error_message)
        logger.error(tb.format_exc())
        return

    print(f"検索結果: {len(matching_lines)} 件")
