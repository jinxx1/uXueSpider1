'''-*- coding: utf-8 -*-'''

import requests
from bs4 import BeautifulSoup
import lxml
from multiprocessing import Process, Queue
import random
import json
import time
import requests
import re


def test(ip, port):

    try:
        telnetlib.Telnet(ip, port=port, timeout=20)
    except:
        a = 'no'
    else:
        a = 'ok'
    return a

class Proxies(object):
    def __init__(self, page=3):
        self.proxies = []
        self.verify_pro = []
        self.page = page
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,zh-TW;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
        }
        self.get_proxies()
        self.get_proxies_nn()



    def get_proxies(self):
        # page = random.randint(1,10)
        page = 1
        page_stop = 2
        while page < page_stop:
            url = 'http://www.xicidaili.com/nt/%d' % page
            html = requests.get(url, headers=self.headers).content
            soup = BeautifulSoup(html, 'lxml')
            ip_list = soup.find(id='ip_list')
            for odd in ip_list.find_all(class_='odd'):
                protocol = odd.find_all('td')[5].get_text().lower()+'://'
                self.proxies.append(protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
            page += 1

    def get_proxies_nn(self):
        page = 1
        page_stop = 2
        while page < page_stop:
            url = 'http://www.xicidaili.com/nn/%d' % page
            html = requests.get(url, headers=self.headers).content
            soup = BeautifulSoup(html, 'lxml')
            ip_list = soup.find(id='ip_list')
            for odd in ip_list.find_all(class_='odd'):
                protocol = odd.find_all('td')[5].get_text().lower() + '://'
                self.proxies.append(protocol + ':'.join([x.get_text() for x in odd.find_all('td')[1:3]]))
            page += 1

    def verify_proxies(self):
        old_queue = Queue()
        new_queue = Queue()
        # print ('verify proxy........')
        works = []
        for _ in range(15):
            works.append(Process(target=self.verify_one_proxy, args=(old_queue,new_queue)))
        for work in works:
            work.start()
        for proxy in self.proxies:
            old_queue.put(proxy)
        for work in works:
            old_queue.put(0)
        for work in works:
            work.join()
        self.proxies = []
        while 1:
            try:
                self.proxies.append(new_queue.get(timeout=1))
            except:
                break
        print ('verify_proxies done!')

    def verify_one_proxy(self, old_queue, new_queue):
        while 1:
            proxy = old_queue.get()
            if proxy == 0:break
            protocol = 'https' if 'https' in proxy else 'http'
            proxies = {protocol: proxy}
            try:
                if requests.get('http://www.baidu.com', proxies=proxies, timeout=2).status_code == 200:
                    # print ('success %s' % proxy)
                    new_queue.put(proxy)
            except:
                pass



if __name__ == '__main__':
    a = Proxies()
    a.verify_proxies()
    # print (a.proxies)
    proxie = a.proxies
    # print(proxie)
    for ips in proxie:
        ip = re.findall(r'://(.*?):', ips)
        # print(ips)
        port = ips.split(':')
        ipT = ip[0]
        portT = port[len(port) - 1]
        # print(ipT)
        # print(portT)
        a = test(ipT, portT)
        if a == 'ok':
            print('发现一个可用的：',ips)
            with open('proxies.txt', 'a') as f:
                f.write(ips + '\n')


