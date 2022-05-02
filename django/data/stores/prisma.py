"""Prisma."""

import requests
import urllib3
from xml.etree import ElementTree as et
from bs4 import BeautifulSoup
import soupsieve as sv
import itertools as it
import os
import math
from typing import Generator, Iterable

from data.stores import Discount, Product, StoreRegistry, product_hash


SITEMAP = 'http://www.prismamarket.ee/products/sitemap.xml'
PRODUCTS_PER_PAGE = 48


@StoreRegistry('Prisma')
def main(saver: Generator[None, Product, None]):
    """Prisma entrypoint."""
    get_all(saver)


def get_all(saver: Generator[None, Product, None]):
    """Get all products."""
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # categories = [page.rstrip() for page in open(path, 'r').readlines()]
    # categories = parse_sitemaps()
    categories = get_category_urls()
    for category in categories:
        first_soup = BeautifulSoup(get_page(category, 1), 'html5lib')
        product_count = sv.select('.products-shelf .category-items > b', first_soup)

        if len(product_count) == 0:  # removes empty category pages
            continue

        page_count = math.ceil(int(product_count[0].text) / PRODUCTS_PER_PAGE)
        soup_gen = (BeautifulSoup(get_page(category, page_num), 'html5lib') for page_num in range(2, page_count + 1))
        for soup in it.chain([first_soup], soup_gen):
            for product in parse_page(soup):
                saver.send(product)


def parse_page(soup: BeautifulSoup) -> Iterable[Product]:
    """Parse a page of products."""
    for listing in sv.select('.shelf li', soup):
        ean = int(listing.attrs['data-ean'])
        discount = Discount.NONE

        name = sv.select('.info > .name', listing)[0].text
        if name.endswith('...'):  # name truncated, use URL instead
            url_name = sv.select('a.js-link-item', listing)[0].attrs['href']
            name = url_name.split('/')[-2].replace('--', ', ').replace('-', ' ').capitalize()

        producer = sv.select('.info > .subname', listing)
        if len(producer) > 0:
            if ',' in producer[0].text:
                name += ' ' + producer[0].text[::-1].split(',', 1)[1][::-1]
                if producer[0].text.count(',') > 1:
                    print(producer[0].text, 'overone')
                    print(producer[0].text[::-1].split(',', 1)[1][::-1])
            else:
                name += ' ' + producer[0].text

        price_eur = int(sv.select('.js-info-price .whole-number', listing)[0].text)
        price_cents = int(sv.select('.js-info-price .decimal', listing)[0].text)
        price = (100 * price_eur + price_cents) / 100

        if len(el := sv.select('.info .price .discount-price', listing)) > 0:
            discount = Discount.NORMAL
            old_price = float(el[0].text.split()[0].replace(',', '.'))
        else:
            old_price = price

        product = Product(name, old_price, price, discount, str(ean), True)
        yield product


def get_page(page_url: str, page: int) -> str:
    """Get a single page of products."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0'}
    page_url = f'{page_url.replace("https", "http")}/page/{page}?sort_order=alpha&sort_dir=asc'
    print(page_url)
    while True:
        attempts = 0
        try:
            response = requests.get(page_url, headers=headers, verify=False)
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError) as e:
            if attempts >= 3:
                raise e
            attempts += 1
            print(f'\nConnect timeout. Retrying ({attempts}/3)...')
        else:
            break
    return response.text


def get_category_urls() -> list[str]:
    """Get category URLs by parsing the category list."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0'}
    site = requests.get('https://www.prismamarket.ee/products/selection', headers=headers, verify=False).text
    soup = BeautifulSoup(site, 'html5lib')
    categories = []
    for category in sv.select('.category-shelf-item .categories-list .js-category-item', soup):
        if category.text != 'Kuva rohkem...':
            categories.append('https://prismamarket.ee' + category.attrs['href'])
    return categories


def parse_sitemaps() -> list[str]:
    """Parse sitemaps and get the main category URLs."""
    pages = []
    doc = et.fromstring(get_sitemap(SITEMAP))
    for sitemap in doc.iterfind('{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap'):
        loc = sitemap.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
        # print(loc.split('/sitemap_items')[0])
        pages.append(loc.split('/sitemap_items')[0])
    return pages


def get_sitemap(url: str) -> str:
    """Parse sitemaps and get the main category URLs."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0'}
    response = requests.get(url, headers=headers, verify=False)
    return response.text


if __name__ == '__main__':
    parse_sitemaps()
