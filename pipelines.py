# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import log
from twisted.enterprise import adbapi
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
import urllib
import pdb
import  traceback

import MySQLdb
import MySQLdb.cursors
import logging

class AreaPipeline(object):
    def __init__(self):
        self.dbpool = adbapi.ConnectionPool('MySQLdb',db = 'top10dr',user = 'root',passwd = 'admin',cursorclass = MySQLdb.cursors.DictCursor,charset = 'utf8',use_unicode = False)
    def handle_error(self,e):
        logging.log(logging.INFO,'error!.')
    def process_item(self, item, spider):
        if spider.name not in ['area']:
            return item
        else:
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
            return item

    def _conditional_insert(self,tx,item):
        result=False
        if result:
            log.msg("Item already stored in db:%s" % item,level=log.DEBUG)
        else:
            # print 'start insert'
            tx.execute("insert into AREA_D(AREA_NM,HSP_NM,DR_LK,DR_NM) values(%s,%s,%s,%s);",
              (item['area'][0],
               item['hospital'][0],
               item['link'][0],
               item['name'][0]))
class IllnessPipeline(object):
    def __init__(self):
       self.dbpool = adbapi.ConnectionPool('MySQLdb',db = 'top10dr',user = 'root',passwd = 'admin',cursorclass = MySQLdb.cursors.DictCursor,charset = 'utf8',use_unicode = False)
    def handle_error(self,e):
        logging.log(logging.INFO,'error!.')
    def process_item(self, item, spider):
        if spider.name not in ['illness']:
            return item
        else:
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
            return item
    def _conditional_insert(self,tx,item):
        result=False
        if result:
            log.msg("Item already stored in db:%s" % item,level=log.DEBUG)
        else:
            for i in range(len(item['illness'])):
                tx.execute("insert into ILL_D(KESHI_NM,KESHI_LK,ILL_NM,ILL_LK) values(%s,%s,%s,%s);",
                  (item['keshi'][0],
                   item['link_keshi'][0],
                   item['illness'][i],
                   item['link_illness'][i]))
class OperationPipeline(object):
    def __init__(self):
       self.dbpool = adbapi.ConnectionPool('MySQLdb',db = 'top10dr',user = 'root',passwd = 'admin',cursorclass = MySQLdb.cursors.DictCursor,charset = 'utf8',use_unicode = False)
    def handle_error(self,e):
        logging.log(logging.INFO,'error!.')
    def process_item(self, item, spider):
        if spider.name not in ['operation']:
            return item
        else:
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
            return item
    def _conditional_insert(self,tx,item):
        result=False
        if result:
            log.msg("Item already stored in db:%s" % item,level=log.DEBUG)
        else:
            for i in range(len(item['operation'])):
                tx.execute("insert into OPR_D(KESHI_NM,KESHI_LK,OPR_NM,OPR_LK) values(%s,%s,%s,%s);",
                  (item['keshi'][0],
                   item['link_keshi'][0],
                   item['operation'][i],
                   item['link_operation'][i]))
class YearPipeline(object):
    def __init__(self):
       self.dbpool = adbapi.ConnectionPool('MySQLdb',db = 'top10dr',user = 'root',passwd = 'admin',cursorclass = MySQLdb.cursors.DictCursor,charset = 'utf8',use_unicode = False)
    def handle_error(self,e):
        logging.log(logging.DEBUG,'error!.')
    def process_item(self, item, spider):
        if spider.name not in ['year']:
            return item
        else:
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
            return item
    def _conditional_insert(self,tx,item):
        result=False
        if result:
            logging.log(logging.INFO,"Item already stored in db")
        else:
            for i in range(len(item['name'])):
                # print '-------start--------'
                # print(item['keshi'][0]).decode('utf-8')+'1111111111111'
                # print(item['name'][i].decode('utf-8'))+'222222222222'
                # print(item['dr_link'][i].decode('utf-8'))+'3333333333'
                # print len(item['year'])
                # print '-------end--------'
                # pdb.set_trace()
                tx.execute("insert into YEAR_D(KESHI_NM,DR_NM,DR_LK,YEAR_FG) values(%s,%s,%s,%s);",(item['keshi'][0],item['name'][i],item['dr_link'][i],''.join(item['year'])))
