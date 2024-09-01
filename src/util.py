# -*- coding: utf-8 -*-
"""
  @Description
  @Author Chris
  @Date 2024/9/1
"""
import csv
import json


def read_txt(file_path: str) -> list:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.readlines()


def write_csv(file_path: str, rows: list):
    with open(file_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def read_csv(file_path: str, encoding="utf-8") -> list:
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        return list(reader)


def read_json(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_json(content: str):
    return json.loads(content)
