"""Prisma."""

import requests
import regex
from xml.etree import ElementTree as et


SITEMAP = 'http://www.prismamarket.ee/products/sitemap.xml'


def get_all():
    """Get all products."""
    cached_pages = [page.rstrip() for page in open('prisma_sites.txt', 'r').readlines()]
    print(cached_pages)


def parse_sitemaps():
    """Parse sitemaps and get the main category URLs."""
    doc = et.fromstring(get_sitemap(SITEMAP))
    for sitemap in doc.iterfind('{http://www.sitemaps.org/schemas/sitemap/0.9}sitemap'):
        loc = sitemap.find('{http://www.sitemaps.org/schemas/sitemap/0.9}loc').text
        print(loc.split('/sitemap_items')[0])


def get_sitemap(url: str) -> str:
    """Parse sitemaps and get the main category URLs."""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:77.0) Gecko/20190101 Firefox/77.0'}
    response = requests.get(url, headers=headers, verify=False)
    return response.text


if __name__ == '__main__':
    parse_sitemaps()
