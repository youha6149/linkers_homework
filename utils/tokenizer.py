import unicodedata


class Tokenizer:
    def __init__(self):
        pass

    def create_2gram(self, term):
        """文字列を2-gramに分割し、一文字の場合はパディングを追加"""
        term = term.strip()
        if len(term) == 1:
            term = f"_{term}_"
        return [term[i : i + 2] for i in range(len(term) - 1)] if term else []

    def normalize_key(self, key):
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
