"""Coop."""

import requests
import csv
from typing import Callable, Any

from products import Discount


RESULTS_PER_PAGE = 1000  # too large and python crashes
BASE_URL = 'https://www.selver.ee/api/catalog/vue_storefront_catalog_et/product/_search'
PARAMS: dict[str, str | int] = {
    # 'from': 11000,  # start from result n
    # 'size': 1000,  # results per page (96 max default)
    'sort': 'name.sortable'
}


def main(save: Callable):
    """Selver entrypoint."""
    save(2)
    return True
    get_all()
    return True


def get_all():
    """Get all products."""
    return  # return early to prevent accidental execution for now
    writer = csv.writer(open('selver.csv', 'w', newline='', encoding='utf-8'))  # noqa

    for n in range(1, 100):
        page = get_page(n)['hits']['hits']
        product_count = len(page)
        print('Products:', product_count)

        if n == 1:  # first page
            writer.writerow(['Name', 'Base price', 'Discounted price', 'Discount'])

        for product in page:
            product = product['_source']

            name = product['name']
            prices = product['prices']
            discount = Discount.NORMAL if prices[0]['is_discount'] else Discount.NONE
            if discount == Discount.NORMAL:
                base_price = prices[0]['original_price']
                price = prices[0]['price']
            else:
                discount = Discount.MEMBER if prices[1]['is_discount'] else Discount.NONE
                base_price = prices[1]['original_price']
                price = prices[1]['price']

            writer.writerow([name, base_price, price, str(discount)])

        if product_count < RESULTS_PER_PAGE:
            break  # last page


def get_page(page: int) -> dict[str, Any]:
    """Get a single page of products."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0'}
    query = PARAMS | {'size': RESULTS_PER_PAGE, 'from': RESULTS_PER_PAGE * (page - 1)}
    response = requests.get(BASE_URL, headers=headers, params=query)
    return response.json()


if __name__ == '__main__':
    get_all()
