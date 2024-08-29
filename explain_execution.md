## 実行手順

## Github リポジトリ

- <https://github.com/youha6149/linkers_homework>

- githubからデータを取得する場合、releaseから`main_mac`をダウンロードし、[項目3](#3-実行ファイルを実行)以降を参考に実行してください

### 1. zipファイルの解凍

zipファイルは以下のような構成になっています。

```
dist
┗ main_mac
picture
┗ ドキュメントで利用する画像
linkers_homework-1.0.0
  ┗ ソースコード
explain_execution.md
explain_technology.md
explain_execution.pdf
explain_technology.pdf
```

### 2. 環境別の実行ファイルを任意のディレクトリにコピー

    dist/main_mac

### 3. 実行ファイルを実行

※ 初回実行時はcsvのダウンロードと検索用ファイルの作成のため引数なしで実行してください

    ```
    chmod +x ./main_mac
    # 対象ファイルの隔離属性を削除し永続的に実行できるようにするコマンド
    xattr -d com.apple.quarantine ./main_mac
    ./main_mac
    ```

実行には10秒程度かかります。
実行すると以下のように表示されるので検索値を入力する(例: 渋谷と入力)
![入力画面](./picture/入力画面.png)

出力結果例:
![検索結果](./picture/検索結果.png)

### 4. ２回目以降で全国.jpのcsvの更新が必要ない場合

以下の引数を入力することで、検索処理のみが行われます。

`--search-only`

    ```
    # 前述の`xattr -d com.apple.quarantine ./main_mac`を実行していれば問題なく稼働する
    ./main_mac --search-only
    ```
