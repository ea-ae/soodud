"""Rimi."""

import requests
import regex
from xml.etree import ElementTree as et
from typing import Callable, Generator, Any
import bs4
import soupsieve as sv


from data.stores.products import Discount, Product

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


def main(save: Callable):
    """Rimi entrypoint."""
    saver = save(3)
    next(saver)
    get_all(saver)
    return True


def get_all():  # saver: Generator[None, Product, None]):
    """Get all products."""
    for page in CACHED_URLS:
        soup = bs4.BeautifulSoup(get_page(page, 1), 'html5lib')
        names = sv.select('p:is(.card__name)', soup)
        base_prices = sv.select('div.price-tag > span, div.price-tag > div > sup', soup)
        # TODO add price and discount and fix up the base_price(Putting bills and cents on separate lines)

        print(names, base_prices)
        # product = Product(name, float(base_price))  # , float(price), discount)
        # saver.send(product)


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
