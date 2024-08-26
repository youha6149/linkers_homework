import unicodedata

import jaconv


class Tokenizer:
    def __init__(self):
        pass

    def create_2gram(self, term):
        """文字列を2-gramに分割し、一文字の場合はパディングを追加"""
        term = term.strip()
        if len(term) == 1:
            term = f"_{term}_"
        return [term[i : i + 2] for i in range(len(term) - 1)] if term else []

    def normalize_key(self, key: str):
        """キーを正規化する処理を行う。文字列を全角に変換し、全角空白を"_"に置き換え、小文字を大文字に変換する"""
        key_fullwidth = jaconv.h2z(key, ascii=True, digit=True)
        key_fullwidth = key_fullwidth.replace(" ", "_").upper()
        return key_fullwidth
