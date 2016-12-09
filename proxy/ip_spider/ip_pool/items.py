# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IPItem(scrapy.Item):
    ipAddress = scrapy.Field(serializer=str)
    port = scrapy.Field(serializer=str)
    physicalAddress = scrapy.Field(serializer=str)
    anonymous = scrapy.Field(serializer=str)
    type = scrapy.Field(serializer=str)
    speed = scrapy.Field(serializer=str)
    connectDuration = scrapy.Field(serializer=str)
    liveTime = scrapy.Field(serializer=str)
    lastVerified = scrapy.Field(serializer=str)
