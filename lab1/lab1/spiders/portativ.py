import scrapy
from scrapy import Selector


class PetMarketSpider(scrapy.Spider):
    name = "portativ"
    fields = {
        'price': '//span[@class="price-value UAH"]/text()',
        'name': '//div[@class="cataloggrid-item-name-block"]/a/text()',
        'product': '//div[@class="cataloglist-item-container"]',
        'img': '//a[@class="product-image"]/img/@src',
        'product_link': '//a[@class="product-image"]/@href'
    }
    start_urls = [
        'https://portativ.ua/category_841832.html?tip_podkljuchenija_fe9f=173597'
    ]
    allowed_domains = [
        'portativ.ua'
    ]
    number_of_items = 20


    def parse(self, response):
        for product in response.xpath(self.fields["product"]).getall()[:self.number_of_items]:
            selector = Selector(text=product)
            yield {
                'link': selector.xpath(self.fields['product_link']).extract(),
                'price': selector.xpath(self.fields['price']).get().strip(),
                'img': selector.xpath(self.fields['img']).extract(),
                'name': ''.join(selector.xpath(self.fields['name']).extract())
            }
