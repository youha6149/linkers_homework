import sys

from indexing.entry import create_inverted_index, search_inverted_index


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--create-index":
            create_inverted_index()

        else:
            print(f"Error: 不明な引数が指定されました: {sys.argv[1]}")
            print("使用方法: main.py [--create-index]")
            sys.exit(1)
    else:
        search_inverted_index()


if __name__ == "__main__":
    main()
