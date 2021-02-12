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
    #Edit these values
    tablename = 'houses'
    new = True
    def __init__(self):
        self.create_connection()
        if (not self.checkTableExists()) or self.new:
            self.create_table()
        

    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'crawler',
            passwd = '123456',
            database = 'houses'
        )
        self.curr = self.conn.cursor()
        pass
    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS houses""")
        self.curr.execute("""create table houses(
            id INT UNSIGNED NOT NULL UNIQUE,
            title TINYTEXT,
            area DECIMAL(10, 2),
            price_azn INT UNSIGNED,
            category TINYTEXT,
            n_floors TINYINT UNSIGNED,
            current_floor TINYINT UNSIGNED,
            n_rooms TINYINT UNSIGNED,
            deed_of_sale BOOLEAN,
            link TINYTEXT,
            updated_time DATETIME,
            latitude TINYTEXT,
            longitude TINYTEXT
        )""")

    def checkTableExists(self):
        cur = self.curr
        cur.execute("""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{0}'
            """.format(self.tablename))
        if cur.fetchone()[0] == 1:
            # cur.close()
            return True
        # cur.close()
        return False

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def checkIdExists(self, id):
        cur = self.curr
        cur.execute("""
            SELECT COUNT(1) FROM {}.{} WHERE {}.id = {}
            """.format(self.tablename, self.tablename, self.tablename, id))
        if cur.fetchone()[0] == 1:
            return True
        return False
    def store_db(self, item):
        if(not self.checkIdExists(item['id'])):
            self.curr.execute("""insert into houses values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (
                item['id'],
                item['title'],
                item['area'],
                item['price_azn'],
                item['category'],
                item['n_floors'],
                item['current_floor'],
                item['n_rooms'],
                item['deed_of_sale'],
                item['link'],
                item['updated_time'],
                item['latitude'],
                item['longitude']
                ))
            self.conn.commit()
        else:
            query = """update houses.houses 
            SET title = %s,
            area = %s,
            price_azn = %s,
            category = %s,
            n_floors = %s,
            current_floor = %s,
            n_rooms = %s,
            deed_of_sale = %s,
            link = %s,
            updated_time = %s,
            latitude = %s,
            longitude = %s WHERE id = %s;
            """
            self.curr.execute(query,(
                item['title'],
                item['area'],
                item['price_azn'],
                item['category'],
                item['n_floors'],
                item['current_floor'],
                item['n_rooms'],
                item['deed_of_sale'],
                item['link'],
                item['latitude'],
                item['updated_time'],
                item['longitude'],
                item['id']
            ))
            print("UPDATED!!!")