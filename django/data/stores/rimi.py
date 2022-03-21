"""Rimi."""

import requests
import regex
from xml.etree import ElementTree as et


SITEMAPS = [
    'https://www.rimi.ee/epood/sitemaps/categories/siteMap_rimiEeSite_Category_et_1.xml',
    'https://www.rimi.ee/epood/sitemaps/categories/siteMap_rimiEeSite_Category_et_2.xml'
]

CACHED_PAGES = [
    'https://www.rimi.ee/epood/ee/tooted/kulmutatud-toidukaubad/c/SH-4',
    'https://www.rimi.ee/epood/ee/tooted/leivad-saiad-kondiitritooted/c/SH-6',
    'https://www.rimi.ee/epood/ee/tooted/alkohol/c/SH-1',
    'https://www.rimi.ee/epood/ee/tooted/joogid/c/SH-3',
    'https://www.rimi.ee/epood/ee/tooted/puuviljad-koogiviljad-lilled/c/SH-12',
    'https://www.rimi.ee/epood/ee/tooted/piimatooted-munad-juust/c/SH-11',
    'https://www.rimi.ee/epood/ee/tooted/kauasailivad-toidukaubad/c/SH-13',
    'https://www.rimi.ee/epood/ee/tooted/vegantooted/c/SH-17',
    'https://www.rimi.ee/epood/ee/tooted/liha--ja-kalatooted/c/SH-8',
    'https://www.rimi.ee/epood/ee/tooted/teenused/c/SH-18',
    'https://www.rimi.ee/epood/ee/tooted/talu-toidab/c/SH-19',
    'https://www.rimi.ee/epood/ee/tooted/lemmikloomakaubad/c/SH-7',
    'https://www.rimi.ee/epood/ee/tooted/kodu--ja-vabaajakaubad/c/SH-10',
    'https://www.rimi.ee/epood/ee/tooted/valmistoit/c/SH-16',
    'https://www.rimi.ee/epood/ee/tooted/peolaud---telli-ette-/c/SH-20',
    'https://www.rimi.ee/epood/ee/tooted/lastekaubad/c/SH-5',
    'https://www.rimi.ee/epood/ee/tooted/maiustused-ja-snakid/c/SH-9',
    'https://www.rimi.ee/epood/ee/tooted/enesehooldustarbed/c/SH-2'
]


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
