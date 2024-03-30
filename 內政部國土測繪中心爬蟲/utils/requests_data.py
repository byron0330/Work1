from bs4 import BeautifulSoup

import requests

headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'}
def get_soup(url): ##讀取網頁函式
    r = requests.get(url, headers=headers)
    soup = r.json()
    return (soup)