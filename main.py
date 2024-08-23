import csv
from collections import defaultdict

# CSVファイルのパス
csv_file_path = "./address/zenkoku.csv"


# データを読み込み、転置インデックスを作成する関数
def create_inverted_index(csv_file):
    inverted_index = defaultdict(list)

    # CSVファイルの読み込み
    with open(
        csv_file, newline="", encoding="shift_jis", errors="ignore"
    ) as f:  # デコードエラーを無視
        reader = csv.DictReader(f)
        for row in reader:
            address_components = [
                row["都道府県"],
                row["市区町村"],
                row["町域"],
                row["京都通り名"],
                row["字丁目"],
                row["事業所名"],
                row["事業所住所"],
            ]
            full_address = " ".join(
                filter(None, address_components)
            )  # Noneを除去して結合
            n_grams = get_ngrams(full_address, 2)
            for ngram in n_grams:
                inverted_index[ngram].append(row)

    return inverted_index


# 2-gramを作成する関数
def get_ngrams(text, n):
    ngrams = [text[i : i + n] for i in range(len(text) - n + 1)]
    return ngrams


# 検索クエリに基づいて結果を返す関数
def search_address(query, inverted_index):
    query_ngrams = get_ngrams(query, 2)
    results = []

    for ngram in query_ngrams:
        if ngram in inverted_index:
            results.extend(inverted_index[ngram])

    # 各住所がすべてのクエリ2-gramを含むかチェック
    filtered_results = [
        row
        for row in results
        if all(
            ngram
            in " ".join(
                filter(
                    None,
                    [
                        row["都道府県"],
                        row["市区町村"],
                        row["町域"],
                        row["京都通り名"],
                        row["字丁目"],
                        row["事業所名"],
                        row["事業所住所"],
                    ],
                )
            )
            for ngram in query_ngrams
        )
    ]

    return filtered_results


# 結果を表示する関数
def display_results(results):
    for row in results:
        print(
            f'{row["郵便番号"]} {row["都道府県"]} {row["市区町村"]} {row["町域"]} {row["京都通り名"]} {row["字丁目"]} {row["事業所名"]} {row["事業所住所"]}'
        )


# CSVファイルから転置インデックスを作成
inverted_index = create_inverted_index(csv_file_path)

# 検索クエリを指定
query = input("単語を入力してください: ")

# 検索結果を取得
results = search_address(query, inverted_index)

# 結果を表示
display_results(results)
