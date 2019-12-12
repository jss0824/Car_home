# -*- coding: utf-8 -*-
# -*- author: Jay -*-
import scrapy
import requests
from bs4 import BeautifulSoup
# from Car.Car.userAgents import get_random_agent
from scrapy.http import Request,FormRequest
from selenium import webdriver
from Car.items import CarItem
import datetime
class CarHomeSpider(scrapy.Spider):
    name = 'car_home'
    allowed_domains = ['https://www.autohome.com.cn']
    # start_urls = ['http://https://www.autohome.com.cn/']

    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }

    def start_requests(self):
        '''
        某些品牌会有多页数据， 只需在selenium获取源码之后判断一下是否有第二页按钮，更改一下代码就
        可以实现自动翻页功能，此项目只是自己爬着娱乐就不加上这个功能了
        :return: 
        '''
        #想爬取哪个页面就加入url
        url_dict = {
                  '宝马':'https://car.autohome.com.cn/price/brand-15.html',
                  '宝马2':'https://car.autohome.com.cn/price/brand-15-0-0-2.html',
                  '宝马3':'https://car.autohome.com.cn/price/brand-15-0-0-3.html',
                  '奔驰':'https://car.autohome.com.cn/price/brand-36.html',
                  '奔驰2': 'https://car.autohome.com.cn/price/brand-36-0-0-2.html',
                  '奔驰3': 'https://car.autohome.com.cn/price/brand-36-0-0-3.html',
                  '奥迪':'https://car.autohome.com.cn/price/brand-33.html',
                  '奥迪2': 'https://car.autohome.com.cn/price/brand-33-0-0-2.html',
        }
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
        soup = BeautifulSoup(content, 'lxml')
        data = soup.find_all('div',class_='list-cont-main')
        print(data)
        for i in data:
            car_type = i.a.string
            price = i.find_all('span',class_='lever-price red')
            for j in price:
                car_price = j.get_text()
                insertTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                item['brand'] = brand
                item['car_type'] = car_type
                item['car_price'] = car_price
                item['insertTime'] = insertTime
                yield item