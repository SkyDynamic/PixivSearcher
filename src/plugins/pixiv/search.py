import json
import requests
import os
import datetime
import random

from .pixiv_site.get_header import *

class Main():
    def __new__(self, key, R18):
        self.R18 = R18
        self.get_token(self)
        self.search(self, key)
        return self.data_json

    def get_token(self):
        if os.path.exists('src/plugins/pixiv/token.json') == True:
            with open('src/plugins/pixiv/token.json', 'r', encoding='utf-8') as f:
                self.token = json.load(f)
        else:
            self.token = None

    def search(self, key):
        if self.token != None:
            if self.R18 == False:
                self.url = f'https://pix.ipv4.host/illustrations?keyword={key}&page=1&pageSize=16&searchType=original&illustType=illust&minWidth=1280&minHeight=720&xRestrict=0'
            elif self.R18 == True:
                self.url = f'https://pix.ipv4.host/illustrations?keyword={key}&page=1&pageSize=16&searchType=original&illustType=illust&minWidth=1280&minHeight=720&xRestrict=1'
            headers = get_simple_header()
            headers['authorization'] = self.token
            res_json = requests.get(self.url, headers=headers).json()
            self.data_json = res_json.get("data")
        else:
            self.data_json = 'Not Token'

class Rank():
    def __new__(self, rank):
        headers = get_simple_header()
        yesterday = datetime.date.today() + datetime.timedelta(-1)
        pagenum = random.randint(1,8)
        if rank == 'day':
            url = f'https://pix.ipv4.host/ranks?page={pagenum}&pageSize=15&date={yesterday}&mode=day'
        if rank == 'week':
            url = f'https://pix.ipv4.host/ranks?page={pagenum}&pageSize=15&date={yesterday}&mode=week'
        if rank == 'month':
            url = f'https://pix.ipv4.host/ranks?page={pagenum}&pageSize=15&date={yesterday}&mode=month'
        res_json = requests.get(url, headers=headers).json()
        return res_json.get("data")