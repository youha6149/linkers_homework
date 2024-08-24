import csv
import pickle
import unicodedata
from collections import defaultdict


def create_2gram(term):
    """文字列を2-gramに分割し、一文字の場合はパディングを追加"""
    term = term.strip()
    if len(term) == 1:
        term = f"_{term}_"
    return [term[i : i + 2] for i in range(len(term) - 1)] if term else []


def build_inverted_index(filename):
    """CSVファイルから転置インデックスを構築"""
    inverted_index = defaultdict(set)
    idx = 0
    with open(filename, "r", encoding="shift-jis", errors="ignore") as file:
        reader = csv.DictReader(file)
        for row in reader:
            idx += 1
            address_components = [
                row["都道府県"],
                row["市区町村"],
                row["町域"],
                row["京都通り名"],
                row["字丁目"],
                row["事業所名"],
                row["事業所住所"],
            ]

            for component in address_components:
                if component:
                    ngrams = create_2gram(component)
                    for ngram in ngrams:
                        inverted_index[ngram].add(idx)

    return inverted_index


def normalize_key(key):
    """キーを正規化する処理を行う。文字列を全角に変換し、全角空白を"_"に置き換える"""
    key_fullwidth = "".join(
        (
            unicodedata.normalize("NFKC", char)
            if unicodedata.east_asian_width(char) in "NaH"
            else char
        )
        for char in key
    )

    key_fullwidth = key_fullwidth.replace("\u3000", "_")

    return key_fullwidth


# 1. 転置インテックスの作成処理
csv_file_path = "./address/zenkoku.csv"
inverted_index = build_inverted_index(csv_file_path)
normalized_dict = {normalize_key(k): v for k, v in inverted_index.items()}
with open("inverted_index.pkl", "wb") as fw:
    pickle.dump(inverted_index, fw)

# 2. 検索処理
query = input("検索したい地名や住所の一部を入力してください: ")
normalized_query = normalize_key(query)
query_ngrams = create_2gram(normalized_query)
