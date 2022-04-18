"""Rimi."""

import requests
import regex
from xml.etree import ElementTree as et
from bs4 import BeautifulSoup
import itertools as it
import soupsieve as sv
from typing import Callable, Iterable, Generator, Any

from data.stores import Discount, Product, StoreRegistry, product_hash


SITEMAPS = [
    'https://www.rimi.ee/epood/sitemaps/categories/siteMap_rimiEeSite_Category_et_1.xml',
    'https://www.rimi.ee/epood/sitemaps/categories/siteMap_rimiEeSite_Category_et_2.xml'
]

CACHED_URLS = [
    'https://www.rimi.ee/epood/ee/tooted/kulmutatud-toidukaubad/c/SH-4',
    'https://www.rimi.ee/epood/ee/tooted/leivad-saiad-kondiitritooted/c/SH-6',
    'https://www.rimi.ee/epood/ee/tooted/alkohol/c/SH-1',
    'https://www.rimi.ee/epood/ee/tooted/joogid/c/SH-3',
    'https://www.rimi.ee/epood/ee/tooted/puuviljad-koogiviljad-lilled/c/SH-12',
    'https://www.rimi.ee/epood/ee/tooted/piimatooted-munad-juust/c/SH-11',
    'https://www.rimi.ee/epood/ee/tooted/kauasailivad-toidukaubad/c/SH-13',
    'https://www.rimi.ee/epood/ee/tooted/vegantooted/c/SH-17',
    'https://www.rimi.ee/epood/ee/tooted/liha--ja-kalatooted/c/SH-8',
    # 'https://www.rimi.ee/epood/ee/tooted/teenused/c/SH-18',
    'https://www.rimi.ee/epood/ee/tooted/talu-toidab/c/SH-19',
    'https://www.rimi.ee/epood/ee/tooted/lemmikloomakaubad/c/SH-7',
    'https://www.rimi.ee/epood/ee/tooted/kodu--ja-vabaajakaubad/c/SH-10',
    'https://www.rimi.ee/epood/ee/tooted/valmistoit/c/SH-16',
    # 'https://www.rimi.ee/epood/ee/tooted/peolaud---telli-ette-/c/SH-20',
    'https://www.rimi.ee/epood/ee/tooted/lastekaubad/c/SH-5',
    'https://www.rimi.ee/epood/ee/tooted/maiustused-ja-snakid/c/SH-9',
    'https://www.rimi.ee/epood/ee/tooted/enesehooldustarbed/c/SH-2'
]

BASE_URL = 'https://www.rimi.ee/epood/ee/tooted'
BASE_PAGE_PARAMS: dict[str, str | int] = {
    'pageSize': 100,
}


@StoreRegistry('Rimi')
def main(saver: Generator[None, Product, None]):
    """Rimi entrypoint."""
    get_all(saver)


def get_all(saver: Generator[None, Product, None]):
    """Get all products."""
    for page in CACHED_URLS:
        first_soup = BeautifulSoup(get_page(page, 1), 'html5lib')
        last_page = sv.select('li.pagination__item:nth-last-child(2)', first_soup)
        pages = int(last_page[0].text) if last_page is not None else 1
        print('Rimi pages:', pages, page)

        soup_gen = (BeautifulSoup(get_page(page, page_num), 'html5lib') for page_num in range(2, pages + 1))
        for soup in it.chain([first_soup], soup_gen):
            for product in parse_page(soup):
                saver.send(product)


def parse_page(soup: BeautifulSoup) -> Iterable[Product]:
    """Parses a store page."""
    for listing in sv.select('.js-product-container.card', soup):  # li.product-grid__item
        if 'Ei ole saadaval' in listing.text:
            continue

        name = sv.select('.card__name', listing)[0].text
        discount = Discount.NONE
        link = sv.select('.card__url', listing)[0].attrs['href']
        # product_id = int(regex.search(r'/(\d+)$', link).group(1))
        product_id = int(link.split('/p/')[1])
        hash_value = product_hash('rimi', product_id)

        # main price
        price_eur = sv.select('.price-tag.card__price > span', listing)[0].text
        price_cents = sv.select('.price-tag.card__price > div > sup', listing)[0].text
        price = float(f'{price_eur}.{price_cents}')

        # old price in case of a regular sale
        old_price = sv.select('.old-price-tag.card__old-price > span', listing)
        if len(old_price) > 0:
            old_price = float(old_price[0].text[:-1].replace(',', '.'))
            discount = Discount.NORMAL

        # member sale
        member_price = sv.select('.card__image-wrapper .price-badge__price span', listing)
        if len(member_price) > 0:
            member_price = float(f'{member_price[0].text}.{member_price[1].text}')
            discount = Discount.MEMBER

        product = Product(name,
                          old_price if discount == Discount.NORMAL else price,
                          member_price if discount == Discount.MEMBER else price,
                          discount, hash_value, False)
        yield product

        # pattern = r'(?P<s1>\d+,?\d*)\s+(?P<s2>\d+)\s*€/tk\s*((?P<b>\d+,?\d*)€(?=[\s\S]*€))?'
        # groups = [match.groupdict() for match in regex.finditer(pattern, listing.text)][0]
        # price = float(f'{groups["s1"]}.{groups["s2"]}')
        # if groups['b'] is not None:  # there's a sale
        #     base_price = float(groups['b'].replace(',', '.'))
        #     print(name, '||', f'Base price: {base_price}\tSale: {price}')
        # else:
        #     print(name, '||', f'Base price: {price}')


def get_page(page_url: str, page: int) -> str:
    """Get a single page of products."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0'}
    query = BASE_PAGE_PARAMS | {'page': page}
    response = requests.get(page_url, headers=headers, params=query)

    return response.text


def parse_sitemaps():
    """Parse sitemaps and get the main category URLs."""
    for sitemap in SITEMAPS:
        doc = et.fromstring(get_sitemap(sitemap))
        for url in doc.iterfind('{http://www.sitemaps.org/schemas/sitemap/0.9}url'):
            loc = url.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
            if loc == 'https://www.rimi.ee/epood/ee':
                continue
            else:
                pattern = r'^https://www\.rimi\.ee/epood/ee/tooted/[^/]*/c/SH-\d+$'
                if (match := regex.fullmatch(pattern, loc)) is not None:
                    result = match.group(0)
                    print(result)


def get_sitemap(url: str) -> str:
    """Get a single page of products."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0'}
    response = requests.get(url, headers=headers)
    return response.text


if __name__ == '__main__':
    get_all()
