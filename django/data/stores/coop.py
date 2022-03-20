"""Coop."""

import requests
from typing import Callable, Any

from products import Discount


PAGE_LIMIT = 5  # don't accidentally DOS the site (for now) (implement ratelimiting later)
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
    result = get_page(1)
    page_count, _ = result['metadata']['pages'], result['metadata']['count']
    pages = [get_page(page) for page in range(1, min(page_count, PAGE_LIMIT) + 1)]

    for page in pages:
        for product in page['data']:
            print(
                f'"{product["name"]}"',
                product['price'],
                sale if (sale := product['price_sale_mbr']) is not None else product['price']
            )


def get_page(page: int) -> dict[str, Any]:
    """Get a single page of products."""
    query = BASE_PAGE_PARAMS | {'page': page}
    response = requests.get(BASE_URL, params=query)
    return response.json()


if __name__ == '__main__':
    get_all()
