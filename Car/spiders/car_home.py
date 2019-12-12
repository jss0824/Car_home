# -*- coding: utf-8 -*-
# -*- author: Jay -*-
import scrapy
import requests
from bs4 import BeautifulSoup

from scrapy.http import Request,FormRequest
from selenium import webdriver
from Car.items import CarItem
import datetime
from Car.brand_url import brand_url_dict
class CarHomeSpider(scrapy.Spider):
    name = 'car_home'
    allowed_domains = ['https://www.autohome.com.cn']
    # start_urls = ['http://https://www.autohome.com.cn/']

    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }

    def start_requests(self):
        '''
        某些品牌会有多页数据， 只需在selenium获取源码之后判断一下是否有第二页按钮
        :return:
        '''
        #导入所有汽车品牌主页
        url_dict = brand_url_dict()

        for url in url_dict:
            yield Request(url_dict[url], meta={'brand':url},callback=self.parse, headers=self.headers, dont_filter=True)
    def parse(self, response):
        item = CarItem()
        brand = response.meta['brand']
        opt = webdriver.ChromeOptions()
        opt.set_headless()
        opt.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(options=opt)
        driver.get(response.url)
        content = driver.page_source                #使用selenium获取源码后进行解析
        driver.close()
        soup = BeautifulSoup(content, 'lxml')
        data = soup.find_all('div',class_='list-cont-main')
        # print(data)

        page = soup.find_all('div',class_='page')
        pages_list = []
        for i in page:
            for url in i:
                pages_list.append('https://car.autohome.com.cn/' + url.attrs['href'])

        pages = pages_list[2:-1]
        # print('字典',pages)
        # print('字段长度',len(pages))

        if len(pages) == 0:
            for i in data:
                car_type = i.a.string
                print(car_type)
                price = i.find_all('span',class_='lever-price red')
                for j in price:
                    car_price = j.get_text()
                    print(car_price)
                    insertTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    item['brand'] = brand
                    item['car_type'] = car_type
                    item['car_price'] = car_price
                    item['insertTime'] = insertTime
                    yield item
        else:
            for i in data:
                car_type = i.a.string
                print(car_type)
                price = i.find_all('span',class_='lever-price red')
                for j in price:
                    car_price = j.get_text()
                    print(car_price)
                    insertTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    item['brand'] = brand
                    item['car_type'] = car_type
                    item['car_price'] = car_price
                    item['insertTime'] = insertTime
                    yield item

            for url in pages:
                yield Request(url, meta={'brand':brand},callback=self.parse_nextpage,headers=self.headers, dont_filter=True)

    def parse_nextpage(self,response):
        item = CarItem()
        brand = response.meta['brand']
        opt = webdriver.ChromeOptions()
        opt.set_headless()
        opt.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(options=opt)
        driver.get(response.url)
        content = driver.page_source  # 使用selenium获取源码后进行解析
        driver.close()
        soup = BeautifulSoup(content, 'lxml')
        data = soup.find_all('div', class_='list-cont-main')
        # print(data)
        for i in data:
            car_type = i.a.string
            print(car_type)
            price = i.find_all('span', class_='lever-price red')
            for j in price:
                car_price = j.get_text()
                print(car_price)
                insertTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                item['brand'] = brand
                item['car_type'] = car_type
                item['car_price'] = car_price
                item['insertTime'] = insertTime
                yield item