import io
import os
import zipfile

import requests


class CsvDownloader:
    def __init__(self, url: str = "http://jusyo.jp/downloads/new/csv/csv_zenkoku.zip"):
        self.url = url
        self.zip_content = None

    def download(self):
        """全国csvのzipファイルをダウンロードする"""
        try:
            with requests.get(self.url) as response:
                response.raise_for_status()
                self.zip_content = response.content

        except requests.exceptions.HTTPError as http_err:
            raise requests.exceptions.HTTPError(f"HTTPエラーが発生しました: {http_err}")

        except requests.exceptions.RequestException as req_err:
            raise requests.exceptions.RequestException(
                f"リクエスト例外が発生しました: {req_err}"
            )

        except Exception as err:
            raise Exception(
                f"全国csvをDL処理実行中に予期せぬエラーが発生しました: {err}"
            )

    def extract(self, csv_save_to: str = "./address"):
        """全国csvのzipファイルを解凍する"""
        try:
            if self.zip_content is None:
                raise ValueError("ダウンロードが実行されていません。")

            with zipfile.ZipFile(io.BytesIO(self.zip_content)) as zip_file:
                os.makedirs(csv_save_to, exist_ok=True)

                for file_name in zip_file.namelist():
                    if file_name.endswith(".csv"):
                        with zip_file.open(file_name) as source:
                            file_path = os.path.join(
                                csv_save_to, os.path.basename(file_name)
                            )
                            with open(file_path, "wb") as target:
                                target.write(source.read())

        except zipfile.BadZipFile as zip_err:
            raise zipfile.BadZipFile(f"ZIPファイルが壊れています: {zip_err}")

        except zipfile.LargeZipFile as zip_err:
            raise zipfile.LargeZipFile(f"ZIPファイルが大きすぎます: {zip_err}")

        except FileNotFoundError as file_err:
            raise FileNotFoundError(f"指定されたファイルが見つかりません: {file_err}")

        except ValueError as val_err:
            raise ValueError(f"{val_err}")

        except Exception as err:
            raise Exception(
                f"全国csvを解凍処理実行中に予期せぬエラーが発生しました: {err}"
            )
