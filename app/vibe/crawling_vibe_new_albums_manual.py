from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import json
from time import sleep
load_dotenv()

driver = webdriver.Chrome()
# 페이지 렌더링
driver.get('https://vibe.naver.com/new-release-album/manual')
# 7초간 로딩 대기
driver.implicitly_wait(time_to_wait=7)
# 팝업창 닫기 클릭
driver.find_element(By.CSS_SELECTOR, "#__modal-container > div > div > div > div > a._btn_close_1mry4_247").click()

while True:
    # 밑으로 스크롤
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    try:
        # 더보기 클릭
        driver.find_element(By.CSS_SELECTOR, "#content > div > div.sub_list > div.btn_more_list > a.link").click()
    except Exception as err:
        break

    sleep(0.5)


driver.implicitly_wait(time_to_wait=3)
set_directory = driver.find_elements(By.CSS_SELECTOR, "#content > div > div.sub_list > ul > li.list_item")

title_array = []
artist_array = []
save_array = []

try:
    for data in set_directory:

        title = data.find_element(By.CSS_SELECTOR, "div > div.info > a > span.text_wrap > span.text").text
        if(title):
            title_array.append(title)

        artist = data.find_element(By.CSS_SELECTOR, "div > div.info > div.artist > span.artist_sub_inner").text
        if(artist):
            artist_array.append(artist)

    for j, k in zip(title_array, artist_array):
        save_array.append({ "title" : j, "artist" : k })

    file_path = "vibe_new_album_manual.txt"
    with open(f"{os.environ.get('DOWNLOAD_PATH')}{file_path}", "w", encoding="utf-8") as file:
        file.write(json.dumps(save_array, indent=4, ensure_ascii=False))
except Exception as err:
    print(err)
    print("에러 발생")
finally:
    driver.close()