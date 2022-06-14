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

import re

import pandas as pd


# url = 'https://www.flipkart.com/'


headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "User-Agent": f'{ua}'  # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,
    # like Gecko) Chrome/96.0.4664.45 Safari/537.36"
}

print('start...')

# # #         = 1 =
# # #
# # # # START of "Init..."
# # # #
# chrome_path = "./chromedriver.exe"
#
# options = webdriver.ChromeOptions()
# options.headless = False
# options.add_argument("--incognito")
# options.add_argument("start-maximized")
# #
# options.add_argument('--disable-blink-features=AutomationControlled')
# #
# options.add_experimental_option("excludeSwitches", ["enable-logging"])
# options.add_experimental_option('useAutomationExtension', False)
# browser = webdriver.Chrome(options=options, executable_path=chrome_path)
# # # #
# # # # END of "Init..."
# #
# browser.implicitly_wait(1.5)
#
#
# start_ = True
#
# url_ = []
#
# for pg in range(1, 50):
#
#     if start_:
#         start_ = False
#         url = f'https://www.viator.com/Iceland/d55-ttd'
#     else:
#         url = f'https://www.viator.com/Iceland/d55-ttd/{pg}'
#
#     browser.get(url)
#
#     first_pg_xp = '//*[@id="pagination"]/li[2]/a'
#     start_time = time.time()
#     try:
#         WebDriverWait(browser, 15).until(EC.element_to_be_clickable((By.XPATH, first_pg_xp)))
#     except:
#         pass
#     finish_time = time.time() - start_time
#     print(f'Page = {pg}     FP: {finish_time}')
#
#     source_html = browser.page_source
#     # # запись СПАРСЕНОЙ инфы в ХТМЛ-файл
#     # with open('index.html', 'w', encoding='utf-8') as file:
#     #     file.write(source_html)
#
#     soup = BeautifulSoup(source_html, 'lxml')
#
#     el_links_ = soup.find_all("h2", class_='product-card-row-title mb-0 pt-md-4')
#     for i in el_links_:
#         el_link_ = i.find('a').get('href')
#         el_link = f'https://www.viator.com{el_link_}'
#         url_.append(el_link)
#
# # запись ссылок из СПИСКА в файл
# with open('urls.txt', 'a', encoding='utf-8') as file:
#     for url in url_:
#         file.write(f'{url}\n')
# #
# # #         = End of 1 =


start_time = time.time()

ele_list = []
ele_info = []

async def get_page_data(session, link_, str_num):
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": f'{ua_}'
    }

    print(f"start...")

    global ele_list
    global ele_info


    async with session.get(url=link_, headers=headers) as response:

        response_text = await response.text()
        soup = BeautifulSoup(response_text, 'lxml')

        # # ЗАЩИТА от БАНА!!!
        # time.sleep(randrange(1, 2))

        # print(f'str_num: {str_num}')

        url_ = link_
        print(f'url: {url_}')

        try:
            name_ = soup.find('h1', class_='title__1Wwg title2__C3R7').text
        except:
            name_ = 'NONE'
        print(f'name: {name_}')

        try:
            r_c_ = soup.find('div', class_='ratingReviews__2CyF').text
            review_count = str(re.findall(r'\d+[,.]?\d+', r_c_))
            review_count_ = str(review_count).replace("['", "").replace("']", "").replace(r",", "")
        except:
            review_count_ = 'NONE'
        print(f'review_count: {review_count_}')


        try:
            total_rating_ = soup.find('span', class_='averageRatingValue__Q1ep').text
        except:
            total_rating_ = 'NONE'
        # print(f'total_rating: {total_rating_}')

        breadcrumb_ = soup.find_all('li', class_='crumb__7IyR')#.text
        str_ = ''
        for i in breadcrumb_:
            str_ += i.text + ' > '
        breadcrumb_ = str_[0:-2]
        # print(f'breadcrumb: {breadcrumb_}')

        try:
            price_ = soup.find('span', class_='moneyView__2HPx').text
        except:
            price_ = 'NONE'
        # print(f'price: {price_}')

        try:
            overview_ = soup.find('div', class_='overviewWrapper__bMs4').find('div').find('div').text
        except:
            overview_ = 'NONE'
        # print(f'overview_: {overview_}')

        departure_points = []
        try:
            departure__ = soup.find('title__1Wwg title4__AH0S')
            #
            # SCRYPT!!!
            #
            script_all = soup.find_all('script')
            try:
                script_ = str(re.findall('\"locationPoints\":(.*?)\"dropOffPoints\":', str(script_all[5]))).\
                        replace("['[{\"locationCategory", "[{\"locationCategory"). \
                        replace("}}],']", "}}]"). \
                        replace("\\", "_")
            except:
                pass

            try:
                script_new = str(re.findall('\"pageModel\":(.*?)\"pageMeta\":', str(script_all[5]))).\
                        replace("['{\"destinationId", "{\"destinationId"). \
                        replace("}}},']", "}}}"). \
                        replace("\\", "_"). \
                        replace('__\"', '__*')
            except:
                pass

            with open(f'_my_script_new_{str_num}.json.', 'w', encoding='utf-8') as file:
                # json.dump(json_all, file, indent=4, ensure_ascii=False)
                file.write(script_new)


            if script_ != "['[],']":
                # with open(f'_my_json_{str_num}.json.', 'w', encoding='utf-8') as file:
                #     # json.dump(json_all, file, indent=4, ensure_ascii=False)
                #     file.write(script_)
                #
                # with open(f"_my_json_{str_num}.json", "r", encoding='utf-8') as read_file:
                #     data_ = json.load(read_file)

                try:
                    data_ = json.loads(script_)
                except:
                    pass


                departure_points = []

                for y in range(1, 100):
                    try:
                        ele_label_ = f"{data_[y]['locationData']['location']['label']}"
                        #print(f'{y} --> {ele_label_}')
                        departure_points.append(ele_label_)
                    except:
                        break
        except:
            pass
        # print(f'departure_points: {departure_points}')

        # departure_time
        try:
            departure_time_ = soup.find('div', class_='departureTimeLocation__3gU_').text
        except:
            departure_time_ = 'NONE'
        # print(f'departure_time: {departure_time_}')

        # included

        # with open(f'_my_json555_{str_num}.json.', 'w', encoding='utf-8') as file:
        #     #json.dump(script_new, file, indent=4, ensure_ascii=False)
        #     file.write(script_new)
        #
        #
        # with open(f"_my_json555_{str_num}.json", "r", encoding='utf-8') as read_file:
        #     ddd = json.load(read_file)

        try:
            ddd = json.loads(script_new)
        except:
            pass



        included_ = ddd['product']['description']['inclusions']['features']
        # print(f'included: {included_}')

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # try:
        #     what_to_expect_ = soup.find('span', class_='overflow-wrap: break-word;').text
        # except:
        #     what_to_expect_ = 'NONE'
        what_to_expect_ = ddd['product']['itinerary']['introduction']
        print(f'what_to_expect: {what_to_expect_}')
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        addtional_info_ = ddd['product']['description']['additionalInfo']['features']
        cancelation_policy_ = ddd['product']['description']['cancellationPolicy']['policies']

        # photo
        traveler_photos_count = ddd['product']['mediaGallery']['travellerImagesCount']
        traveler_photos_ = []

        for f in range(traveler_photos_count):
            traveler_photos_.append((ddd['product']['mediaGallery']['travellerImages'][f]['fullSizeImage']['src']).replace('__u002F', '/'))

        # reviews
        reviews_ = []
        try:
            reviews_count = len(ddd['product']['reviews']['viatorReviews'])

            for r in range(reviews_count):
                reviews_.append(
                    {
                        "title": ddd['product']['reviews']['viatorReviews'][r]['title'],
                        "rating": ddd['product']['reviews']['viatorReviews'][r]['rating'],
                        "user": ddd['product']['reviews']['viatorReviews'][r]['user']['nickName'],
                        "date": ddd['product']['reviews']['viatorReviews'][r]['publishedAt'],
                        "text": ddd['product']['reviews']['viatorReviews'][r]['text']
                    }
                )
        except:
            pass

        ele_info.append(
            {
                "url": url_,
                "name": name_,
                "review_count": review_count_,
                "total_rating": total_rating_,
                "breadcrumb": breadcrumb_,
                "price": price_,
                "overview": overview_,
                "departure_and_return": {
                    'departure_points': departure_points,
                    'departure_time': departure_time_
                },
                "included": included_,
                "what_to_expect": what_to_expect_,
                "addtional_info": addtional_info_,
                "cancelation_policy": cancelation_policy_,
                "traveler_photos": traveler_photos_,
                "reviews": reviews_
             }
        )


