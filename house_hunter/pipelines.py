# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class HouseHunterPipeline:
    def process_item(self, item, spider):
        return item


class BinaPipeline:
    def __init__(self):
        self.create_connection()
        self.create_table()
    
    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'crawler',
            passwd = '1234',
            database = 'houses'
        )
        self.curr = self.conn.cursor()
        pass
    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS houses""")
        self.curr.execute("""create table houses(
            id INT UNSIGNED,
            price_azn INT UNSIGNED,
            category TEXT,
            n_floors TINYINT UNSIGNED,
            current_floor TINYINT UNSIGNED,
            n_rooms TINYINT UNSIGNED,
            deed_of_sale BOOLEAN
        )""")
    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute("""insert into houses values (%s, %s, %s, %s, %s, %s, %s)""", (
            item['id'],
            item['price_azn'],
            item['category'],
            item['n_floors'],
            item['current_floor'],
            item['n_rooms'],
            item['deed_of_sale']
            ))
        self.conn.commit()

