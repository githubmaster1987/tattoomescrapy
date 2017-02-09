# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

class TattoomescraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    tatt_title = scrapy.Field()
    tatt_city = scrapy.Field()
    tatt_style = scrapy.Field()
    tatt_id = scrapy.Field()
    tatt_breadcrumbs = scrapy.Field()
    tatt_person_name = scrapy.Field()
    tatt_phone_number = scrapy.Field()
    tatt_picture = scrapy.Field()
    tatt_address = scrapy.Field()
    tatt_coordinate = scrapy.Field()
    tatt_detail_url = scrapy.Field()
    tatt_page_url = scrapy.Field()
