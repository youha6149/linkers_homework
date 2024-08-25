import unicodedata


def create_2gram(term):
    """文字列を2-gramに分割し、一文字の場合はパディングを追加"""
    term = term.strip()
    if len(term) == 1:
        term = f"_{term}_"
    return [term[i : i + 2] for i in range(len(term) - 1)] if term else []


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


def display_results(reader, matching_lines):
    """検索結果を表示"""
    for idx, row in enumerate(reader, 1):
        if idx in matching_lines:
            print(
                f'{row["郵便番号"]} {row["都道府県"]} {row["市区町村"]} {row["町域"]} '
                f'{row["京都通り名"]} {row["字丁目"]} {row["事業所名"]} {row["事業所住所"]}'
            )
