# -*- coding: utf-8 -*-
import scrapy
import requests
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.link import Link
import time
import re
from uxuepai.items import UxuepaiItem
ToDayTime = time.strftime("%Y-%m-%d", time.localtime())
ToDayTime1 = time.strftime("%m-%d", time.localtime())



class SgSpider(scrapy.Spider):
    name = 'sg'
    allowed_domains = ['sg.gov.cn']
    start_urls = ['http://www.sg.gov.cn/fzgn/wzdt/']

    def parse(self, response):
        link_extractor = LinkExtractor(attrs=('href', 'text'))
        links = link_extractor.extract_links(response)
        for url in links:

            yield scrapy.Request(url=url.url, callback=self.parseA,meta = {'temurl':url.url},dont_filter=False)

    def parseA(self, response):
        Time = response.xpath("//ul/li/span/text()").extract()
        Title = response.xpath("//ul/li/span/preceding-sibling::a/text()").extract()
        Link = response.xpath("//ul/li/span/preceding-sibling::a/@href").extract()
        # print(Time)
        # print(Title)
        # print(Link)

        for n in range(len(Time)):
            if Time[n] == ToDayTime or Time[n] == ToDayTime1:
            # if Time[n] == '2018-09-30':
                Linktemp = Link[n].split('/')
                if Linktemp[0] == ".":
                    url = response.url + Link[n].replace('./', '')
                    # print(Title[n])
                    # print(url)
                    yield scrapy.Request(url=url, callback=self.parseB,)#meta={'TitleItem': Title[n]},dont_filter=False)

        w1 = ''
        try:
            reword = re.findall('<div class=\"gl-left\">(.*?)</div>', str(response.body), re.M | re.S)
            w1 = re.findall('href=\"(.*?)">', reword[0], re.M | re.S)
        except:
            pass
        if len(w1)>0:
            tempLink = []
            for w11 in w1:
                noVoice = re.findall('voice', w11)
                action = re.findall('action', w11)
                httpwww = re.findall('\/http:\/\/www', w11)
                if noVoice or action or httpwww:
                    continue
                # print(w11)
                if w11 == '../':
                    continue
                elif w11.split('/')[0] == '.':
                    continue
                tempLink.append(w11.replace('../', ''))
                if tempLink:
                    for tempurl1 in tempLink:
                        # a1 = response.url.split('/')
                        # a2 = a1[0].replace('\n', '') + '//' + a1[2] + '/' + a1[3] + '/'
                        tURL = response.meta['temurl'] + tempurl1
                        print(tURL)
                        print(response.meta['temurl'])


                    # actUrl = requests.get(tURL)
                    # if actUrl.status_code == 200:
                    # print(tURL)
                    # print(response.url)
                    print('-----------------------------------')
                    yield scrapy.Request(url=tURL, callback=self.parseA,dont_filter=False)

    def parseB(self, response):
        pass
        #
        # item = UxuepaiItem()
        #
        # # Title = response.xpath("//div[@class ='txt_title1 tleft']/text() | //div[@class ='txt_title1']/text() | //strong/font/text()").extract()
        # word1 = response.xpath("//p/span/text() | //p/text() | //p/span/font/text()").extract()
        # wo = ''
        # for i1 in range(len(word1)):
        #     ss = word1[i1].strip()
        #     if len(ss) > 0:
        #         s = '<p>' + str(ss) + '</p>'
        #         wo = wo + s
        # item['NameTOTALItem'] = '发改委'
        # item['TitleItem'] = response.meta['TitleItem']
        # item['LinkItem'] = response.url
        # item['TimeItem'] = ToDayTime.replace('/', '')
        # item['WordItem'] = wo
        # yield item
