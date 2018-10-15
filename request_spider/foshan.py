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
NameTitle = '佛山市人民政府'
# ToDayTime = '2018-08-20'
base_url = 'http://www.foshan.gov.cn/wzbz/wzdt/'
def get_url():
    r = requests.get(base_url,headers = headers)
    enconding = requests.utils.get_encodings_from_content(r.text)
    r.encoding = 'utf - 8'
    brow = html.fromstring(r.text)
    AllLink = brow.xpath("//ul[@class = 'maplist']/li/a/@href")
    otherLink = [
        'http://www.foshan.gov.cn/zwgk/zwdt/jryw/',
        'http://www.foshan.gov.cn/zwgk/zwdt/bmdt/',
        'http://www.foshan.gov.cn/zwgk/zwdt/wqdt/ccq/',
        'http://www.foshan.gov.cn/zwgk/zwdt/wqdt/nhq/',
        'http://www.foshan.gov.cn/zwgk/zwdt/wqdt/sdq/',
        'http://www.foshan.gov.cn/zwgk/zwdt/wqdt/gmq/',
        'http://www.foshan.gov.cn/zwgk/zwdt/wqdt/ssq/',
        'http://www.foshan.gov.cn/zwgk/zcwj/zcjd/',
        'http://www.foshan.gov.cn/zwgk/zcwj/gfxwj/',

    ]
    return AllLink + otherLink

def open_urlList(url):
    r = requests.get(url,headers = headers)
    enconding = requests.utils.get_encodings_from_content(r.text)
    r.encoding = 'utf - 8'
    a = re.findall('(.*)'+ ToDayTime +'(.*)',r.text,re.M | re.I)
    print(a)
    if a:
        for i in range(len(a)):
            try:
                # Title= re.findall('([\\u3400-\\u9FFF].*?)<', str(a[i]))[0].replace('\"','').replace('>','')
                Title= re.findall('l>(.*?)</a>', str(a[i]))[0].replace('\"','').replace('>','')

                Link = re.findall('href="\.\/(.*?)\"',str(a[i]))[0]
                urlLink = url + Link
                word = requests.get(urlLink, headers=headers)
                enconding = requests.utils.get_encodings_from_content(word.text)
                word.encoding = 'utf - 8'
                brow = html.fromstring(word.text)
                word1 = brow.xpath("//p//text() | //div[@id = 'idc_text']//p/text() | //div[@id = 'idc_text']//div/text()  ")
                wo = ''
                for i1 in range(len(word1)):
                    ss = word1[i1].strip()
                    if len(ss) > 0:
                        s = '<p>' + str(ss) + '</p>'
                        wo = wo + s
                with open('foshan.csv', 'a', encoding='utf-8', newline='') as csvfile:
                    write = csv.writer(csvfile)
                    write.writerow([NameTitle, Title, urlLink, ToDayTime.replace('-',''), wo])
                    csvfile.flush()
                    print(NameTitle)
                    print(Title)
                    print(urlLink)
                    print(ToDayTime.replace('-',''))
                    print(wo)


            except:
                print('有问题')


urlList = get_url()
for i in range(len(urlList)):
    # if i == 0:
        # urlList[i] = urlList[i] + '/jryw/'
    if urlList[i] == 'http://wz.foshan.gov.cn/':
        continue
    print(i,urlList[i])
    open_urlList(urlList[i])

