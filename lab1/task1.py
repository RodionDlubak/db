import os

from scrapy import cmdline
from lxml import etree

cmdline.execute("scrapy crawl isport".split())
root = None
with open('results/isport.xml', 'r') as file:
    root = etree.parse(file)

pagesCount = root.xpath('count(//page)')
textFragmentsCount = root.xpath('count(//fragment[@type="link"])')
os.system('Average count of text fragments per page %f' % (textFragmentsCount / pagesCount))
