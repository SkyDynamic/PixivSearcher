![](https://img.shields.io/badge/Python-%3E%3D3.7-blue) ![](https://img.shields.io/badge/Nonebot2-%3E%3D2.0.0b4-pink)
# PixivSearcher
一个用来搜涩图的好东西  

# 如何使用
先修改`/src/plugins/pixiv/account.json`文件  
`{
  "username": "你的pixivic用户名",
  "password": "你的pixivic用户密码"
}`
如果没有账号请先去pixivic.com去注册

# 指令：
## 私聊
修改完`account.json`后私聊对机器人输入`/登录`或`/login`指令，然后输入发送的图片中的验证码即可登录

## 群聊
`/rank <Value>`Value可选值：`day` `week` `month`  
`/搜 <标签关键词>`搜索相关标签图片（不要把`<>`这个符号给我写上去）(需要登录)  
`/搜 R <标签关键词>`搜索R18相关标签图片（可能会搜不到，需要登陆）  
