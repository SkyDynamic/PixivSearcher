import random
import requests
import asyncio

from nonebot import on_command
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.matcher import Matcher
from nonebot.params import Arg, ArgPlainText, CommandArg, State
from nonebot.rule import to_me
from nonebot.typing import T_State

from .account import *
from .search import *

path = os.getcwd()

start = on_command('搜', priority=7)
login = on_command("登录", rule=to_me(),aliases={"login"}, priority=7)
rank = on_command("rank", priority=7)

@login.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    global verifi
    verifi = account.GetVervfi()
    await login.send(MessageSegment.image(f'file:///{path}/src/plugins/pixiv/tmp.png'))
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("_login", args)

@login.got("_login", prompt = "请输入下图验证码")
async def handle_login(_login: Message = Arg(), login_msg: str = ArgPlainText("_login")):
    with open("src/plugins/pixiv/account.json") as f:
        account_data = json.load(f)
    account_choose = json.dumps(account_data)
    url1 = f"https://pix.ipv4.host/users/token?vid={verifi}&value={login_msg}"
    account_msg = requests.post(url1, data=account_choose, headers=get_login_header())
    accountjson = account_msg.json()['message']
    if 'authorization' in account_msg.headers:
        token = account_msg.headers['authorization']
    if accountjson == '登录成功':
        with open('src/plugins/pixiv/token.json', "w", encoding="utf-8") as fi:
            json.dump(token, fi, ensure_ascii=False, indent=4)
        os.remove('src/plugins/pixiv/tmp.png')
    if accountjson == '验证码错误':
        os.remove('src/plugins/pixiv/tmp.png')
    await login.finish(accountjson)

@start.handle()
async def _(event: MessageEvent, arg: Message = CommandArg()):
    arg1 = str(arg).split(' ')
    tag = arg1[0]
    if tag == '':
        await start.send('你的关键词呢？')
    else:
        if len(arg1) == 1:
            await start.send(f'正在搜索：{tag}')
            data_json = search.Main(tag, 'False')
            if data_json != None and data_json != 'Not Token':
                await __(data_json, 'False')
            elif data_json == None:
                __msg = '什么也没找到呢~'
                await start.send(__msg)
            elif data_json == 'Not Token':
                ___msg = '未设置Token，请私聊机器人并修改account.json进行登录哦~'
                await start.send(___msg)
        if len(arg1) == 2:
            if arg1[0] == 'R':
                data_json = search.Main(tag, 'True')
                if data_json != None and data_json != 'Not Token':
                    await __(data_json, 'True')
                elif data_json == None:
                    __msg = '什么也没找到呢~'
                    await start.send(__msg)
                elif data_json == 'Not Token':
                    ___msg = '未设置Token，请私聊机器人并修改account.json进行登录哦~'
                    await start.send(___msg)

@rank.handle()
async def rank_(event: MessageEvent, arg: Message = CommandArg()):
    arg1 = str(arg).split(' ')
    tag = arg1[0]
    if tag == '':
        await rank.send('您未输入查询哪个榜，默认搜索日榜')
        data_json = search.Rank('day')
    elif tag == 'day':
        await rank.send('正在查询今日日榜，请稍后')
        data_json = search.Rank('day')
    elif tag == 'week':
        await rank.send('正在查询今日周榜，请稍后')
        data_json = search.Rank('week')
    elif tag == 'month':
        await rank.send('正在查询今日月榜，请稍后')
        data_json = search.Rank('month')
    if data_json != None:
            await _rank_(data_json)
    elif data_json == None:
        __msg = '什么也没找到呢~'
        await start.send(__msg)

async def __(data_json, R18):
    num = random.randint(1,20)
    tasks = []
    for i in range(3):
        msg = DownLoadImg(data_json, num, R18)
        num = num + 1
        tasks.append(send_img(msg))
    await asyncio.gather(*tasks)

async def _rank_(data_json):
    tasks = []
    for i in range(3):
        msg = DownLoadImg(data_json, i, "False")
        tasks.append(send_img(msg))
    await asyncio.gather(*tasks)        

async def send_img(msg):
    await start.send(msg)

def DownLoadImg(data_json, num, R18):
    try:
        id = data_json[num]['id']
        title = data_json[num]['title']
        author = data_json[num]['artistPreView']['account']
        url = f'https://pixiv.re/{id}.png'
        imgmsg = Message(f'ID：{id}\n标题：{title}\n作者：{author}\n')
        if R18 == 'False':
            img = MessageSegment.image(url)
        if R18 == 'True':
            img = url + '\n这个图是R18哦~自行下载来观赏哦，机器人就不发出来了，上面是链接'
        msg = imgmsg + img
        return msg
    except IndexError as e:
        num = num - 10
        id = data_json[num]['id']
        title = data_json[num]['title']
        author = data_json[num]['artistPreView']['account']
        url = f'https://pixiv.re/{id}.png'
        imgmsg = Message(f'ID：{id}\n标题：{title}\n作者：{author}\n')
        if R18 == 'False':
            img = MessageSegment.image(url)
        if R18 == 'True':
            img = url + '\n这个图是R18哦~自行下载来观赏哦，机器人就不发出来了，上面是链接'
        msg = imgmsg + img
        return msg