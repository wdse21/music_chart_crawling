from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import json
load_dotenv()

driver = webdriver.Chrome()
# 페이지 렌더링
driver.get('https://vibe.naver.com/chart/domestic')
# 7초간 로딩 대기
driver.implicitly_wait(time_to_wait=7)
# 팝업창 닫기 클릭
driver.find_element(By.CSS_SELECTOR, "#__modal-container > div > div > div > div > a._btn_close_1mry4_247").click()
# 밑으로 스크롤
driver.execute_script("window.scrollTo(0, 700)")

rank_array = []
title_array = []
artist_array = []
save_array = []

set_directory = driver.find_elements(By.CSS_SELECTOR, "#content > div.track_section > div:nth-child(2) > div > table > tbody > tr")

try :
    for data in set_directory:
        rank = data.find_element(By.CSS_SELECTOR, "td.rank > span.text").text
        if(rank):
            rank_array.append(rank)

        title = data.find_element(By.CSS_SELECTOR, "td.song > div.title_badge_wrap > span.inner_cell > a").text
        if(title):
            title_array.append(title)
    
        artist = data.find_element(By.CSS_SELECTOR, "td.song > div.artist_sub > span.artist_sub_inner").text
        if(artist):
            artist_array.append(artist)
        
    for j, k, n in zip(rank_array, title_array, artist_array):
        save_array.append({ "rank" : j, "title" : k, "artist" : n })

    file_path = "vibe_soaring_domestic_chart_100.txt"
    with open(f"{os.environ.get('DOWNLOAD_PATH')}{file_path}", "w", encoding="utf-8") as file:
        file.write(json.dumps(save_array, indent=4, ensure_ascii=False))
except Exception as err:
    print(err)
    print("에러 발생")
finally:
    driver.close()