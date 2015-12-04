# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Top10DrItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class DoctorItem(scrapy.Item):
    name = scrapy.Field()
    hospital = scrapy.Field()
    illness = scrapy.Field()
    operation = scrapy.Field()
    img = scrapy.Field()
    dr_link = scrapy.Field()
    description = scrapy.Field()
    keshi1=scrapy.Field()
    keshi2=scrapy.Field()
class AreaItem(scrapy.Item):
    hospital = scrapy.Field()
    area = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
class IllnessItem(scrapy.Item):
    keshi = scrapy.Field()
    illness = scrapy.Field()
    link_keshi = scrapy.Field()
    link_illness = scrapy.Field()
class OperationItem(scrapy.Item):
    keshi = scrapy.Field()
    operation = scrapy.Field()
    link_operation = scrapy.Field()
    link_keshi = scrapy.Field()
class YearItem(scrapy.Item):
    keshi = scrapy.Field()
    name = scrapy.Field()
    dr_link = scrapy.Field()
    year =scrapy.Field()
class DoctorIllItem(scrapy.Item):
    doctor_img = scrapy.Field()
    doctor_name = scrapy.Field()
    illness_link = scrapy.Field()
class DoctorOprItem(scrapy.Item):
    doctor_img = scrapy.Field()
    doctor_name = scrapy.Field()
    operation_link = scrapy.Field()
class DoctorKeshiItem(scrapy.Item):
    doctor_name = scrapy.Field()
    keshi_link = scrapy.Field()
    keshi_name = scrapy.Field()
    hospital_name = scrapy.Field()
    description = scrapy.Field()