# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class used_car_item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    price = scrapy.Field()
    notice = scrapy.Field()
    model = scrapy.Field()
    VIN = scrapy.Field()
    cylinders = scrapy.Field()
    drive = scrapy.Field()
    fuel =scrapy.Field()
    odometer = scrapy.Field()
    title_status = scrapy.Field()
    transmission = scrapy.Field()
    body_type = scrapy.Field()
    ex_color = scrapy.Field()
    in_color = scrapy.Field()
    condition = scrapy.Field()
    size = scrapy.Field()
    has_pic = scrapy.Field()
    has_map = scrapy.Field()
    pic_link = scrapy.Field()
    location = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    year_model = scrapy.Field()
    #veh_info = scrapy.Field()
    #contact = scrapy.Field()
    #engine = scrapy.Field()
    # image_link = scrapy.Field()
    # user_other_ads = scrapy.Field()
    #address = scrapy.Field()
    #seller = scrapy.Field()