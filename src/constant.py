# -*- coding: utf-8 -*-
"""
  @Description
  @Author Chris
  @Date 2024/9/1
"""

import os

from dotenv import load_dotenv

load_dotenv()
ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + "/"
DATA_PATH = ROOT_PATH + "data/"
RES_PATH = ROOT_PATH + "res/"
COOKIE = os.environ.get("COOKIE")
TOKEN = os.environ.get("TOKEN")

ACCOUNT_NAME_PREFIX_FILE_PATH = DATA_PATH + "AccountNamePrefix.txt"
OFFICIAL_ACCOUNT_FILE_PATH = RES_PATH + "OfficialAccount.csv"
ARTICLE_PATH = RES_PATH + "article/"
