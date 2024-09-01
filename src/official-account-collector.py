# -*- coding: utf-8 -*-
"""
  @Description
  @Author Chris
  @Date 2024/9/1
"""
import time

import requests

from constant import TOKEN, COOKIE, DATA_PATH, OFFICIAL_ACCOUNT_FILE_PATH, ACCOUNT_NAME_PREFIX_FILE_PATH
from util import read_txt, write_csv


def search_official_account_item(name: str):
    url = "https://mp.weixin.qq.com/cgi-bin/searchbiz"
    headers = {
        "Cookie": COOKIE,
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.901.400 QQBrowser/9.0.2524.400"
    }
    begin = 0
    count = 1
    params = {
        "action": "search_biz",
        "begin": begin,
        "count": count,
        "token": TOKEN,
        "lang": "zh_CN",
        "f": "json",
        "ajax": 1
    }
    params["query"] = name
    response = requests.get(url, headers=headers, params=params).json()
    if response["base_resp"]["ret"] != 0:
        return None
    if response["list"][0]["nickname"] != name:
        return None
    return response["list"][0]["fakeid"]


def search_all_official_account():
    name_prefix_list = read_txt(ACCOUNT_NAME_PREFIX_FILE_PATH)
    accounts = []
    for name_prefix in name_prefix_list:
        name = name_prefix.strip() + "社会工作"
        fakeid = search_official_account_item(name)
        if fakeid is None:
            fakeid = ""
        accounts.append([name, fakeid])
        print(name, fakeid)
        time.sleep(1)
    return accounts


if __name__ == '__main__':
    accounts = search_all_official_account()
    write_csv(OFFICIAL_ACCOUNT_FILE_PATH, accounts)
    pass
