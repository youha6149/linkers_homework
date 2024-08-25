import pickle
from collections import defaultdict

from utils import create_2gram, normalize_key


class InvertedIndexManager:
    """転置インデックスを作成・検索を行うクラス"""

    def __init__(self):
        # すでに作成済みの転置インデックスが存在する場合は読み込む
        # 現状は作成済みの転置インデックスが存在しない前提
        self.inverted_index = defaultdict(set)

    def build(self, raw) -> None:
        """CSVリーダーから転置インデックスを構築"""
        try:
            for row in raw:
                address_components = [
                    row["都道府県"],
                    row["市区町村"],
                    row["町域"],
                    row["京都通り名"],
                    row["字丁目"],
                    row["事業所名"],
                    row["事業所住所"],
                ]
                row_data = (row["郵便番号"], *address_components)

                for component in address_components:
                    if component:
                        normalized_component = normalize_key(component)
                        ngrams = create_2gram(normalized_component)
                        for ngram in ngrams:
                            self.inverted_index[ngram].add(row_data)

        except Exception as e:
            raise Exception(
                f"転置インデックスの構築中に予期しないエラーが発生しました: {e}"
            )

    def save(self, filename) -> None:
        """転置インデックスをpickleファイルに保存"""
        # memo: self.inverted_indexが空の場合はエラーを返す想定
        try:
            if not self.inverted_index:
                raise ValueError("inverted_index is empty")

            with open(filename, "wb") as file:
                pickle.dump(self.inverted_index, file)

        except ValueError as e:
            raise ValueError(f"転置インデックスが空です: {e}")

        except FileNotFoundError:
            raise FileNotFoundError(
                f"転置インデックスファイルが見つかりません: {filename}"
            )

        except Exception as e:
            raise Exception(
                f"転置インデックスの保存中に予期しないエラーが発生しました: {e}"
            )

    def load(self, filename):
        """pickleファイルから転置インデックスを読み込む"""
        try:
            with open(filename, "rb") as file:
                self.inverted_index = pickle.load(file)

        except FileNotFoundError:
            raise FileNotFoundError(
                f"転置インデックスファイルが見つかりません: {filename}"
            )

        except Exception as e:
            raise Exception(
                f"転置インデックスの読み込み中に予期しないエラーが発生しました: {e}"
            )

    def search(self, query):
        """転置インデックスでクエリを検索"""
        try:
            normalized_query = normalize_key(query)
            query_ngrams = create_2gram(normalized_query)

            result_sets = [
                self.inverted_index.get(ngram, set()) for ngram in query_ngrams
            ]

            if result_sets:
                return set.intersection(*result_sets)
            return set()

        except Exception as e:
            raise Exception(f"検索処理中に予期しないエラーが発生しました: {e}")
