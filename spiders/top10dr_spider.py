# -*- coding: utf-8 -*-
import time
import scrapy
import pdb
import traceback
from scrapy.spiders import Spider
from scrapy.selector import Selector
from top10dr.items import *
from sqlalchemy import *
from sqlalchemy.orm import *
import MySQLdb
import logging
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class AreaSpider(scrapy.Spider):
    name = "area"
    allowed_domains = ["top10dr.com"]
    start_urls = []
    for i in range(1,35):
        start_urls.append("http://www.top10dr.com/diqu/%d.html"%(i))

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="searchwrap"]/div[@class="searchss"]')
        diqu = sel.xpath('//div[@class="diquwrap"]/h5/span/text()').extract()
        items = []
        url = 'http://top10dr.com'

        for site in sites:
            item = AreaItem()
            link = site.xpath('a/@href').extract()
            name = site.xpath('a/img/@alt').extract()
            hospital = site.xpath('p/strong/text()').extract()
            item['link'] = [url + l.encode('utf-8') for l in link]
            item['hospital'] = [h.encode('utf-8') for h in hospital]
            item['name'] = [n.encode('utf-8') for n in name]
            item['area'] = [d.encode('utf-8') for d in diqu]
            items.append(item)
            logging.log(logging.INFO,'Appeding area item...')
        logging.log(logging.INFO,'Appeding area Done!')
        return items
class IllnessSpider(scrapy.Spider):
    name = "illness"
    allowed_domains = ["top10dr.com"]
    start_urls = ["http://www.top10dr.com/jibing.html"]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="index_content"]/div[@class="diquwrap"]/dl')
        items = []
        url = 'http://top10dr.com'

        for site in sites:
            item = IllnessItem()
            keshi_link = site.xpath('dt/a/@href').extract()
            keshi = site.xpath('dt/a/text()').extract()
            illness = site.xpath('dd/a/text()').extract()
            illness_link = site.xpath('dd/a/@href').extract()

            item['keshi'] = [k.encode('utf-8') for k in keshi]
            item['link_keshi'] = [url + l.encode('utf-8') for l in keshi_link]
            item['illness'] = [i.encode('utf-8') for i in illness]
            item['link_illness'] = [url + l.encode('utf-8') for l in illness_link]
            items.append(item)
            logging.log(logging.INFO,'Appeding illness item...')
        logging.log(logging.INFO,'Appeding illness Done!')
        return items
class OperationSpider(scrapy.Spider):
    name = "operation"
    allowed_domains = ["top10dr.com"]
    start_urls = ["http://www.top10dr.com/shoushu.html"]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="index_content"]/div[@class="diquwrap"]/dl')
        items = []
        url = 'http://top10dr.com'

        for site in sites:
            item = OperationItem()
            keshi_link = site.xpath('dt/a/@href').extract()
            keshi = site.xpath('dt/a/text()').extract()
            operation = site.xpath('dd/a/text()').extract()
            operation_link = site.xpath('dd/a/@href').extract()

            item['keshi'] = [k.encode('utf-8') for k in keshi]
            item['link_keshi'] = [url + l.encode('utf-8') for l in keshi_link]
            item['operation'] = [i.encode('utf-8') for i in operation]
            item['link_operation'] = [url + l.encode('utf-8') for l in operation_link]
            items.append(item)
            logging.log(logging.INFO,'Appeding operation item...')
        logging.log(logging.INFO,'Appeding operation Done!')
        return items
