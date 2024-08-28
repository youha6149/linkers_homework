import os
import pickle
from collections import defaultdict

from indexing.tokenizer import Tokenizer


class InvertedIndex:
    """転置インデックスを作成・保存・読込・検索を行うクラス"""

    def __init__(self):
        # memo: すでに作成済みの転置インデックスが存在する場合は明示的にloadを実行して上書きする
        self.inverted_index = defaultdict(set)

    def build(self, raw: list[dict]) -> None:
        """CSVのリスト辞書から転置インデックスを構築"""
        search_keys = [
            "都道府県",
            "市区町村",
            "町域",
            "京都通り名",
            "字丁目",
            "事業所名",
            "事業所住所",
        ]

        try:
            tokenizer = Tokenizer()
            for row in raw:
                full_address = "".join(
                    filter(
                        None,
                        (row[key] for key in search_keys),
                    )
                )
                row_data = (row["郵便番号"], full_address)

                if full_address:
                    normalized_address = tokenizer.normalize_key(full_address)
                    for part in [row[key] for key in search_keys]:
                        if part and len(part) == 1:
                            normalized_part = tokenizer.normalize_key(part)
                            ngrams_part = tokenizer.create_2gram(normalized_part)
                            for n in ngrams_part:
                                self.inverted_index[n].add(row_data)

                    ngrams = tokenizer.create_2gram(normalized_address)
                    for ngram in ngrams:
                        self.inverted_index[ngram].add(row_data)

        except Exception as e:
            raise Exception(
                f"転置インデックスデータの構築中に予期しないエラーが発生しました: {e}"
            )

    def save(self, filename: str) -> None:
        """転置インデックスをpickleファイルに保存"""
        try:
            if not self.inverted_index:
                raise ValueError(
                    "転置インデックスデータが空です。\n転置インデックスファイルが存在する場合、loadメソッドを実行してください。"
                )

            os.makedirs(os.path.dirname(filename), exist_ok=True)

            with open(filename, "wb") as file:
                pickle.dump(self.inverted_index, file)

        except ValueError as e:
            raise ValueError(e)

        except FileNotFoundError:
            raise FileNotFoundError(
                f"転置インデックスファイルが見つかりません: {filename}"
            )

        except Exception as e:
            raise Exception(
                f"転置インデックスデータの保存中に予期しないエラーが発生しました: {e}"
            )

    def load(self, filename: str) -> None:
        """pickleファイルから転置インデックスデータを読み込む"""
        try:
            with open(filename, "rb") as file:
                self.inverted_index = pickle.load(file)

        except FileNotFoundError:
            raise FileNotFoundError(
                f"転置インデックスファイルが見つかりません: {filename}"
            )

        except Exception as e:
            raise Exception(
                f"転置インデックスファイルの読み込み中に予期しないエラーが発生しました: {e}"
            )

    def search(self, query: str) -> set:
        """クエリをトークン化し、転置インデックスから検索"""
        try:
            tokenizer = Tokenizer()
            # memo:「大阪市梅田」のような市区町村が抜けたクエリの場合は検索結果が0件になる
            normalized_query = tokenizer.normalize_key(query)
            query_ngrams = tokenizer.create_2gram(normalized_query)

            result_sets = [
                self.inverted_index.get(ngram, set()) for ngram in query_ngrams
            ]

            if result_sets:
                return set.intersection(*result_sets)
            return set()

        except Exception as e:
            raise Exception(f"検索処理中に予期しないエラーが発生しました: {e}")
