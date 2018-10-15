'''-*- coding: utf-8 -*-'''

import requests
from lxml import html
import re
import csv
import time
ToDayTime = time.strftime("%Y%m%d", time.localtime())
import lxml
import lxml.html as HTML
from pyquery import PyQuery as pq
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
}
base_url = 'http://www.zs.gov.cn/main/zwgk/list/town/index.action'
NameTitleList = '中山人民政府网站'
def get_url(url,headers):
    r = requests.get(base_url,headers = headers)
    enconding = requests.utils.get_encodings_from_content(r.text)
    r.encoding = 'utf - 8'
    brow = html.fromstring(r.text)
    AllLink = brow.xpath("//div[@class = 'aside']/div/div/ul/li/a/@href")
    allLinkt = []
    for i in range(len(AllLink)-1):
        allLinkt.append('http://www.zs.gov.cn' + AllLink[i])
    return allLinkt


def url_id(id,headers):
    data1 = {
        'did': id,
        'curPage': 1,
        'pageSize': 22,
        'ts': 1537952595837,
    }
    r = requests.get('http://www.zs.gov.cn/ajax/infoPage.action?did=' + str(id), headers=headers, data=data1)
    return r.json()

def url_noid(url,headers):
    jsonR = []
    rWord = requests.get(url, headers=headers)
    regex = re.findall('getOpenData\(\'(.*?)\'\, \'(.*?)\'',rWord.text,re.S)
    try:
        tokentype = re.findall('token=(.*?)\';',rWord.text,re.S)[0]
    except:
        pass
    for i in range(len(regex)):
        pubcode = regex[i][0]
        codetype = regex[i][1]
        base0_url = 'http://www.zs.gov.cn/ajax/openInfoPage.action?'
        data1 = {
            'curPage': 1,
            'pageSize': 22,
            'pubcode': pubcode,
            'type': 'scatcode',
            'code': codetype,
            'token': tokentype,
        }
        r = requests.get(base0_url,headers=headers,params=data1,cookies=rWord.cookies.get_dict())
        jsonR.append(r.json())
    return jsonR

def json_data(jsonR):
    for i in range(len(jsonR['rows'])):
        Time = jsonR['rows'][i]['date'].replace('-','')
        Id = jsonR['rows'][i]['id']
        Title = jsonR['rows'][i]['title']
        if Time != ToDayTime:
            continue
        try:
            Link = jsonR['rows'][i]['url']
        except:
            Link = jsonR['rows'][i]['link']
        if len(Link) > 0:
            Link = 'http://www.zs.gov.cn' + Link
        else:
            Link = 'http://www.zs.gov.cn/main/zwgk/newsview/index.action?id=' + str(Id)
        r = requests.get(Link,headers = headers)
        enconding = requests.utils.get_encodings_from_content(r.text)
        r.encoding = 'utf - 8'
        brow1 = html.fromstring(r.text)
        word1 = brow1.xpath("//p/span/text() | //p/text() | //div[@class = 'xs_cnt']/text()")
        wo = ''
        for i1 in range(len(word1)):
            ss = word1[i1].strip()
            if len(ss) > 0:
                s = '<p>' + str(ss) + '</p>'
                wo = wo + s
        print(NameTitleList)
        print(Title)
        print(Time)
        print(Link)
        print(wo)
        with open('zs.csv', 'a', encoding='utf-8', newline='') as csvfile:
            write = csv.writer(csvfile)
            write.writerow([NameTitleList, Title, Link, Time, wo])
            csvfile.flush()
        print("************************************")



urlList = get_url(base_url,headers)
for i in range(len(urlList)):
    urlcut = re.findall('did=(\d*)',urlList[i])
    if len(urlcut) > 0:
        urlid = urlcut[0]
        url = urlList[i]
        jsonR = url_id(urlid,headers)
        json_data(jsonR)
    else:
        jsonR = url_noid(urlList[i],headers)
        for i in range(len(jsonR)):
            json_data(jsonR[i])






