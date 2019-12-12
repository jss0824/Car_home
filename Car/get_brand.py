from selenium import webdriver
import requests
from lxml import etree
from bs4 import BeautifulSoup
import time
import json
def get_brand_url():
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    }


    url = 'https://www.autohome.com.cn/car/'
    opt = webdriver.ChromeOptions()
    # opt.set_headless()
    opt.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(options=opt)
    driver.get(url)
    for i in range(1, 25):
        driver.execute_script('window.scrollTo(0,{})'.format(i * 10000))
        time.sleep(4)
    content = driver.page_source
    # driver.close()
    soup = BeautifulSoup(content, 'lxml')
    data = soup.find_all(attrs={'vos':'gs'}, class_='uibox')

    brand_url = {}
    for i in data:
        for j in i.find_all('dt'):
            brand_url[j.div.string] = 'https://' + j.a.attrs['href']

    # print(brand)
    print(len(brand_url))
    print(brand_url)
    brand_url = json.dumps(brand_url)
    driver.close()
    return  brand_url