class YearSpider(scrapy.Spider):
    name = "year"
    allowed_domains = ["top10dr.com"]
    start_urls = ["http://www.top10dr.com/top10dr.html",
                  "http://www.top10dr.com/top10dr-2013.html",
                  "http://www.top10dr.com/top10dr-2014.html"]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="index_content"]/div[@class="tbs"]/div[@class="lis"]')
        year = sel.xpath('//div[@class="index_content"]/div[@class="tbs"]/h1/text()').extract()
        items = []
        url = 'http://top10dr.com'
        for site in sites:
            keshi = site.xpath('span/a/text()').extract()
            doctor_name = site.xpath('div[@class="liscon"]/ul/li/a/text()').extract()
            doctor_link = site.xpath('div[@class="liscon"]/ul/li/a/@href').extract()
            item = YearItem()
            item['keshi'] = [k.encode('utf-8') for k in keshi]
            item['name'] = [n.encode('utf-8') for n in doctor_name]
            item['dr_link'] = [url + l.encode('utf-8') for l in doctor_link]
            item['year'] = year[0]
            print '------------------'
            print len(item['year'])
            items.append(item)
            logging.log(logging.INFO,'Appeding yeard item...')
        logging.log(logging.INFO,'Appeding yeard Done!')
        return items
class DoctorFSpider(scrapy.Spider):
    name = "doctorf"
    allowed_domains = ["top10dr.com"]
    start_urls = []
    conn = MySQLdb.connect('localhost', 'root','admin', 'top10dr');
    cur = conn.cursor()
    cur.execute("SELECT DR_LK FROM YEAR_D")
    data = cur.fetchall()
    conn.close()
    for d in data:
        start_urls.append(d[0])
        # print d[0]
    def parse(self,response):

        url = 'http://top10dr.com'
        sel = Selector(response)
        sites = sel.xpath('//div[@class="index_content"]')
        name = sites.xpath('div[@class="inster_left fl"]/div[@class="inster_left_meun"]/h3/text()').extract()
        hospital = sites.xpath('div[@class="inster_left fl"]/div[@class="inster_left_meun"]/dl/dd[1]/a/text()').extract()
        illness =  sites.xpath('div[@class="inster_left fl"]/div[@class="inster_left_meun"]/dl/dd[2]/text()').extract()
        operation = sites.xpath('div[@class="inster_left fl"]/div[@class="inster_left_meun"]/dl/dd[3]/text()').extract()
        img = sites.xpath('div[@class="inster_right fr"]/div[@class="expert_end_con"]/div[@class="expert_end_text"]/img/@src').extract()
        desc = sites.xpath('div[@class="inster_right fr"]/div[@class="expert_end_con"]/div[@class="expert_end_text"]/p/text()').extract()
        keshi1 = sites.xpath('div[@class="inster_weizhi"]/a[2]/text()').extract()
        keshi2 = sites.xpath('div[@class="inster_weizhi"]/a[3]/text()').extract()
        items = []
        item = DoctorItem()
        item['illness'] = [i.encode('utf-8') for i in illness]
        item['hospital'] = [h.encode('utf-8') for h in hospital]
        item['name'] = [n.encode('utf-8') for n in name]
        item['keshi1'] = [k1.encode('utf-8') for k1 in keshi1]
        item['keshi2'] = [k2.encode('utf-8') for k2 in keshi2]
        if len(operation) > 0:
            item['operation'] = [o.encode('utf-8') for o in operation]
        else:
            item['operation'] = ['none']
        item['img'] = [url + i.encode('utf-8') for i in img]
        item['dr_link'] = [response.url.encode('utf-8')]
        if len(desc) > 0:
            item['description'] = [d.encode('utf-8') for d in desc]
        else:
            item['description'] = ['none']


        # desc_info = ''
        # for info in item['description']:
        #     desc_info = desc_info + info
        # print '-----------start--------'
        # print item['dr_link']
        # print item['illness'][0].decode('utf-8')
        # print item['hospital'][0].decode('utf-8')
        # print item['name'][0].decode('utf-8')
        # print item['operation'][0].decode('utf-8')
        # print item['img'][0].decode('utf-8')
        # print desc_info
        # print '--------end-----------'
        # pdb.set_trace()
        items.append(item)
        # logging.log(logging.INFO,'Appeding doctor item...')
        return items
