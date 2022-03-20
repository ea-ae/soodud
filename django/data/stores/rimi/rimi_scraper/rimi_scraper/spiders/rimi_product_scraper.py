import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class RimiScraper(scrapy.Spider):
    name = "rimi_product_scraper"
    rules = [Rule(LinkExtractor(allow=r'www.rimi.ee/epood/ee/tooted.*/c/SH-.*\?page='))]
    start_urls = ["https://www.rimi.ee/epood/ee/tooted/piimatooted-munad-juust/c/SH-11?"
                  "page=1&pageSize=80&query=%3Aprice-asc%3AallCategories%3ASH-11%3AassortmentStatus%3AinAssortment"]

    def parse(self, response):
        for products in response.css("div.card__details"):
            if f'{products.css("span::text").get()},{products.css("sup::text").get()}' == "None,None":
                continue
            elif not products.css("div.card__price-wrapper.-has-discount").get():
                yield {
                    "name": products.css("p.card__name::text").get(),
                    "price": f'{products.css("span::text").get()},{products.css("sup::text").get()}',
                    "discounted_price": None,
                }
            else:
                yield {
                    "name": products.css("p.card__name::text").get(),
                    "price": products.css("div.old-price-tag.card__old-price span::text").get().replace('€', ''),
                    "discounted_price": f'{products.css("span::text").get()},{products.css("sup::text").get()}',
                }
