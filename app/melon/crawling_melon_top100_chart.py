import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
import json
load_dotenv()

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.melon.com/chart/',headers=headers)
 
soup = BeautifulSoup(data.text, 'html.parser')

setTop_50 = soup.select("#lst50")
setTop_100 = soup.select("#lst100")

rank_array = []
title_array = []
artist_array = []
save_array = []

try:
    for data in setTop_50 :
        rank = data.select_one("td:nth-child(2) > div.wrap.t_center > span.rank").text
        if(rank):
            rank_array.append(rank)

        title = data.select_one("td:nth-child(6) > div.wrap > div.wrap_song_info > div.ellipsis.rank01 > span > a").text
        if(title):
            title_array.append(title)

        artist = data.select("td:nth-child(6) > div.wrap > div.wrap_song_info > div.ellipsis.rank02 > a")
        if(len(artist) > 1):
            artist_array.append([i.text for i in artist])
        else :
            for i in artist:
                artist_array.append(i.text)

    for data in setTop_100:
        rank = data.select_one("td:nth-child(2) > div.wrap.t_center > span.rank")
        if(rank):
            rank_array.append(rank.text)

        title = data.select_one("td:nth-child(6) > div.wrap > div.wrap_song_info > div.ellipsis.rank01 > span > a")
        if(title):
            title_array.append(title.text)

        artist = data.select("td:nth-child(6) > div.wrap > div.wrap_song_info > div.ellipsis.rank02 > a")
        if(len(artist) > 1):
            artist_array.append([i.text for i in artist])
        else :
            for i in artist:
                artist_array.append(i.text)

    for j, k, n in zip(rank_array, title_array, artist_array):
        save_array.append({ "rank" : j, "title" : k, "artist" : n })

    file_path = "melon_top100_chart_100.txt"
    with open(f"{os.environ.get('DOWNLOAD_PATH')}{file_path}", "w", encoding="utf-8") as file:
        file.write(json.dumps(save_array, indent=4, ensure_ascii=False))
except Exception as err:
    print(err)
    print("에러 발생")


        



