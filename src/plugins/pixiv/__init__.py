from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11.message import Message,MessageSegment
from nonebot.adapters.onebot.v11.event import  MessageEvent
from nonebot.matcher import Matcher
from nonebot.typing import T_State
from nonebot.params import State, CommandArg, Arg, ArgPlainText
from .account import *
from .search import *
import requests,random

path = os.getcwd()

start = on_command('搜', priority=7)
login = on_command("登录", rule=to_me(),aliases={"login"}, priority=7)

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
        await start.send(f'正在搜索：{tag}')
        img = search.Main(tag)
        await start.finish(img)