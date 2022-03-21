"""Coop."""

import requests
import csv
from time import sleep
from typing import Callable, Any

from products import Discount


PAGE_LIMIT = 10_000  # don't accidentally DOS the site (for now) (implement ratelimiting later)
BASE_URL = 'http://api.ecoop.ee/supermarket/products'
BASE_PAGE_PARAMS: dict[str, str | int] = {
    'orderby': 'name',
    'order': 'asc',
    'language': 'et'
}


def main(save: Callable):
    """Coop entrypoint."""
    save(1)
    return False
    get_all()
    return True


def get_all():
    """Get all products."""
    return  # return early to prevent accidental execution for now
    result = get_page(1)  # noqa
    page_count, _ = result['metadata']['pages'], result['metadata']['count']
    print('Pages:', page_count)
    pages = (get_page(page) for page in range(1, min(page_count, PAGE_LIMIT) + 1))

    writer = csv.writer(open('coop.csv', 'w', newline='', encoding='utf-8'))
    writer.writerow(['Name', 'Base price', 'Discounted price', 'Discount'])

    for page in pages:
        for product in page['data']:
            name = product['name']
            discount = Discount.NONE
            base_price = product['price']
            if (price := product['price_sale_mbr']) is not None:
                discount = Discount.MEMBER
            elif (price := product['price_sale']) is not None:
                discount = Discount.NORMAL
            else:
                price = base_price

            # print(name, base_price, price, discount)
            writer.writerow([name, base_price, price, str(discount)])


def get_page(page: int) -> dict[str, Any]:
    """Get a single page of products."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0'}
    query = BASE_PAGE_PARAMS | {'page': page}
    response = requests.get(BASE_URL, headers=headers, params=query)

    # slow down!
    print(f'\rPage {page:03}', end='', flush=True)
    if page % 5 == 0:
        sleep(2)

    return response.json()


if __name__ == '__main__':
    get_all()
