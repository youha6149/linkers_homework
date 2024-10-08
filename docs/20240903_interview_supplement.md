# 回答が不十分だった内容の説明

## 質問

ご質問内容として、「なぜ`build`において単一項目値（例：曙、甲、境など）は、結合文字列のトークン化処理の部分とは分けて、"_"を付ける処理を行ったのか？」を頂きました。(※)

## 結論

面談途中で頂いた補足の通り、単一項目値をタームリストに含め、単一の入力文字列でも検索できるようにしたかったため。(※)

※ こちらの解釈がご説明の内容と異なる場合はお知らせいただけると幸いです。

## 背景

### 問題

単一項目値のみが入力された場合、検索結果が0件になることがありました。

### 原因1

検索項目値を結合した文字列からトークンを生成すると、「単一の地名である」という情報が失われる。

#### 例

| 項目         | 内容                              |
|--------------|-----------------------------------|
| 都道府県      | 北海道                            |
| 市区町村      | 名寄市                            |
| 町域         | 曙                                |
| 検索項目値    | 北海道 名寄市 曙                   |
| 結合文字列    | 北海道名寄市曙                     |
| トークン      | ["北海", "海道", "道名", "名寄", "寄市", "市曙"] |

---

### 原因2

単一項目値のみが入力された場合、以下のようにトークンが生成される。

#### 例

| 項目         | 内容              |
|--------------|-------------------|
| 入力文字列   | 曙                |
| トークン     | `["_曙", "曙_"]`  |

---

### まとめ

原因1で生成されたトークンに加え、`["_曙", "曙_"]`のような"_"を付けた単一項目値をタームリストに保存することで、
原因2のように単一項目値のみが入力された場合でも正しく検索できるようにしました。

また、`build`において単一項目値に対して`create_2gram`関数を用いるだけでこの問題を解決できたため、効率も良好でした。

---

### 代替案の検討

以下の方法でも解決可能と考えましたが、「入力文字列から2-gramで作成されるすべてのトークン」という課題の要件を踏まえ、上記の方法を採用しました。

1. タームリストに ["曙"] のような単一項目値を保存する
2. 単一項目値が入力された場合、トークン化を行わない

長文になり恐縮ですが、ご確認頂けますと大変うれしく思います。
