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


def build_inverted_index(reader):
    """CSVリーダーから転置インデックスを構築"""
    inverted_index = defaultdict(set)

    for idx, row in enumerate(reader, start=1):
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
    return key_fullwidth.replace("\u3000", "_")


def save_inverted_index(filename, inverted_index):
    """転置インデックスをpickleファイルに保存"""
    with open(filename, "wb") as fw:
        pickle.dump(inverted_index, fw)


def load_inverted_index(filename):
    """pickleファイルから転置インデックスを読み込む"""
    with open(filename, "rb") as fr:
        return pickle.load(fr)


def search_inverted_index(inverted_index, query):
    """転置インデックスでクエリを検索"""
    normalized_query = normalize_key(query)
    query_ngrams = create_2gram(normalized_query)

    result_sets = [inverted_index.get(ngram, set()) for ngram in query_ngrams]

    if result_sets:
        return set.intersection(*result_sets)
    return set()


def display_results(csv_file_path, matching_lines):
    """検索結果を表示"""
    with open(csv_file_path, "r", encoding="shift-jis", errors="ignore") as file:
        reader = csv.DictReader(file)
        for idx, row in enumerate(reader, 1):
            if idx in matching_lines:
                print(
                    f'{row["郵便番号"]} {row["都道府県"]} {row["市区町村"]} {row["町域"]} '
                    f'{row["京都通り名"]} {row["字丁目"]} {row["事業所名"]} {row["事業所住所"]}'
                )


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
