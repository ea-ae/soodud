"""Coop."""

import requests
from typing import Generator, Callable, Any

from data.stores import Discount, Product, StoreRegistry, product_hash


RESULTS_PER_PAGE = 1000  # too large and python crashes
BASE_URL = 'https://www.selver.ee/api/catalog/vue_storefront_catalog_et/product/_search'
PARAMS: dict[str, str | int] = {
    # 'from': 11000,  # start from result n
    # 'size': 1000,  # results per page (96 max default)
    'sort': 'name.sortable'
}


@StoreRegistry('Selver')
def main(saver: Generator[None, Product, None]):
    """Selver entrypoint."""
    get_all(saver)


def get_all(saver: Generator[None, Product, None]):
    """Get all products."""
    for n in range(1, 100):
        page = get_page(n)['hits']['hits']
        product_count = len(page)
        print(f'Selver page: {n} ({product_count})')

        for product in page:
            product = product['_source']

            name = product['name']
            prices = product['prices']
            hash_value, has_barcode = int(str(product['product_main_ean'])[:-15:-1]), True
            discount = Discount.NORMAL if prices[0]['is_discount'] else Discount.NONE
            if discount == Discount.NORMAL:
                base_price = prices[0]['original_price']
                price = prices[0]['price']
            else:
                discount = Discount.MEMBER if prices[1]['is_discount'] else Discount.NONE
                base_price = prices[1]['original_price']
                price = prices[1]['price']

            if base_price is None or price is None:
                old_hash_value = int(str(hash(f'selver{prices[0]["id"]}'))[:-15:-1])
                hash_value, has_barcode = product_hash('selver', prices[0]['id']), False
                assert old_hash_value == hash_value

            if hash_value is None:
                hash_value = 0

            product = Product(name, float(base_price), float(price), discount, hash_value, has_barcode)
            saver.send(product)

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
