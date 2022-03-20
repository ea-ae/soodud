import scrapy


class RimiScraper(scrapy.Spider):
    name = "rimi_product_scraper"
    start_urls = ["https://www.rimi.ee/epood/ee/tooted/piimatooted-munad-juust/c/SH-11"]

    def parse(self, response):
        for products in response.css("div.js-product-container card-horizontal-for-mobile"):
            yield {
                "info": products.css("div.data-gtm-eec-product").get(),
            }
