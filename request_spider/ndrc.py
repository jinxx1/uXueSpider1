'''-*- coding: utf-8 -*-'''
import requests
from lxml import html
import re
import csv
import time
ToDayTime = time.strftime("%Y%m%d", time.localtime())

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}

base_url =[
'http://www.ndrc.gov.cn/govszyw/',
'http://www.ndrc.gov.cn/gzdt/',
'http://www.ndrc.gov.cn/dffgwdt/',
'http://www.ndrc.gov.cn/jjxsfx/',
'http://www.ndrc.gov.cn/tpxw/',
'http://bgt.ndrc.gov.cn/zcfb/',
'http://bgt.ndrc.gov.cn/xxtdt/',
'http://zys.ndrc.gov.cn/xwfb/',
'http://zys.ndrc.gov.cn/gzdt/',
'http://ghs.ndrc.gov.cn/gzdt/',
'http://ghs.ndrc.gov.cn/zcfg/',
'http://zhs.ndrc.gov.cn/gzyzcdt/',
'http://zhs.ndrc.gov.cn/zcdt/',
'http://dqs.ndrc.gov.cn/gzdt/',
'http://dqs.ndrc.gov.cn/qygh/',
'http://dqs.ndrc.gov.cn/qyhz/gnqyhz/',
'http://dqs.ndrc.gov.cn/kcxfz/',
'http://dqs.ndrc.gov.cn/fpkf/',
'http://dqs.ndrc.gov.cn/dkzy/dkzydt/',
'http://jtyss.ndrc.gov.cn/gzdt/',
'http://jtyss.ndrc.gov.cn/zcfg/',
'http://jtyss.ndrc.gov.cn/zdxm/',
'http://jtyss.ndrc.gov.cn/zcfg/',
'http://jtyss.ndrc.gov.cn/hysj/',
'http://jtyss.ndrc.gov.cn/dffz/',
'http://gjss.ndrc.gov.cn/gjsgz/',
'http://gjss.ndrc.gov.cn/gzdtx/',
'http://gjss.ndrc.gov.cn/ghzc/',
'http://gjss.ndrc.gov.cn/tbxwx/',
'http://shs.ndrc.gov.cn/gzdt/',
'http://shs.ndrc.gov.cn/shfzdt/',
'http://shs.ndrc.gov.cn/zcyj/',
'http://pszx.ndrc.gov.cn/gzdt/',
]

NameTitleList = [
'发改委-时政要闻',
'发改委-工作动态',
'发改委-地方动态',
'发改委-经济形势分析',
'发改委-图片新闻',
'发改委-办公厅-政策发布',
'发改委-办公厅-系统动态',
'发改委-政研室-新闻发布',
'发改委-政研室-工作动态',
'发改委-发展规划司-工作动态',
'发改委-发展规划司-政策法规',
'发改委-国民经济综合司-工作要情',
'发改委-国民经济综合司-政策要情',
'发改委-地区经济司-工作动态',
'发改委-地区经济司-区域规划和区域政策',
'发改委-地区经济司-国内区域合作',
'发改委-地区经济司-区域治理和可持续发展',
'发改委-地区经济司-扶贫开发',
'发改委-地区经济司-对口支援',
'发改委-基础产业司-工作动态',
'发改委-基础产业司-政策法规',
'发改委-基础产业司-重大工程',
'发改委-基础产业司-政策法规',
'发改委-基础产业司-行业数据',
'发改委-基础产业司-地方发展',
'发改委-高技术产业司-高技术工作',
'发改委-高技术产业司-发展动态',
'发改委-高技术产业司-政策发布',
'发改委-高技术产业司-图片新闻',
'发改委-社会发展司-社会发展工作',
'发改委-社会发展司-社会发展动态',
'发改委-社会发展司-社会发展规划、政策与研究',
'发改委-评审中心-工作动态',
]
for n in range(len(NameTitleList)):
# for n in range(0,4):
    NameTitle = NameTitleList[n]
    r = requests.get(base_url[n],headers = headers)
    enconding = requests.utils.get_encodings_from_content(r.text)
    r.encoding = 'utf - 8'
    brow = html.fromstring(r.text)
    print(n)

    Link = brow.xpath("//div[@class = 'box1 ']/ul/li/a/@href|//div[@class = 'box1 ']/div/ul/li/p/a/@href")
    if n>=4:
        Title = brow.xpath("//div[@class = 'box1 ']/ul/li/a/@title|//div[@class = 'box1 ']/div/ul/li/p/a/@title")
    else:
        Title = brow.xpath("//div[@class = 'box1 ']/ul/li/a/text()|//div[@class = 'box1 ']/div/ul/li/p/a/text()")
    Time = brow.xpath("//div[@class = 'box1 ']/ul/li/font/text()")
    # print(r.text)
    # print(Title)
    # print(Link)

    for i in range(len(Link)):
        TitleT = Title[i]
        pathurl = 'http://' + base_url[n].split('/')[2] + '/' + base_url[n].split('/')[3] + '/'
        LinkT = Link[i].replace('./', pathurl)
        # print(len(Title),len(Link),i)
        # TimeT = Time[i].split('/')[0] + Time[i].split('/')[1] + Time[i].split('/')[2]
        if n >=4:
            TimeT = LinkT.split('/')[5].split('t')[1].split('_')[0]
        else:
            TimeT = Time[i].split('/')[0] + Time[i].split('/')[1] + Time[i].split('/')[2]
        if TimeT != ToDayTime:
            continue
        r1 = requests.get(LinkT,headers = headers)
        if r1.status_code == 404:
            continue
        enconding = requests.utils.get_encodings_from_content(r1.text)
        r1.encoding = 'utf - 8'
        brow1 = html.fromstring(r1.text)
        word1 = brow1.xpath("//p/text()|//p/span/text() | //p/span//*/text() | //div[@class = 'TRS_Editor']/text() | //p/font/text()")
        wo = ''
        for i1 in range(len(word1)):
            ss = word1[i1].strip()
            if len(ss) > 0:
                s = '<p>' + str(ss) + '</p>'
                wo = wo + s
        with open('ndrc.csv', 'a', encoding='utf-8', newline='') as csvfile:
            write = csv.writer(csvfile)
            write.writerow([NameTitle, TitleT, LinkT, TimeT, wo,base_url[n],n])
            csvfile.flush()
        print(NameTitleList[n])
        print(TimeT)
        print(TitleT)
        print(wo)
        print('-------------')
print('------the end ---------')