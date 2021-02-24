from urllib.parse import urljoin

import scrapy


def isNotEmptyString(str):
    return len(str) > 0


class GolosUaSpider(scrapy.Spider):
    name = "isport"
    custom_settings = {
        'ITEM_PIPELINES': {
            'lab1.pipelines.NewsXmlPipeline': 300,
        }
    }
    fields = {
        'img': '//img/@src',
        'text': '//*[not(self::script)]/text()',
        'link': '//a/@href'
    }
    start_urls = [
        'https://isport.ua/'
    ]
    allowed_domains = [
        'isport.ua'
    ]
    max_pages = 20

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.visited_pages = ['https://isport.ua/']

    def parse(self, response):
        links = response.xpath('//body//a/@href').extract()
        self.visited_pages.append('mailto:info@isport.ua')
        for l in links:
            if l not in self.visited_pages:
                print(l)
                self.visited_pages.append(l)
                url = urljoin(response.url, l)
                yield scrapy.Request(url, callback=self.parse_page)

    def parse_page(self, response):
        text = filter(isNotEmptyString,
                      map(lambda str: str.strip(),
                          [text.extract() for text in response.xpath(self.fields["text"])]))
        images = map(lambda url: ((response.url + url) if url.startswith('/') else url),
                     [img_url.extract() for img_url in response.xpath(self.fields["img"])])
        return {
            'text': text,
            'images': images,
            'url': response.url
        }
