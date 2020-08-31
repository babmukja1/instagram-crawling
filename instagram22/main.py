# 필요 패키지들 import 하기

from urllib.request import urlopen # 인터넷 url를 열어주는 패키지
from urllib.parse import quote_plus # 한글을 유니코드 형식으로 변환해줌
from bs4 import BeautifulSoup
from selenium import webdriver # webdriver 가져오기
import time # 크롤링 중 시간 대기를 위한 패키지
import warnings # 경고메시지 제거 패키지
from selenium.webdriver.common.keys import Keys
from urllib.request import Request
from selenium import webdriver
from tqdm import tqdm

import pandas as pd
warnings.filterwarnings(action='ignore')

warnings.filterwarnings(action='ignore') # 경고 메세지 제거

SCROLL_DOWN_TIME = 1.5 # 스크롤 내리는 시간

# 인스타 그램 url 생성
baseUrl = "https://www.instagram.com/explore/tags/"
plusUrl = input('검색할 태그를 입력하세요 : ')
url = baseUrl + quote_plus(plusUrl)

driver = webdriver.Chrome(
    executable_path="C:/Users/ILIFO-050/Desktop/instagram22/chromedriver.exe"
)
driver.get(url)


time.sleep(3)

# 로그인 하기
login_section = '//*[@id="react-root"]/section/nav/div[2]/div/div/div[3]/div/span/a[1]/button'
driver.find_element_by_xpath(login_section).click()
time.sleep(2)


elem_login = driver.find_element_by_name("username")
elem_login.clear()
elem_login.send_keys('ID')

elem_login = driver.find_element_by_name('password')
elem_login.clear()
elem_login.send_keys('PASSWORD')

time.sleep(1)

xpath = """//*[@id="loginForm"]/div/div[3]/button/div"""
driver.find_element_by_xpath(xpath).click()

time.sleep(4)

xpath = """//*[@id="react-root"]/section/main/div/div/div/div/button"""
driver.find_element_by_xpath(xpath).click()

time.sleep(4)

# 총 게시물 숫자 불러오기
pageString = driver.page_source
bsObj = BeautifulSoup(pageString, 'lxml')
temp_data = bsObj.find_all(name='meta')[-1]
temp_data = str(temp_data)
start = temp_data.find('게시물') + 4
end = temp_data.find('개')
total_post_data = temp_data[start:end]
print("총 {0}개의 게시물이 검색되었습니다.".format(total_post_data))
print('태그를 수집하는 중입니다...')

#==================================================================================================
reallink = [] # 전체 게시물 링크 저장

# url 화면에서 스크롤을 내리면서 게시물 크롤링
while True:
    pageString = driver.page_source
    bsObj = BeautifulSoup(pageString, 'lxml')

    for link1 in bsObj.find_all(name='div', attrs={"class":"Nnq7C weEfm"}):
        title = link1.select('a')[0]
        real = title.attrs['href']
        reallink.append(real)
        title = link1.select('a')[1]
        real = title.attrs['href']
        reallink.append(real)
        title = link1.select('a')[2]
        real = title.attrs['href']
        reallink.append(real)

    last_scroll = driver.execute_script('return document.body.scrollHeight')
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(SCROLL_DOWN_TIME)
    new_scroll = driver.execute_script("return document.body.scrollHeight")

    if new_scroll == last_scroll:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_DOWN_TIME)
        new_scroll = driver.execute_script("return document.body.scrollHeight")

        # 현재 게시물이 마지막 게시물일 때 break
        if new_scroll == last_scroll:
            break
        else:
            last_scroll = new_scroll
            continue

    time.sleep(2)

total_tag_data = len(reallink) # 전체 태그 데이터의 크기 저장

print('{0}개의 태그를 수집합니다.'.format(total_tag_data))
csvtext = []

#==================================================================================================
# 프로그램 실시간 진행률을 알기 위한 tqdm 라이브러리 사용
for i in tqdm(range(total_tag_data)):
    csvtext.append([])
    req = Request("https://www.instagram.com/p"+reallink[i], headers={'User-Agent': 'Mozila/5.0'})

    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, 'lxml', from_encoding='utf-8')
    soup1 = soup.find('meta', attrs={'property':"og:description"})

    reallink1 = soup1['content']
    reallink1 = reallink1[reallink1.find("@") + 1:reallink1.find(")")]
    reallink1 = reallink1[:20]

    if reallink1 == '':
        reallink1 = "Null"
    csvtext[i].append(reallink1)

    for reallink2 in soup.find_all('meta', attrs={'property':"instapp:hashtags"}):
        hashtags = reallink2['content'].rstrip(',')
        csvtext[i].append(hashtags)

    time.sleep(0.5)

    import re

    text = "행복함, 즐거움, 즐겁다, 즐겁, 짜증, 행복, 행복감, 스트레스, 외로움, 고독"

    # '즐겁다'를 제외한 나머지 단어
    regex_1 = re.compile(r'\b(?!즐겁다\b)\w+')
    re_1 = regex_1.findall(text)
    print(re_1)

    # '즐겁'이라는 단어를 제외한 나머지 단어
    regex_2 = re.compile(r'\b(?:(?!즐겁)\w)+\b')
    re_2 = regex_2.findall(text)
    print(re_2)

    # '행복'이라는 단어를 제외한 나머지 단어
    regex_3 = re.compile(r'\b(?:(?!행복)\w)+\b')
    re_3 = regex_3.findall(text)
    print(re_3)

    # '짜증'이라는 단어를 제외한 나머지 단어
    regex_4 = re.compile(r'\b(?:(?!짜증)\w)+\b')
    re_4 = regex_4.findall(text)
    print(re_4)

    # '행복감'이라는 단어를 제외한 나머지 단어
    regex_5 = re.compile(r'\b(?:(?!행복감)\w)+\b')
    re_5 = regex_5.findall(text)
    print(re_5)

    # '스트레스'이라는 단어를 제외한 나머지 단어
    regex_6 = re.compile(r'\b(?:(?!스트레스)\w)+\b')
    re_6 = regex_6.findall(text)
    print(re_6)

    # '외로움'이라는 단어를 제외한 나머지 단어
    regex_7 = re.compile(r'\b(?:(?!외로움)\w)+\b')
    re_7 = regex_7.findall(text)
    print(re_7)

    # '고독'이라는 단어를 제외한 나머지 단어
    regex_8 = re.compile(r'\b(?:(?!고독)\w)+\b')
    re_8 = regex_8.findall(text)
    print(re_8)


    # 데이터를 csv파일, txt파일로 저장
    data = pd.DataFrame(csvtext)
    data.to_csv('tagdata.csv', encoding='utf-8-sig')
    data.to_csv('tagdata.txt', encoding='utf-8')

    

#==================================================================================================

driver.close() # Chrome Driver 종료


#==================================================================================================

# https://github.com/Hinterhalter/instagram_crawling  - 참고 오픈소스 출처