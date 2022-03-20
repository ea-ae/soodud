import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class RimiScraper(scrapy.Spider):
    name = "rimi_product_scraper"
    rules = [Rule(LinkExtractor(allow=r'epood/ee/tooted.*/c/SH-.*\?page='), allow_domains='rimi.ee')]
    start_urls = ["https://www.rimi.ee/epood/ee/tooted/piimatooted-munad-juust/c/SH-11"]

    def parse(self, response):
        for products in response.css("div.card__details"):
            yield {
                "name": products.css("p.card_name::text").get(),
                "price": products.css("div.price-tag::text").get(),
            }
