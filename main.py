import csv
import os
import requests
from concurrent import futures

# Colors
GREEN = '\33[32m'
YELLOW = '\33[33m'

CATEGORY = 'all' # all
OUTPUT_DIR = 'Books'  # Output directory
TYPE = 'pdf'  # pdf / epub

CONTENT = 'content' if TYPE == 'pdf' else 'download'
BOOK_URL = f'https://link.springer.com/{CONTENT}/{TYPE}/'


def download(book):
    if len(book[5]) and len(book[5]) > 8:
        print(YELLOW + f'[!] Fetching: {book[0]} ...')
        url = f'{BOOK_URL}{book[5]}.{TYPE}'
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(f'{OUTPUT_DIR}/{book[6]} - {book[0]}.{TYPE}', 'wb') as f:
                f.write(response.raw.read())


def main():
    books = []
    with open(f'categories/{CATEGORY}.csv', 'r', encoding='utf8') as csv_file:
        csv_result = csv.reader(csv_file, delimiter=',')
        books = list(csv_result)
        print(f'{YELLOW}[!] Total books: { len(books) - 1 }')
    if not os.path.exists(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)
    ex = futures.ThreadPoolExecutor(max_workers=20)
    ex.map(download, books)


if __name__ == "__main__":
    main()
