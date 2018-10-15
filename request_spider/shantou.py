'''-*- coding: utf-8 -*-'''
import requests
from lxml import html
import re
import csv
import time
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}

ToDayTime = time.strftime("%Y-%m-%d", time.localtime())
ToDayTimeNOYEAR = time.strftime("%m-%d", time.localtime())
NameTitle = '汕头市人民政府'
# ToDayTime = '2018-08-20'
base_url = 'http://www.shantou.gov.cn/cnst/dbdh/wzdt.shtml'
def get_url():
    r = requests.get(base_url,headers = headers)
    enconding = requests.utils.get_encodings_from_content(r.text)
    r.encoding = 'utf - 8'
    brow = html.fromstring(r.text)
    AllLink = brow.xpath("//div[@class = 'wzdt_bg']/div/ul/li/a/@href")
    AllLink1 =[]
    for i in AllLink:
        link1 = i.split('/')
        if link1[1] == 'cnst':
            AllLink1.append('http://www.shantou.gov.cn' + i)
    return AllLink1

def open_urlList(url):
    r = requests.get(url,headers = headers)
    enconding = requests.utils.get_encodings_from_content(r.text)
    r.encoding = 'utf - 8'
    brow = html.fromstring(r.text)
    # Time = brow.xpath("//ul/li/span/text()")
    a = re.findall('(.*)'+ ToDayTime +'(.*)',r.text,re.M | re.I) or re.findall('(.*)'+ ToDayTimeNOYEAR +'(.*)',r.text,re.M | re.I)
    if a:
        for htmlword in a:
            Title = re.findall('blank"  >(.*?)</a>',htmlword[0])
            if Title:
                Link = re.findall('href=\"(.*?)\" targ',htmlword[0])
                LinkT = 'http://www.shantou.gov.cn' + Link[0]
                TitleT = Title[0]
                TimeT = ToDayTime
                p = requests.get(LinkT,headers = headers)
                enconding = requests.utils.get_encodings_from_content(p.text)
                p.encoding = 'utf - 8'
                brow1 = html.fromstring(p.text)
                word1 = brow1.xpath("//div[@id ='zoomcon']/ucapcontent/p/text()")
                wo = ''
                for i1 in range(len(word1)):
                    ss = word1[i1].strip()
                    if len(ss) > 0:
                        s = '<p>' + str(ss) + '</p>'
                        wo = wo + s
                print('------------------------------------',TitleT)
                print(LinkT)
                print(TimeT)
                print(wo)


    # for TimeN in Time:
    #     TimeS = TimeN.strip().replace(r'\r','').replace(r'\n','')
    #     if TimeS ==ToDayTime or TimeS == ToDayTimeNOYEAR:
    #         # xpathmark = "//ul/li/span/[contains(text()," + TimeS + ")]/../following-sibling::li[1]/text()"
    #         xpathmark = "//ul/li/span [contains(text()," + str(TimeS) + ")]/../following-sibling::li[1]/text()"
    #         print(xpathmark)
    #         title = brow.xpath(xpathmark)
    #         print(title)
    #
    #         print(TimeS)

urlList = get_url()
# print(urlList)
for url in urlList:
    open_urlList(url)