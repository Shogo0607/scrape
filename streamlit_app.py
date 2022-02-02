import urllib.request
from urllib.parse import quote
from bs4 import BeautifulSoup
import time
import streamlit as st
import random

def get_search_html(keyword, page):
    start = "&start=" + str(page * 10) # 次ページstart=10
    url = 'https://www.google.com/search?q=' + quote(keyword) + start 
    
    headers = {'User-Agent': user_agent}
    req = urllib.request.Request(url, headers=headers)

    with urllib.request.urlopen(req) as res:
        body = res.read()
        return body


def get_page_rank(soup, page):
    res_rank = 1

    for a_tag in soup.find_all('a'):
        h3_tag = a_tag.select("h3")

        if len(h3_tag) > 0:
            if a_tag.get('href').startswith(target) == True:
                return res_rank + page * 10

            res_rank += 1
    return -1

keyword = st.sidebar.text_input('検索ワード')
if keyword == "":
    st.sidebar.warning("検索ワードを入力してください")
    st.stop()
st.sidebar.write("検索ワードは",keyword,"です。")

# 上位から何件までのサイトを抽出するか指定する
pages_num = st.sidebar.number_input("検索件数を入力してください",value=100)
if pages_num == "" or pages_num == 0:
    st.warning("検索件数を入力してください")
    st.stop()
st.sidebar.write("検索件数は",pages_num,"です")


pages_num = int(pages_num/10)

target = st.sidebar.text_input('検索URL')
if target == "":
    st.sidebar.warning("検索URLを入力してください")
    st.stop()

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
rank = -1
max_page = pages_num

if st.sidebar.button("検索"):
    with st.spinner("現在検索中です。少々お待ちください"):
        for page in range(max_page):
            html = get_search_html(keyword, page)
            soup = BeautifulSoup(html, 'html.parser')

            title_text = soup.find('title').get_text()
            rank = get_page_rank(soup, page)

            page += 1
            if rank != -1:
                break
            rand = random.randint(3, 7)
            time.sleep(rand)
            
        if rank != -1:
            st.write("順位: {}位".format(rank))
        else:
            st.write("見つかりませんでした")
