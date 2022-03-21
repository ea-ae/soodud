import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class RimiScraper(scrapy.Spider):
    """RimiScraper class."""
    name = "rimi_product_scraper"
    rules = [Rule(LinkExtractor(allow=r'www.rimi.ee/epood/ee/tooted.*/c/SH-.*\?page='))]
    start_urls = [
        'https://www.rimi.ee/epood/ee/tooted/kulmutatud-toidukaubad/c/SH-4',
        'https://www.rimi.ee/epood/ee/tooted/leivad-saiad-kondiitritooted/c/SH-6',
        'https://www.rimi.ee/epood/ee/tooted/alkohol/c/SH-1',
        'https://www.rimi.ee/epood/ee/tooted/joogid/c/SH-3',
        'https://www.rimi.ee/epood/ee/tooted/puuviljad-koogiviljad-lilled/c/SH-12',
        'https://www.rimi.ee/epood/ee/tooted/piimatooted-munad-juust/c/SH-11',
        'https://www.rimi.ee/epood/ee/tooted/kauasailivad-toidukaubad/c/SH-13',
        'https://www.rimi.ee/epood/ee/tooted/vegantooted/c/SH-17',
        'https://www.rimi.ee/epood/ee/tooted/liha--ja-kalatooted/c/SH-8',
        'https://www.rimi.ee/epood/ee/tooted/talu-toidab/c/SH-19',
        'https://www.rimi.ee/epood/ee/tooted/lemmikloomakaubad/c/SH-7',
        'https://www.rimi.ee/epood/ee/tooted/kodu--ja-vabaajakaubad/c/SH-10',
        'https://www.rimi.ee/epood/ee/tooted/valmistoit/c/SH-16',
        'https://www.rimi.ee/epood/ee/tooted/lastekaubad/c/SH-5',
        'https://www.rimi.ee/epood/ee/tooted/maiustused-ja-snakid/c/SH-9',
        'https://www.rimi.ee/epood/ee/tooted/enesehooldustarbed/c/SH-2'
    ]

    # Wont be using these urls, because they dont contain normal products.
    # 'https://www.rimi.ee/epood/ee/tooted/teenused/c/SH-18',
    # 'https://www.rimi.ee/epood/ee/tooted/peolaud---telli-ette-/c/SH-20',

    def parse(self, response):
        """Scrape urls."""
        for products in response.css("div.card__details"):
            if f'{products.css("span::text").get()},{products.css("sup::text").get()}' == "None,None":
                continue
            elif not products.css("div.card__price-wrapper.-has-discount").get():
                yield {
                    "name": products.css("p.card__name::text").get(),
                    "price": f'{products.css("span::text").get()},{products.css("sup::text").get()}',
                    "discounted_price": None,
                }
            elif not products.css("div.old-price-tag.card__old-price").get():
                yield {
                    "name": products.css("p.card__name::text").get(),
                    "price": None,
                    "discounted_price": f'{products.css("span::text").get()},{products.css("sup::text").get()}',
                }
            else:
                yield {
                    "name": products.css("p.card__name::text").get(),
                    "price": products.css("div.old-price-tag.card__old-price span::text").get().replace('€', ''),
                    "discounted_price": f'{products.css("span::text").get()},{products.css("sup::text").get()}',
                }

        next_page = f'https://www.rimi.ee{response.css("li.pagination__item.-chevron a").attrib["href"]}'
        if next_page is not None:
            print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            print('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
            print(':(')
            print(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
