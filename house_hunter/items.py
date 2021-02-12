# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HouseHunterItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class BinaItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    area = scrapy.Field()
    price_azn = scrapy.Field()
    category = scrapy.Field()
    n_floors = scrapy.Field()
    current_floor = scrapy.Field()
    n_rooms = scrapy.Field()
    deed_of_sale = scrapy.Field()
    link = scrapy.Field()
    updated_time = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()


