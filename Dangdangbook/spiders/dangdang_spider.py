__author__ = 'shushi'
# -*- coding:utf-8 -*-

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.spiders import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.contrib.linkextractors import LinkExtractor
from Dangdangbook.items import DangDangbookItem

class Spider(Spider):
    name = 'dangdangbook'
    allowed_domains = ['category.dangdang.com/']
    start_urls = ['http://category.dangdang.com/cp01.54.06.12.00.00.html']
    # start_urls = ['http://category.dangdang.com/']
    url = 'http://category.dangdang.com/'
    # rules = (
    #     Rule(
    #         SgmlLinkExtractor(allow = r"/pg\d+-cp01.54.06.12.00.00"),
    #         callback = "parse",
    #         follow = True),
    #     Rule(
    #         SgmlLinkExtractor(allow = r"/cp01.54.06.12.00.00"),
    #         follow = True),
    # )

    def parse(self, response):
        print '=======parse========'
        print response.url
        sel = Selector(response)

        books = sel.xpath('//div[@class="con shoplist"]/ul/li/div[@class="inner"]')


        for i,book in enumerate(books):
            item = DangDangbookItem()
            name = book.xpath('//p[@class="name"]/a/text()').extract()[i]
            url = book.xpath("//p[@class='name']/a/@href").extract()[i]
            price = book.xpath("//p[@class='price']/span[@class='price_n']/text()").extract()[i]

            item['name'] = name
            item['url'] = url
            item['price'] = price

            yield item

        nextpage =  sel.xpath('//li[@class="next"]/a/@href').extract()
        if nextpage:
            nextpage = nextpage[0]
            nextlink = self.url + nextpage[1:]
            print nextlink
            yield Request(nextlink, callback = self.parse, dont_filter=True)





