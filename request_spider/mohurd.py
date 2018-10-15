# -*- coding: utf-8 -*-
import requests
from lxml import html
import re
import csv
import time
ToDayTime = time.strftime("%Y%m%d", time.localtime())
import lxml
import lxml.html as HTML
import lxml.etree as etree
base_url = 'http://jzsc.mohurd.gov.cn/asite/jsbpp/jsp/news_list.jsp'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}
classModle = ['jsbpp_news_tzgg','jsbpp_news_hydt','jsbpp_news_pqgs','jsbpp_news_phgg']
NameTitleList = ['住建部-文件通知','住建部-行业动态','住建部-公示','住建部-公告']
for n in range(len(classModle)):
    for x in range(1,6):
        data = {
            'data-callback': 'lastRefreshMoreLink',
            'data-contentid': 'news_tab2',
            'class': 'formsubmit',
            'data-url': 'news_list.jsp',
            'item_code': classModle[n],
            '$pg': x,
        }
        NameTitle = NameTitleList[n]
        r = requests.post(base_url,headers = headers,data=data)
        enconding = requests.utils.get_encodings_from_content(r.text)
        r.encoding = 'utf - 8'
        brow = html.fromstring(r.text)
        Link = brow.xpath("//div[@class = 'news_group_title']/a[@class = 'formsubmit']/@data-exturl")
        Title = brow.xpath("//div[@class = 'news_group_title']/a[@class = 'formsubmit']/text()")
        Time = brow.xpath("//div[@class = 'news_group_date']/text()")
        for i in range(len(Title)):
            Time1 = Time[i].replace('\r','').replace('\n','').replace('\t','').split(" ")
            num = re.sub(r'\.*$', "", Time1[0]).split('\xa0')[0].split('-')
            TimeT = num[0] + num[1]  + num[2]
            if int(TimeT) != int(ToDayTime):
                continue
            TitleT = Title[i].replace('\r','').replace('\n','').replace('\t','')
            LinkT = Link[i]
            r1 = requests.get(LinkT)
            if r1.status_code == 404:
                continue
            enconding = requests.utils.get_encodings_from_content(r1.text)
            r1.encoding = 'utf - 8'
            brow1 = html.fromstring(r1.text)
            word1 = brow1.xpath("//p/text()")
            wo = ''
            for i1 in range(len(word1)):
                ss = word1[i1].replace(u'\3000', u'').strip()
                if len(ss) > 0:
                    s = '<p>' + str(ss) + '</p>'
                    wo = wo + s
            with open('mohurd.csv','a',encoding='utf-8',newline= '') as csvfile:
                write = csv.writer(csvfile)
                write.writerow([NameTitle,TitleT,LinkT,TimeT,wo])
print("-------The End--------")

'''
jsbpp_news_tzgg文件通知
jsbpp_news_mtjj媒体聚焦
jsbpp_news_hydt行业动态
jsbpp_news_pqgs公示
jsbpp_news_phgg公告
'''