class DoctorIllnessSpider(scrapy.Spider):
    name = "doctorill"
    allowed_domains = ["top10dr.com"]
    start_urls = []
    conn = MySQLdb.connect('localhost', 'root','admin', 'top10dr');
    cur = conn.cursor()
    cur.execute("SELECT ILL_LK FROM ILL_D")
    data = cur.fetchall()
    conn.close()
    for d in data:
        start_urls.append(d[0])
        # print d[0]
    def parse(self,response):

        url = 'http://top10dr.com'
        sel = Selector(response)
        sites = sel.xpath('//div[@class="expert_end_con"]/div[@class="expert_end_pic"]/ul/li')
        items = []
        for site in sites:
            name = site.xpath('a/img/@alt').extract()
            img =site.xpath('a/img/@src').extract()
            item = DoctorIllItem()
            item['illness_link'] = [response.url.encode('utf-8')]
            item['doctor_name']= [n.encode('utf-8') for n in name]
            item['doctor_img'] = [url + i.encode('utf-8') for i in img]
            items.append(item)
        return items
class DoctorOprSpider(scrapy.Spider):
    name = "doctoropr"
    allowed_domains = ["top10dr.com"]
    start_urls = []
    conn = MySQLdb.connect('localhost', 'root','admin', 'top10dr');
    cur = conn.cursor()
    cur.execute("SELECT OPR_LK FROM OPR_D")
    data = cur.fetchall()
    conn.close()
    for d in data:
        start_urls.append(d[0])
        # print d[0]
    def parse(self,response):

        url = 'http://top10dr.com'
        sel = Selector(response)
        sites = sel.xpath('//div[@class="expert_end_con"]/div[@class="expert_end_pic"]/ul/li')
        items = []
        for site in sites:
            name = site.xpath('a/img/@alt').extract()
            img =site.xpath('a/img/@src').extract()
            item = DoctorOprItem()
            item['operation_link'] = [response.url.encode('utf-8')]
            item['doctor_name']= [n.encode('utf-8') for n in name]
            item['doctor_img'] = [url + i.encode('utf-8') for i in img]
            items.append(item)
        return items
class DoctorKeshiSpider(scrapy.Spider):
    name = "doctorkeshi"
    allowed_domains = ["top10dr.com"]
    start_urls = []
    conn = MySQLdb.connect(host='localhost', user='root',passwd='admin', db='top10dr',charset='utf8');
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT KESHI_LK,KESHI_NM FROM ILL_D")
    data = cur.fetchall()
    conn.close()
    __keshi_link_dict = {}
    for d in data:
        start_urls.append(d[0])
        __keshi_link_dict.__setitem__(d[0],d[1])
        # print d[0]
    def parse(self,response):
        # url = 'http://top10dr.com'
        sel = Selector(response)
        sites = sel.xpath('//div[@class="inster_right fr"]/div[@class="expert_con"]/div[@class="expert_box"]')
        items = []
        for site in sites:
            hos_name = site.xpath('div[@class="expert_text fr"]/h3/a/text()').extract()
            description = site.xpath('div[@class="expert_text fr"]/p/text()').extract()
            item = DoctorKeshiItem()
            item['hospital_name'] = [hos_name[0].split('：')[0]]
            item['doctor_name'] = [hos_name[0].split('：')[1]]
            item['description'] = [d for d in description]
            item['keshi_link'] = [response.url]
            item['keshi_name'] = [self.__keshi_link_dict[response.url]]

            # print item['keshi_name'][0].decode('utf-8')
            # pdb.set_trace()

            # pdb.set_trace()
            # img =site.xpath('a/img/@src').extract()
            # item = DoctorOprItem()
            # item['operation_link'] = [response.url.encode('utf-8')]
            # item['doctor_name']= [n.encode('utf-8') for n in name]
            # item['doctor_img'] = [url + i.encode('utf-8') for i in img]
            items.append(item)
        return items