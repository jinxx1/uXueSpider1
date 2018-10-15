# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.link import Link
import time
from uxuepai.items import UxuepaiItem
ToDayTime = time.strftime("%Y/%m/%d", time.localtime())


class NdrcSpider(scrapy.Spider):
    name = 'ndrc'
    allowed_domains = ['ndrc.gov.cn']
    start_urls = ['http://www.ndrc.gov.cn/jsfb/wzdt/']

    def parse(self, response):
        link_extractor = LinkExtractor(attrs=('href','text'))
        links = link_extractor.extract_links(response)
        for url in links:
            yield scrapy.Request(url=url.url,callback = self.parseA)
    def parseA(self,response):
        Title = response.xpath("//div[@class ='box1 ']/ul[@class = 'list_02 clearfix']/li/a/text()").extract()
        Link  = response.xpath("//div[@class ='box1 ']/ul[@class = 'list_02 clearfix']/li/a/@href").extract()
        Time  = response.xpath("//div[@class ='box1 ']/ul[@class = 'list_02 clearfix']/li/font/text()").extract()
        for n in range(len(Time)):
            if Time[n] == ToDayTime:
            # if Time[n] == '2018/09/30':
                Linktemp = Link[n].split('/')
                if Linktemp[0] == ".":
                    url = response.url + Link[n].replace('./','/')
                    yield scrapy.Request(url=url,callback = self.parseB,meta={'TitleItem':Title[n]})

        tempLink = response.xpath("//h3/a/@href").extract()
        if tempLink:
            for tempurl1 in tempLink:
                if tempurl1.split('/')[0] == "..":
                    a1 = response.url.split('/')
                    a2 = a1[0] + '//' + a1[2] + '/' + a1[3] + '/'
                    tURL = a2 + tempurl1.replace('../','')
                    yield scrapy.Request(url=tURL,callback = self.parseA)

    def parseB(self,response):
        item = UxuepaiItem()

        # Title = response.xpath("//div[@class ='txt_title1 tleft']/text() | //div[@class ='txt_title1']/text() | //strong/font/text()").extract()
        word1 = response.xpath("//p/span/text() | //p/text() | //p/span/font/text()").extract()
        wo = ''
        for i1 in range(len(word1)):
            ss = word1[i1].strip()
            if len(ss) > 0:
                s = '<p>' + str(ss) + '</p>'
                wo = wo + s
        item['NameTOTALItem'] = '发改委'
        item['TitleItem'] = response.meta['TitleItem']
        item['LinkItem'] = response.url
        item['TimeItem'] = ToDayTime.replace('/', '')
        item['WordItem'] = wo
        yield item