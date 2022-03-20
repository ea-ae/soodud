"""Coop."""

import requests
from typing import Callable, Any

from data.stores.main import Discount


PAGE_LIMIT = 5  # don't accidentally DOS the site (for now) (implement ratelimiting later)
BASE_URL = 'https://www.selver.ee/api/catalog/vue_storefront_catalog_et/product/_search'
PARAMS: dict[str, str | int] = {
    'from': 0,  # start from result n
    'size': 96,  # results per page (96 max default)
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
    pages = [get_page(1)]

    for page in pages:
        page = page['hits']['hits']

        for product in page:
            product = product['_source']

            prices = product['prices']
            discount = Discount.NORMAL if prices[0]['is_discount'] else Discount.NONE
            if discount == Discount.NORMAL:
                base_price = prices[0]['original_price']
                price = prices[0]['price']
            else:
                discount = Discount.MEMBER if prices[1]['is_discount'] else Discount.NONE
                base_price = prices[1]['original_price']
                price = prices[1]['price']

            print(
                f'"{product["name"]}"',
                base_price,
                price,
                discount
            )


def get_page(page: int) -> dict[str, Any]:
    """Get a single page of products."""
    query = PARAMS
    response = requests.get(BASE_URL, params=query)
    return response.json()


if __name__ == '__main__':
    get_all()
