# 지니뮤직 1-50위 스크래핑하기!
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

client = MongoClient('localhost', port=27017)
db = client.dbsparta

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get('https://www.genie.co.kr/chart/top200?ditc=D&rtm=N&ymd=20200713 ', headers=headers)

soup = BeautifulSoup(data.text, 'html.parser')

trs = soup.select('#body-content > div.newest-list > div> table > tbody > tr')

for tr in trs:
    rank = tr.select_one('td.number')
    rank_arrange = rank.text.strip()[0:2].rstrip()

    title = tr.select_one('td.info > a.title')
    title_arrange = title.text.strip()

    artist = tr.select_one('td.info > a.artist')
    artist_arrange = artist.text

    # print(rank_arrange, title_arrange, artist_arrange)
    if rank_arrange is not None and title_arrange is not None and artist_arrange is not None:
        data = {
            'rank': rank_arrange,
            'title': title_arrange,
            'artist': artist_arrange
        }

        db.musics.insert_one(data)

#github을 위한 변화