# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# from Lagou.items import LagouJobItemLoader,LagouJobItem


class ShantouSpider(scrapy.Spider):
    pass
# class ShantouSpider(CrawlSpider):
    name = 'shantou'

    allowed_domains = ['shantou.gov.cn']
    start_urls = ['http://www.shantou.gov.cn/cnst/dbdh/wzdt.shtml']
    # alldomains = ['shantou.gov.cn']

    # link = LinkExtractor(allow_domains=allowed_domains)  # .link_extractor
    #
    # links = link.extract_links(response)
    # for url in links:
    #     print(url.url, url.text)
    # rules = (
    #     # Rule(LinkExtractor(allow=r'href="(.*?)"')),
    #     Rule(LinkExtractor(allow_domains=allowed_domains), callback='parse', follow=True),
    # )
    # links = LinkExtractor(allow = "href=\"\./(.*?)\"")
    # le = LinkExtractor(restrict_xpaths=("//a/@herf")).extract_links(response)
    # link = le.extract_links(response)
    # rules = [Rule(link_extractor=links,callback='parse',follow=True)]
    # restrict_xpath = '//div[@class = "wzdt_bg"]//@href'
    # allow = '/cnst/.+\.shtml'
    # rules = {
    #     Rule(LinkExtractor(),callback="parse",follow=True)
    #
    # }
    # def request_url(self,response):
    #
    denydomian = ['english.shantou.gov.cn','www.shantou.gov.cn/cnst/appxz/mapp.shtml']

    def parse(self, response):
        # link = LinkExtractor(allow_domains=ShantouSpider.allowed_domains,deny_domains=ShantouSpider.denydomian,deny='\.apk')  # .link_extractor
        # links = link.extract_links(response)
        links = [
            'http://www.shantou.gov.cn/cnst/styw/list.shtml',
            'http://www.shantou.gov.cn/cnst/bmdt/list.shtml',

        ]
        for urlparse in links:
            yield scrapy.Request(url=urlparse, callback=self.parseA,dont_filter=True)


    def parseA(self, response):
        titel = response.xpath("//*[@name = 'ArticleTitle']/@content").extract()
        print(response.url)
        if len(titel)>0:
            print(titel)
        else:
            link = LinkExtractor()
            print(link)
            links = link.extract_links(response)
            print(links)
            for urlparse in links:
                print('没有title的链接： ',urlparse.url)
                yield scrapy.Request(url=urlparse.url, callback=self.parseA,dont_filter=False)


    def parseB(self, response):
        titel = response.xpath("//*[@name = 'ArticleTitle']/@content").extract()
        if len(titel) > 0:
            # print(titel[0].strip())
            print(titel)
            print(response.url)
        # if titel:
        #     print(titel[0].strip())
        #     print(response.url)
        else:
            link = LinkExtractor(allow_domains=ShantouSpider.allowed_domains,
                                 deny_domains=ShantouSpider.denydomian,deny='\.apk')  # .link_extractor
            links = link.extract_links(response)
            for urlparse in links:

                yield scrapy.Request(url=response.url, callback=self.parseA,)


    def parseC(self, response):
        titel = response.xpath("//ucaptitle/text()").extract()
        if titel:
            yield scrapy.Request(url=response.url, callback=self.parseB)
        else:
            link = LinkExtractor(allow_domains=ShantouSpider.allowed_domains,
                                 deny_domains=ShantouSpider.denydomian,
                                 deny='\.apk')  # .link_extractor
            links = link.extract_links(response)
            for urlparse in links:
                yield scrapy.Request(url=urlparse.url, callback=self.parseA)




        '''
        
    def parseB(self, response):
        titel = response.xpath("//ucaptitle/text()").extract()
        if titel:
            print(titel[0].strip())
        else:
            link = LinkExtractor(allow_domains=ShantouSpider.allowed_domains,deny_domains='english.shantou.gov.cn')  # .link_extractor
            links = link.extract_links(response)
            for urlparse in links:
                yield scrapy.Request(url=urlparse.url, callback=self.parseC, dont_filter=False)
        print(response.url)

    def parseC(self, response):
        titel = response.xpath("//ucaptitle/text()").extract()
        if titel:
            print(titel[0].strip())
        else:
            link = LinkExtractor(allow_domains=ShantouSpider.allowed_domains,
                                 deny_domains='english.shantou.gov.cn')  # .link_extractor
            links = link.extract_links(response)
            for urlparse in links:
                yield scrapy.Request(url=urlparse.url, callback=self.parse, dont_filter=False)
            print(response.url)
'''
        # print(response.url)
        # pass
        # print(response.url)
        # links = response.xpath("//div[@class = 'wzdt_bg']//@href").extract()

        # alldomains = ['shantou.gov.cn']
        #
        # link = LinkExtractor(restrict_xpaths='//div[@class = "wzdt_bg"]//@href')
        # link = LinkExtractor(allow_domains=alldomains)
        #
        # links = link.extract_links(response)
        # for url in links:
        #     print(url.url,url.text)