async def gather_data():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": f'{ua_}'
    }

    # читаю ССЫЛКИ из ранее созданного файла
    # !!! ОБРЕЗАЮ СИМВОЛ ПЕРЕНОСА СТРОКИ !!!
    with open('urls.txt') as file:
        url_list = [line.strip() for line in file.readlines()]

    page_count = len(url_list)
    # print(f'PAG.: {page_count}')

    async with aiohttp.ClientSession() as session:
        # try:
        #     ele_link_ = soup.find('a', {'name': 'business-unit-card'}).get('href')
        # except Exception as e:
        #     print(e)

        tasks = []

        # for i in range(1, page_count):
        #for url_ in enumerate(url_list[0:1]):
        str_num = 0
        for url_ in url_list[0:1154]:
        #for url_ in url_list:
            # for i in range(1, 2):

            # print(f'URL -------> {url_}')

            task = asyncio.create_task(get_page_data(session, url_, str_num))
            tasks.append(task)
            str_num += 1


        await asyncio.gather(*tasks)


        # # ЗАЩИТА от БАНА!!!
        # time.sleep(randrange(0, 2))
        # print(f'Обработал {i} / {page_count}')

def json_to_csv():
    df = pd.read_json(r'_my_json2022.json')
    df.to_csv(r'_my_json2022.csv', index=None)

def main():
    # json_to_csv()
    asyncio.run(gather_data())

    finish_time = time.time() - start_time

    # with open('test.txt', 'w+', encoding='utf-8') as file:
    #     file.write(ele_info)

    with open('_my_json2022.json.', 'w', encoding='utf-8') as file:
        json.dump(ele_info, file, indent=4, ensure_ascii=False)

    # with open('out.json', 'w+', encoding='utf-8') as file:
    #     json.dump(ele_list, file, indent=4, ensure_ascii=False)

    print(f"TIME: {finish_time}")
    # cur_time = datetime.now().strftime("%d.%m.%Y %H:%M")
    # print(f"TIME_now: {cur_time}")







if __name__ == "__main__":
    # print(sys.version_info[0])
    # ЗАПЛАТКА!!! Блок выпадания ОШИБКИ под виндой...
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    # asyncio.run(main())
    main()


# # 1
# #
# # запись СПАРСЕНОЙ инфы в ХТМЛ-файл
# with open('index.html', 'w', encoding='utf-8') as file:
#     file.write(source_html)
#pagination_count = soup.find('div', {"id": "ajaxPaging-product"}).find('ul', class_='product-pagination js-pagination').find_all('li', class_='pagination-item')[-1].text.strip()

# with open("index.html", "r", encoding='utf-8') as f:
#     source_html = f.read()
