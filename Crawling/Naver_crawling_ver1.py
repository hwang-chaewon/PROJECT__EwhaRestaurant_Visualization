# -*- coding: utf-8 -*-
"""Naver_crawling_ver2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Wp_ze3ph6JMGnT3E7Fw-gqWwFPOH59y5
"""

import pandas as pd
import numpy as np


df = pd.read_csv('shops.csv', sep=',')

df.info()

# 음식점 데이터만 쓸 겁니다
#f = df.loc[df["상권업종대분류명"=="음식"]]

columns = ['상호명', '상권업종대분류명','상권업종소분류명', 
           '시도명', '시군구명', '행정동명', '도로명주소', 
           '경도', '위도']
print(df.shape)
df=df[columns].copy()

df

df = df.loc[(df['시군구명'] == '서대문구')]

df_ = df.loc[df.상권업종대분류명 =="음식"]

dong=list(sorted(set(list((df_['행정동명'])))))
len(dong)
dong

dong_list=[]
for i in range(len(dong)): 
    dong_list.append(df_.loc[df.행정동명==dong[i]])
    i+=1
dong_list[0]

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time

chromedriver = 'C:/crawling/chromedriver.exe' 
driver = webdriver.Chrome(chromedriver) 
dong_list[0]['naver_keyword'] = dong_list[0]['행정동명']+'%20'+dong_list[0]['상호명']
dong_list[0]['naver_map_url'] = ''

# url 가져오기

for i, keyword in enumerate(dong_list[0]['naver_keyword'].tolist()):
    print("이번에 찾을 키워드 :", i, f"/ {dong_list[0].shape[0] -1} 행", keyword)
    try:
        naver_map_search_url = f"https://m.map.naver.com/search2/search.naver?query={keyword}&sm=hty&style=v5"
        driver.get(naver_map_search_url)
        
        time.sleep(3.5)
        dong_list[0].iloc[i,-1] = driver.find_element_by_css_selector("#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview").get_attribute('data-cid')

        #검색결과 없는 경우
    except Exception as e1:
        if "li:nth-child(1)" in str(e1):
            try:
                dong_list[0].iloc[i,-1] = driver.find_element_by_css_selector("#ct > div.search_listview._content._ctList > ul > li:nth-child(1) > div.item_info > a.a_item.a_item_distance._linkSiteview").get_attribute('data-cid')
                time.sleep(1)
            except Exception as e2:
                print(e2)
                dong_list[0].iloc[i,-1] = np.nan
                time.sleep(1)
        else:
            pass


driver.quit()


# url 만들어주기
dong_list[0]['naver_map_url'] = "https://m.place.naver.com/restaurant/" + dong_list[0]['naver_map_url']


# URL이 수집되지 않은 데이터는 제거합니다.
dong_list[0] = dong_list[0].loc[~dong_list[0]['naver_map_url'].isnull()]

dong_list[0]

CH = dong_list[0]

CH.to_csv("충현동.csv", mode='w')