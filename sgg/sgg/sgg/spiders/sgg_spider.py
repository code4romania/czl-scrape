# -*- coding: utf-8 -*-
import scrapy
 
from scrapy.crawler import CrawlerProcess
import logging
import json 
import hashlib 

base_url = "http://www.sgg.ro"



class Item(scrapy.Item):
    identifier = scrapy.Field()
    title = scrapy.Field()
    type = scrapy.Field()
    institution = scrapy.Field()
    date = scrapy.Field()
    description = scrapy.Field()
    feedback_days = scrapy.Field()
    contact = scrapy.Field()
    documents = scrapy.Field() 
    
def xtract(obj, sel):
    ret = obj.xpath(sel).extract_first()

    if ret: 
        ret = " ".join(map(lambda s : s.strip(), ret.splitlines()))
        return ret
    return ""

def identify(institution, titlu):

    return " : ".join([hashlib.md5(titlu.encode('utf-8')).hexdigest(), institution])

class SggSpider(scrapy.Spider):
    name = "sgg_spider"
    allowed_domains = ["www.sgg.ro"]
    start_urls = ['http://www.sgg.ro/legislativ/index.php/']

    def parse(self, response):
        links = response.css('a::attr(href)').extract()
        links = list(set([response.urljoin(link) for link in links if "domeniu.php" in link]))
        # yield scrapy.Request(response.urljoin('/legislativ/domeniu.php?id=84'), callback=self.parse_details)

        for link in links:
            yield scrapy.Request(response.urljoin(link), callback=self.parse_details)
            

    def parse_details(self, response):
        # response = get(response.url)

        institution = response.xpath('//h2/text()').extract()[0].strip() 
        logging.warn("scrapping: %s - %s"%(response.url, institution))

        for tr in response.xpath('//table[@class="fancy"]/tr'): 
            
            if tr.xpath('td[1]'):
                item = Item()
                titlu =  xtract(tr, 'td[1]//div/text()') 
                type_ = xtract(tr, 'td[2]//div//strong/text()')
                consult = xtract(tr, 'td[3]//div/text()')
                avizare = xtract(tr, 'td[4]//div/text()')
                avizori = xtract(tr, 'td[5]//div/text()')
                termen_avize = xtract(tr, 'td[6]//div/text()')
                mfp_mj = xtract(tr, 'td[7]//div/text()')
                reavizare = xtract(tr, 'td[8]//div/text()')
                init_1 = xtract(tr, 'td[9]//a/@href')
                init_2 = xtract(tr, 'td[10]//a/@href')
                final_1 = xtract(tr, 'td[11]//a/@href')
                final_2 = xtract(tr, 'td[12]//a/@href')

                docs = [{"type": "nota", "url": response.urljoin(f)} for f in [init_1, init_2, final_1, final_2] if f]

                item['identifier'] = identify(institution, titlu)
                item['title'] = titlu
                item['type'] = type_
                item['institution'] = "SGG"
                item['date'] = consult
                item['description'] = ""
                item['feedback_days'] = None
                item['contact'] = None
                item['documents'] = docs

                logging.warn("row: %s  "% item)
                yield item 

if __name__ == '__main__':
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'LOG_LEVEL' : 'WARNING'
    })

    process.crawl(SggSpider)
    process.start()