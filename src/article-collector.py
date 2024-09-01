# -*- coding: utf-8 -*-
"""
  @Description
  @Author Chris
  @Date 2024/9/1
"""
import os
import random
import time
from json import JSONDecodeError

import requests

from src.constant import COOKIE, TOKEN, DATA_PATH, OFFICIAL_ACCOUNT_FILE_PATH, ARTICLE_PATH
from src.util import load_json, read_txt, read_json, write_csv, read_csv

total_count = 0
page_size = 24


def search_account_all_article(fakeid: str):
    articles = []
    begin = 0
    while True:
        result = search_account_article_page(fakeid, begin)
        if not result:
            break
        articles.extend(result)
        begin += page_size
        if len(articles) >= total_count:
            break
        time.sleep(random.randint(1, 30))
    return articles


def search_account_article_page(fakeid: str, begin: int = 0):
    url = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish"
    headers = {
        "Cookie": COOKIE,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.901.400 QQBrowser/9.0.2524.400"
    }
    count = page_size
    params = {
        "sub": "list",
        "search_field": "null",
        "begin": begin,
        "count": count,
        "query": "",
        "fakeid": fakeid,
        "type": "101_1",
        "free_publish_type": 1,
        "sub_action": "list_ex",
        "token": TOKEN,
        "lang": "zh_CN",
        "f": "json",
        "ajax": 1
    }
    response = requests.get(url, headers=headers, params=params).json()
    if response["base_resp"]["ret"] != 0:
        print(response)
        return None
    try:
        publish_page = load_json(response["publish_page"])
    except JSONDecodeError as e:
        print(e)
        return
    articles = extract_article(publish_page)

    return articles


def extract_article(content: dict):
    global total_count
    total_count = content["total_count"]
    articles = []
    for publish in content["publish_list"]:
        try:
            tmp = load_json(publish["publish_info"])
        except JSONDecodeError as e:
            print(e)
            continue
        for article in tmp["appmsgex"]:
            created_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(article["create_time"]))
            articles.append([article["title"], article["link"], created_time])
    return articles


def output(account, articles):
    rows = [["account", "title", "link", "created_time"]]
    for article in articles:
        rows.append([account, article[0], article[1], article[2]])
    file_path = ARTICLE_PATH + account + ".csv"
    write_csv(file_path, rows)


def collected():
    paths = os.listdir(ARTICLE_PATH)
    return set(path.replace(".csv", "") for path in paths)


if __name__ == '__main__':
    rows = read_csv(OFFICIAL_ACCOUNT_FILE_PATH, encoding="gbk")
    rows = rows[1:]
    for row in rows:
        account = row[0]
        # Check if the account has been collected
        if account in collected():
            continue
        fakeid = row[1]
        # Check if the account has no fakeid
        if fakeid == "" or fakeid is None:
            continue
        print(account)
        articles = search_account_all_article(fakeid)
        # # Check if the account has no articles
        # if len(articles) == 0:
        #     continue
        output(account, articles)
        time.sleep(random.randint(1, 30))
