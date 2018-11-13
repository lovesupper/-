# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class DsSpider(CrawlSpider):
    name = 'ds'
    allowed_domains = ['www.dushu.com']
    start_urls = ['http://www.dushu.com/book/1163.html']
    #/book/1107_2.html
    rules = (
        Rule(LinkExtractor(allow=r'/book/1163_\d+.html'),
                           callback='parse_item',
                           follow=False),
    )

    def parse_item(self, response):
        i = {}
        #1 确定我要爬取哪些数据 然后去item中定义
        li_list = response.xpath('//div[@class="bookslist"]/ul/li')
        for li in li_list:
            i['src'] = li.xpath('./div/div/a/img/@data-original').extract_first()
            i['alt'] = li.xpath('./div/div/a/img/@alt').extract_first()
            i['author'] = li.xpath('./div/p[1]/a/text()').extract_first()
            yield i
