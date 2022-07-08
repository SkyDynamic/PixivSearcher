import json
from turtle import end_fill
import requests
import os
import random
from nonebot.adapters.onebot.v11.message import MessageSegment,Message

from .pixiv_site.get_header import *

class Main():
    def __new__(self, key):
        self.get_token(self)
        self.search(self, key)
        msg = self.download_img(self)
        return msg

    def get_token(self):
        with open('src/plugins/pixiv/token.json', 'r', encoding='utf-8') as f:
            self.token = json.load(f)

    def search(self, key):
        headers = get_simple_header()
        headers['authorization'] = self.token
        url = f'https://pix.ipv4.host/illustrations?keyword={key}&page=1&pageSize=10&searchType=original&illustType=illust&minWidth=1280&minHeight=720&xRestrict=0'
        res_json = requests.get(url, headers=headers).json()
        self.data_json = res_json.get("data")

    def download_img(self) -> str:
        num = random.randint(1,8)
        if self.data_json != 'None':
            id = self.data_json[num]['id']
            title = self.data_json[num]['title']
            author = self.data_json[num]['artistPreView']['account']
            url = f'https://pixiv.re/{id}.png'
            imgmsg = Message(f'ID：{id}\n标题：{title}\n作者：{author}\n')
            img = MessageSegment.image(url)
            msg = imgmsg + img
            return msg
        elif self.data_json == 'None':
            return '什么也没找到呢~'
           
