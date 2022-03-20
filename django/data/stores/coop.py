"""Coop."""

import requests
from typing import Any


TOTAL_PAGES = 3  # we should pull this number from the API automatically later
BASE_URL = 'http://api.ecoop.ee/supermarket/products'
BASE_PAGE_PARAMS: dict[str, str | int] = {
    'orderby': 'name',
    'order': 'asc',
    'language': 'et'
}


def get_all():
    """Get all products."""
    pages = [get_page(page) for page in range(1, TOTAL_PAGES + 1)]
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