class DoctorFPipeline(object):
    def __init__(self):
       self.dbpool = adbapi.ConnectionPool('MySQLdb',db = 'top10dr',user = 'root',passwd = 'admin',cursorclass = MySQLdb.cursors.DictCursor,charset = 'utf8',use_unicode = False)
    def handle_error(self,e):
        logging.log(logging.DEBUG,'error!.')
    def process_item(self, item, spider):
        if spider.name not in ['doctorf']:
            return item
        else:
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
            return item
    def _conditional_insert(self,tx,item):
        result=False
        if result:
            logging.log(logging.INFO,"Item already stored in db")
        else:
            desc_info = ''
            for info in item['description']:
                desc_info = desc_info + info
            # print '-----------start--------'
            # print item['dr_link'][0]
            # print item['illness'][0].decode('utf-8')
            # print item['hospital'][0].decode('utf-8')
            # print item['name'][0].decode('utf-8')
            # print item['operation'][0].decode('utf-8')
            # print item['img'][0].decode('utf-8')
            # print desc_info
            # print '--------end-----------'

            tx.execute("insert into DR_F(DR_NM,HSP_NM,ILL_NM,OPR_NM,IMG_LK,DR_LK,KESHI1_NM,KESHI2_NM,DESC_INFO) values(%s,%s,%s,%s,%s,%s,%s,%s,%s);",
              (item['name'][0],
               item['hospital'][0],
               item['illness'][0],
               item['operation'][0],
               item['img'][0],
               item['dr_link'][0],
               item['keshi1'][0],
               item['keshi2'][0],
               str(desc_info).strip()))
class DoctorIllPipeline(object):
    def __init__(self):
       self.dbpool = adbapi.ConnectionPool('MySQLdb',db = 'top10dr',user = 'root',passwd = 'admin',cursorclass = MySQLdb.cursors.DictCursor,charset = 'utf8',use_unicode = False)
    def handle_error(self,e):
        logging.log(logging.DEBUG,'error!.')
    def process_item(self, item, spider):
        if spider.name not in ['doctorill']:
            return item
        else:
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
            return item
    def _conditional_insert(self,tx,item):
        result=False
        if result:
            logging.log(logging.INFO,"Item already stored in db")
        else:
            tx.execute("insert into DR_ILL(DR_NM,IMG_LK,ILL_LK) values(%s,%s,%s);",
              (item['doctor_name'][0],
               item['doctor_img'][0],
               item['illness_link'][0]))
class DoctorOprPipeline(object):
    def __init__(self):
       self.dbpool = adbapi.ConnectionPool('MySQLdb',db = 'top10dr',user = 'root',passwd = 'admin',cursorclass = MySQLdb.cursors.DictCursor,charset = 'utf8',use_unicode = False)
    def handle_error(self,e):
        logging.log(logging.DEBUG,'error!.')
    def process_item(self, item, spider):
        if spider.name not in ['doctoropr']:
            return item
        else:
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
            return item
    def _conditional_insert(self,tx,item):
        result=False
        if result:
            logging.log(logging.INFO,"Item already stored in db")
        else:
            tx.execute("insert into DR_OPR(DR_NM,IMG_LK,OPR_LK) values(%s,%s,%s);",
              (item['doctor_name'][0],
               item['doctor_img'][0],
               item['operation_link'][0]))
class DoctorKeshiPipeline(object):
    def __init__(self):
       self.dbpool = adbapi.ConnectionPool('MySQLdb',db = 'top10dr',user = 'root',passwd = 'admin',cursorclass = MySQLdb.cursors.DictCursor,charset = 'utf8',use_unicode = False)
    def handle_error(self,e):
        logging.log(logging.DEBUG,'error!.')
    def process_item(self, item, spider):
        if spider.name not in ['doctorkeshi']:
            return item
        else:
            query = self.dbpool.runInteraction(self._conditional_insert, item)
            query.addErrback(self.handle_error)
            return item
    def _conditional_insert(self,tx,item):
        result=False
        if result:
            logging.log(logging.INFO,"Item already stored in db")
        else:
            # print item['hospital_name'][0].decode('utf-8')
            # print item['doctor_name'][0].decode('utf-8')
            # print item['keshi_link'][0]
            # print item['description'][0].decode('utf-8')
            # pdb.set_trace()
            tx.execute("insert into DR_KESHI(DR_NM,HSP_NM,KESHI_LK,KESHI_NM,DR_DESC) values(%s,%s,%s,%s,%s);",
              (item['doctor_name'][0],
               item['hospital_name'][0],
               item['keshi_link'][0],
               item['keshi_name'][0],
               (''.join(item['description'])).strip()))