# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CarReviewItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    model = scrapy.Field()
    maker = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    comment = scrapy.Field()
    score = scrapy.Field()
    pros = scrapy.Field()
    cons = scrapy.Field()
    link = scrapy.Field()