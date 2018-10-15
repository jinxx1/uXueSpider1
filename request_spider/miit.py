'''

http://miit.gov.cn/n1146290/n1146392/index.html
时政要闻
http://miit.gov.cn/n1146290/n1146397/index.html
领导活动
http://miit.gov.cn/n1146290/n4388791/index.html
重点工作
http://miit.gov.cn/n1146290/n1146402/index.html
工作动态
http://miit.gov.cn/n1146290/n1146407/index.html
对外交流





'''

import requests
from lxml import html
import re
import csv
import time
ToDayTime = time.strftime("%Y%m%d", time.localtime())
import lxml
import lxml.html as HTML
import lxml.etree as etree
base_url =[
'http://miit.gov.cn/n1146290/n1146392/index.html',
#时政要闻
'http://miit.gov.cn/n1146290/n1146397/index.html',
#领导活动
'http://miit.gov.cn/n1146290/n4388791/index.html',
#重点工作
'http://miit.gov.cn/n1146290/n1146402/index.html',
#工作动态
'http://miit.gov.cn/n1146290/n1146407/index.html',
#对外交流
]

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}

NameTitleList = ['工信部-时政要闻','工信部-领导活动','工信部-重点工作','工信部-工作动态','工信部-对外交流']



for n in range(len(base_url)):
    NameTitle = NameTitleList[n]
    r = requests.post(base_url[n],headers = headers)
    enconding = requests.utils.get_encodings_from_content(r.text)
    r.encoding = 'utf - 8'
    brow = html.fromstring(r.text)
    Link = brow.xpath("//li/a/@href")
    Title = brow.xpath("//li/a/text()")
    Time = brow.xpath("//li/span/a/text()")
    for i in range(len(Title)):

        TimeT = Time[i].split('-')[0] + Time[i].split('-')[1] + Time[i].split('-')[2]
        if TimeT != ToDayTime:
            continue
        TitleT = Title[i]
        LinkT = Link[i].replace('../../', 'http://miit.gov.cn/')

        r1 = requests.get(LinkT,headers = headers)
        if r1.status_code == 404:
            continue
        enconding = requests.utils.get_encodings_from_content(r1.text)
        r1.encoding = 'utf - 8'
        brow1 = html.fromstring(r1.text)
        word1 = brow1.xpath("//p/text()")
        wo = ''
        for i1 in range(len(word1)):
            ss = word1[i1].strip()
            if len(ss) > 0:
                s = '<p>' + str(ss) + '</p>'
                wo = wo + s
        with open('miit.csv', 'a', encoding='utf-8', newline='') as csvfile:
            write = csv.writer(csvfile)
            write.writerow([NameTitle, TitleT, LinkT, TimeT, wo])
            csvfile.flush()
            print(NameTitle)
            print(TitleT)
            print(LinkT)
            print(TimeT)
            print(wo)

print('-------------the end--------------')