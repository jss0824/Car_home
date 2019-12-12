# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql
import hashlib

class CarPipeline(object):
    def process_item(self, item, spider):
        conn = pymysql.connect(host="106.13.169.200", user="root", passwd="fool123000!", db="汽车之家")
        cursor = conn.cursor()
        insertTime = ('').join(item['insertTime'])
        brand = ('').join(item['brand'])
        car_type = ('').join(item['car_type'])
        car_price = ('').join(item['car_price'])
        md5 = self.get_md5(car_type)
        sql = """insert into 汽车(insertTime,brand,car_type,car_price,md5) values ('%s','%s','%s','%s','%s') ON duplicate KEY UPDATE MD5 = MD5""" % (
            insertTime, brand, car_type, car_price, md5)
        print("正在存入数据库。。。。。。。。。。。。")
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return item

    def get_md5(self, nickname):
        str = nickname
        hl = hashlib.md5()
        hl.update(str.encode(encoding='utf-8'))
        return hl.hexdigest()
