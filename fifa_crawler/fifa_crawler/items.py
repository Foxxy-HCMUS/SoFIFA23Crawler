# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FifaCrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    primary_position = scrapy.Field()
    positions = scrapy.Field()
    age = scrapy.Field()
    birth_date = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    Overall_Rating = scrapy.Field()
    Potential = scrapy.Field()
    Value = scrapy.Field()
    Wage = scrapy.Field()
    Preferred_Foot = scrapy.Field()
    Weak_Foot = scrapy.Field()
    pass
