import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from selenium.Java
import time
from random import randrange
from fake_useragent import UserAgent

# from random import randrange
ua = UserAgent()
ua_ = ua.random

import sys
import time
from random import randrange

import asyncio
import aiohttp

import requests
from bs4 import BeautifulSoup
import lxml
import json
import time


# url = 'https://www.flipkart.com/'


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": f'{ua}'  # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,
    # like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

print('start...')

# # 1
# #
# # # START of "Init..."
# # #
chrome_path = "./chromedriver.exe"

options = webdriver.ChromeOptions()
options.headless = False
options.add_argument("--incognito")
options.add_argument("start-maximized")
#
options.add_argument('--disable-blink-features=AutomationControlled')
#
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_experimental_option('useAutomationExtension', False)
browser = webdriver.Chrome(options=options, executable_path=chrome_path)
# # #
# # # END of "Init..."
#
browser.implicitly_wait(1.5)


start_ = True

url_ = []

for pg in range(1, 50):

    if start_:
        start_ = False
        url = f'https://www.viator.com/Iceland/d55-ttd'
    else:
        url = f'https://www.viator.com/Iceland/d55-ttd/{pg}'

    browser.get(url)

    first_pg_xp = '//*[@id="pagination"]/li[2]/a'
    start_time = time.time()
    try:
        WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.XPATH, first_pg_xp)))
    except:
        pass
    finish_time = time.time() - start_time
    print(f'Page = {pg}     FP: {finish_time}')

    source_html = browser.page_source
    # # запись СПАРСЕНОЙ инфы в ХТМЛ-файл
    # with open('index.html', 'w', encoding='utf-8') as file:
    #     file.write(source_html)

    soup = BeautifulSoup(source_html, 'lxml')

    el_links_ = soup.find_all("h2", class_='product-card-row-title mb-0 pt-md-4')
    for i in el_links_:
        el_link_ = i.find('a').get('href')
        print(el_link_)

        el_link = f'https://www.viator.com{el_link_}'
        url_.append(el_link)

# запись ссылок из СПИСКА в файл
with open('urls.txt', 'a', encoding='utf-8') as file:
    for url in url_:
        file.write(f'{url}\n')

