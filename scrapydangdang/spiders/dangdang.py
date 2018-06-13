# -*- coding: utf-8 -*-
import scrapy
import json
from urllib.parse import urlencode
from scrapy import Request
from scrapydangdang.items import DangdangItem

class DangdangSpider(scrapy.Spider):
    name = 'dangdang'
    allowed_domains = ['www.dangdang.com']
    start_urls = ['http://www.dangdang.com/']

    def start_requests(self):
        pages = self.settings.get('PAGE')
        keyword = self.settings.get('KEYWORD')
        # self.logger.info('------------------------ ', pages, type(pages))
        for page in range(1, pages + 1):
            data = {'key': keyword, 'act': 'input', 'page_index': page}
            base_url = 'http://search.dangdang.com/?'
            params = urlencode(data)
            url = base_url + params
            yield Request(url=url, callback=self.parse)


    def parse(self, response):
        item = DangdangItem()
        results = response.xpath('//div[@id="search_nature_rg"]//ul[contains(@class,"bigimg")]//li')
        for result in results:
            item['title'] = result.xpath('.//a[@name="itemlist-title"]/@title').extract_first()
            item['buy_links'] = result.xpath('.//a[@name="itemlist-title"]/@href').extract_first()
            item['detail'] = result.xpath('.//p[@class="detail"]/text()').extract_first()
            item['now_price'] = result.xpath('.//p[@class="price"]//span[@class="search_now_price"]/text()').extract_first()
            item['pre_price'] = result.xpath('.//p[@class="price"]//span[@class="search_pre_price"]/text()').extract_first()
            item['discount'] = result.xpath('.//p[@class="price"]//span[@class="search_discount"]/text()').extract_first()
            item['favorites_ratio'] = result.xpath('.//span[@class="search_star_black"]//span/@style').extract_first()[7:]
            item['comment_num'] = result.xpath('.//p[@class="search_star_line"]//a[@class="search_comment_num"]/text()').extract_first()
            item['author'] = result.xpath('.//p[@class="search_book_author"]//a[starts-with(@name,"itemlist")]/text()').extract_first()
            if result.xpath('.//p[@class="search_book_author"]//span[2]/text()').extract_first():
                item['pub_time'] = result.xpath('.//p[@class="search_book_author"]//span[2]/text()').extract_first().replace(' /', '')
            item['publisher'] = result.xpath('.//p[@class="search_book_author"]//span//a[@name="P_cbs"]/text()').extract_first()

            yield item
