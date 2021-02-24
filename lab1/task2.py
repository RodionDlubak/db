from scrapy import cmdline
import os
import lxml.etree as ET


def crawl():
    try:
        os.remove("results/portativ.xml")
    except OSError:
        print("results/portativ.xml not found")
    cmdline.execute("scrapy crawl portativ -o results/portativ.xml -t xml".split())


# crawl()

def xslt_parse():
    print("FDSFDFDF")
    dom = ET.parse('results/portativ.xml')
    xslt = ET.parse('portativ.xslt')
    transform = ET.XSLT(xslt)
    newdom = transform(dom)
    with open('results/portativ.html', 'wb') as f:
        f.write(ET.tostring(newdom, pretty_print=True))


xslt_parse()
