"""Coop."""

import requests
from time import sleep
from typing import Generator, Callable, Any

from data.stores import Discount, Product, StoreRegistry


PAGE_LIMIT = 100_000  # don't accidentally DOS the site
BASE_URL = 'http://api.ecoop.ee/supermarket/products'
BASE_PAGE_PARAMS: dict[str, str | int] = {
    'orderby': 'name',
    'order': 'asc',
    'language': 'et'
}


@StoreRegistry('Coop')
def main(save: Callable) -> bool:
    """Coop entrypoint."""
    saver = save(1)
    next(saver)
    get_all(saver)
    return True


def get_all(saver: Generator[None, Product, None]):
    """Get all products."""
    result = get_page(1)
    page_count, _ = result['metadata']['pages'], result['metadata']['count']
    print('Coop pages:', page_count)
    pages = (get_page(page) for page in range(1, min(page_count, PAGE_LIMIT) + 1))

    for i, page in enumerate(pages):
        if (i + 1) % 50 == 0:
            print(f'Coop: page {i + 1}')

        for product in page['data']:
            name = product['name']
            hash_value = int(str(product['id2'])[:-15:-1])
            discount = Discount.NONE
            base_price = product['price']
            if (price := product['price_sale_mbr']) is not None:
                discount = Discount.MEMBER
            elif (price := product['price_sale']) is not None:
                discount = Discount.NORMAL
            else:
                price = base_price

            # print(name, base_price, price, type(base_price), type(price))
            if base_price is None or price is None:
                continue  # skip non-purchasable items

            if hash_value is None:
                hash_value = int(str(hash(f'coop{product[0]["id"]}'))[:-15:-1])

            product = Product(name, float(base_price), float(price), discount, hash_value, False)
            saver.send(product)


def get_page(page: int) -> dict[str, Any]:
    """Get a single page of products."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0'}
    query = BASE_PAGE_PARAMS | {'page': page}
    response = requests.get(BASE_URL, headers=headers, params=query)

    # slow down!
    # print(f'\rPage {page:03}', end='', flush=True)
    if page % 5 == 0:
        sleep(2)

    return response.json()


if __name__ == '__main__':
    get_all()
