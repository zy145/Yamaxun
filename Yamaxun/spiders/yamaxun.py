# -*- coding: utf-8 -*-
import scrapy

from Yamaxun.items import YamaxunItem


class YamaxunSpider(scrapy.Spider):
    name = 'yamaxun'
    allowed_domains = ['amazon.cn']
    # start_urls = ['https://www.amazon.cn/s/ref=sr_pg_2?rh=n%3A664978051%2Cn%3A665002051%2Ck%3Aiphone&page=1']
    base_url = 'https://www.amazon.cn/gp/search/other/ref=amb_link_30552132_17?ie=UTF8&n=665002051&pickerToList=brandtextbin&pf_rd_m=A1AJ19PSB66TGU&pf_rd_s=merchandised-search-left-4&pf_rd_r=1RR3NYZGNKTT02HCXYJT&pf_rd_t=101&pf_rd_p=249713272&pf_rd_i=664978051'
    start_urls = [base_url]


    def parse(self, response):
        node_list = response.xpath('//ul/li/span/a')


        for node in node_list:
            pinpai_link = u"https://www.amazon.cn" + node.xpath('./@href').extract_first()

            pinpai_name = node.xpath('./span[1]/text()').extract_first()

            yield scrapy.Request(pinpai_link, callback=self.parse_item)


    def parse_item(self, response):


        titles = response.xpath('//div/div[3]/div[1]/a/h2/text()').extract()
        prices = response.xpath('//div/div[5]/div[1]/a/span[2]/text() | //div/div[6]/div[1]/a/span[2]/text()').extract()
        links = response.xpath('//li/div/div[3]/div[1]/a[1]/@href').extract()

        # pinpai_name = response.meta['name_item']

        for title, price, link in zip(titles, prices, links):
            item = YamaxunItem()

            # item['pinpai_name'] = pinpai_name
            item['title'] = title
            item['price'] = price
            item['link'] = link

            yield item

        next_links = response.xpath('//a[@id="pagnNextLink"]/@href').extract_first()
        if next_links:
            next_link = u'https://www.amazon.cn' + next_links

            yield scrapy.Request(next_link, callback=self.parse_item)











