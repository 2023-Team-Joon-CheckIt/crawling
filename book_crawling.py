import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

import time # time.sleep용
import os
import pandas as pd # csv파일 생성

URL = 'http://www.yes24.com/main/default.aspx' 

driver = webdriver.Chrome(executable_path='chromedriver')
driver.get(url=URL)
#REDAME에 폴더 구조 작성할 것

def setting():
    best_page = driver.find_element(By.XPATH, # 베스트 도서로 이동
        r'//*[@id="yesFixCorner"]/dl/dd/ul[1]/li[1]/a')
    best_page.send_keys(Keys.ENTER)
    time.sleep(0.5)

def move_to_another_book(book_number):
    print(book_number)
    time.sleep(3)
    
    # try:
    #     book = driver.find_element(By.XPATH, # book_number번째 책 상세정보로 이동
    #     f'//*[@id="bestList"]/ol/li[{book_number}]/p[1]/a')
    # except:
    book = driver.find_element(By.XPATH, # book_number번째 책 상세정보로 이동
    f'//*[@id="bestList"]/ol/li[{book_number}]/p[3]/a')
    book.send_keys(Keys.ENTER)

def get_info():
    title = driver.find_element(By.XPATH,
    r'//*[@id="yDetailTopWrap"]/div[2]/div[1]/div/h2').text

    author = driver.find_element(By.XPATH,
    r'//*[@id="yDetailTopWrap"]/div[2]/div[1]/span[2]/span[1]/a').text

    publisher = driver.find_element(By.XPATH,
    r'//*[@id="yDetailTopWrap"]/div[2]/div[1]/span[2]/span[2]/a').text

    try:
        img_url = driver.find_element(By.XPATH,
    r'//*[@id="yDetailTopWrap"]/div[1]/div/div[2]/div/span[1]/em/img').get_attribute('src')
    except:
        img_url = driver.find_element(By.XPATH,
    r'//*[@id="yDetailTopWrap"]/div[1]/div/span/em/img').get_attribute('src')
    
    table = driver.find_element(By.XPATH,
    r'//*[@id="infoset_specific"]/div[2]/div/table/tbody').text

    pages_weight_size = table.split('쪽수, 무게, 크기 ')[1].split('mm')[0].split("|")
    pages = pages_weight_size[0].split("쪽 ")[0]

    if(pages_weight_size.__len__() > 2):
        size = pages_weight_size[2].replace(' ','').split("*")
    else :
        size = pages_weight_size[1].replace(' ','').split("*")
    width = size[0]
    height = size[1]
    thickness = size[2]

    category = driver.find_element(By.XPATH,
    r'//*[@id="infoset_goodsCate"]/div[2]/dl[1]/dd/ul').text

    book_info = {'title': title, 'author': author, 'publisher': publisher,'img_url': img_url
                , 'pages': pages, 'width': width, 'height': height, 'thickness': thickness, 'category': category}
    print(book_info)
    return book_info
    

def go_back():
    driver.back()
    print('뒤로가기')

def create_csv_file(book_info):
    frame = pd.DataFrame([book_info])
    csv = 'DB_BOOKS.csv'
    if not os.path.exists(csv): # 파일 생성 로직
        frame.to_csv(csv, index=False, mode='w', encoding='utf-8-sig')
    else:
        frame.to_csv(csv, index=False, mode='a', encoding='utf-8-sig', header=False)
    time.sleep(3)

setting()
for i in range(40):
    move_to_another_book(i+1) # 1부터 40까지
    book_info = get_info()
    go_back()
    create_csv_file(book_info)