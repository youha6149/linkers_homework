import csv
from collections import defaultdict


def create_2gram(term):
    """文字列を2-gramに分割し、一文字の場合はパディングを追加"""
    term = term.strip()
    if len(term) == 1:
        term = f"_{term}_"
    return [term[i : i + 2] for i in range(len(term) - 1)]


def build_inverted_index(filename):
    # TODO: 遅すぎるので高速化
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
                ngrams = create_2gram(component)
                for ngram in ngrams:
                    inverted_index[ngram].add(idx)

    return inverted_index


csv_file_path = "./address/zenkoku.csv"
inverted_index = build_inverted_index(csv_file_path)
print(inverted_index["北海"])
