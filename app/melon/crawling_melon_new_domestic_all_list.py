from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
import os
import json
from time import sleep
load_dotenv()

mobile_emulation = { "deviceName": "iPhone X" }
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.melon.com/new/index.htm")
driver.implicitly_wait(time_to_wait=7)

title_array = []
artist_array = []
release_date_array = []
save_array = []

# 팝업창 닫기
driver.find_element(By.CSS_SELECTOR, "body > div.melon-container.melon-container-fixed.melon-onboarding > main > div > a.btn-close").click()
sleep(1)

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    try:
        driver.find_element(By.CSS_SELECTOR, "#moreBtn").click()
    except Exception:
        break
    sleep(0.5)

set_directory = driver.find_elements(By.CSS_SELECTOR, "#_mList > li.list_item")
sleep(1)

try:
    for data in set_directory:
        title = data.find_element(By.CSS_SELECTOR, "div.content > div.inner > a > p.title.ellipsis.line_clamp2").text
        if(title):
            title_array.append(title)

        artist = data.find_element(By.CSS_SELECTOR, "div.content > div.inner > a > span.name.ellipsis").text
        if(artist):
            artist_array.append(artist)

        release_date = data.find_element(By.CSS_SELECTOR, "div.content > div.inner > a > div.bottom > span.date").text
        if(release_date):
            release_date_array.append(release_date)

        for j, k, n in zip(title_array, artist_array, release_date_array):
            save_array.append({ "title" : j, "artist" : k, "release_date" : n })

        file_path = "melon_new_domestic_all_list.txt"
        with open(f"{os.environ.get('DOWNLOAD_PATH')}{file_path}", "w", encoding="utf-8") as file:
            file.write(json.dumps(save_array, indent=4, ensure_ascii=False))
except Exception as err:
    print(err)
    print("에러 발생")
finally:
    driver.close()
    

