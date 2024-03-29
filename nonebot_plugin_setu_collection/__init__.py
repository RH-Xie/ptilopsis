from nonebot.plugin.on import on_regex,on_command
from nonebot.rule import to_me
from nonebot.adapters.red import (
    Bot,
    MessageEvent,
    GroupMessageEvent,
    PrivateMessageEvent,
    MessageSegment,
    Message,
    )
from nonebot.adapters.red.message import ForwardNode
from nonebot.params import CommandArg,Arg

import nonebot
import re
import httpx
import asyncio
import unicodedata
from typing import List

from .api.MirlKoi import MirlKoi,is_MirlKoi_tag
from .api.Anosu import Anosu
from .api.Lolicon import Lolicon

Bot_NICKNAME = list(nonebot.get_driver().config.nickname)

Bot_NICKNAME = Bot_NICKNAME[0] if Bot_NICKNAME else "色图bot"

hello = on_command("色图", aliases = {"涩图"}, rule = to_me(), priority = 50, block = True)

@hello.handle()
async def _(bot: Bot, event: MessageEvent):
    msg = (
        "发送【我要一张xx涩图】可获得一张随机色图。"
        "群聊图片取自：\n"
        "Jitsu：https://image.anosu.top/\n"
        "MirlKoi API：https://iw233.cn/\n"
        "私聊图片取自：\n"
        "Lolicon API：https://api.lolicon.app/"
        )
    await hello.finish(msg)

async def func(client,url):
    resp = await client.get(url,headers={'Referer':'http://www.weibo.com/',})
    if resp.status_code == 200:
        return resp.content
    else:
        return None

setu = on_regex("^(我?要|来).*[张份].+$", priority = 50, block = True)

@setu.handle()
async def _(bot: Bot, event: MessageEvent):
    msg = ""
    cmd = event.get_plaintext()
    N = re.sub(r'^我?要|^来|[张份].+$', '', cmd)
    N = N if N else 1

    try:
        N = int(N)
    except ValueError:
        try:
            N = int(unicodedata.numeric(N))
        except (TypeError, ValueError):
            N = 0
    if(N > 5):
        await bot.send(event, "单次最多只能5张哦")
        return;
    Tag = re.sub(r'^我?要|^来|.*[张份]', '', cmd)
    Tag = Tag [:-2]if (Tag.endswith("涩图") or Tag.endswith("色图")) else Tag

    if Tag.startswith("r18"):
        Tag = Tag [3:]
        R18 = 1
    else:
        R18 = 0

    if isinstance(event,GroupMessageEvent):
        if R18:
            await bot.send(event, "涩涩是禁止事项！！")
        else:
            api = "Lolicon API"
            setufunc = Lolicon
            # if not Tag or is_MirlKoi_tag(Tag):
            #     api = "MirlKoi API"
            #     setufunc = MirlKoi
            # else:
            #     api = "Jitsu"
            #     setufunc = Anosu
    else:
        api = customer_api.get(str(event.user_id),None)
        if api == "Lolicon API":
            setufunc = Lolicon
        else:
            if not R18 or not Tag or is_MirlKoi_tag(Tag):
                api = "MirlKoi API"
                setufunc = MirlKoi
            else:
                api = "Jitsu"
                setufunc = Anosu

    msg,url_list = await setufunc(N,Tag,R18)
    msg = msg.replace("Bot_NICKNAME",Bot_NICKNAME)

    # if len(url_list) >3:
    #     msg = msg[:-1]
    #     await setu.send(msg, at_sender = True)

    async with httpx.AsyncClient() as client:
        task_list = []
        for url in url_list:
            task = asyncio.create_task(func(client,url))
            task_list.append(task)
        image_list = await asyncio.gather(*task_list)

    image_list = [image for image in image_list if image]
    if not image_list:
        await bot.send(event, msg + "获取图片失败。")
    N = len(image_list)
    # if N <= 3:
    for i in range(N):
        await bot.send(event, MessageSegment.image(file = image_list[i]))
            # image +=  MessageSegment.image(file = image_list[i])
        # await bot.send(event, Message(msg) + image)
    # else:
        # msg_list: List[ForwardNode] =[]
        # for i in range(N):
        #     msg_list.append(
        #         # {
        #         #     "type": "node",
        #         #     "data": {
        #         #         "name": Bot_NICKNAME,
        #         #         "uin": event.senderUin,
        #         #         "content": MessageSegment.image(file = image_list[i])
        #         #     }
        #         # }
        #         ForwardNode(
        #             uin=event.senderUin,
        #             name="0x0000001f",
        #             message=MessageSegment.image(file = image_list[i])
        #         )
        #     )
        # if isinstance(event,GroupMessageEvent):
        #     await bot.send_group_forward(group = event.group_id, nodes= msg_list)
        # else:
        #     await bot.send_fake_forward(target = event.get_user_id(), nodes= msg_list)

import os
from pathlib import Path

try:
    import ujson as json
except ModuleNotFoundError:
    import json

path = Path() / "data" / "setu"
file = path / "customer_api.json"
if file.exists():
    with open(file, "r", encoding="utf8") as f:
        customer_api = json.load(f)
else:
    customer_api = {}
    if not path.exists():
        os.makedirs(path)

set_api = on_command("设置api", aliases = {"切换api","指定api"}, priority = 50, block = True)

@set_api.got(
    "api",
    prompt = (
        "请选择:\n"
        "1.Jitsu/MirlKoi API\n"
        "2.Lolicon API"
        )
    )
async def _(bot: Bot, event: PrivateMessageEvent, api: Message = Arg()):
    api = str(api)
    user_id = str(event.user_id)
    def save():
        with open(file, "w", encoding="utf8") as f:
            json.dump(customer_api, f, ensure_ascii=False, indent=4)
    if api == "1":
        customer_api[user_id] = "Jitsu/MirlKoi API"
        save()
        await bot.send(event, "api已切换为Jitsu/MirlKoi API")
    elif api == "2":
        customer_api[user_id] = "Lolicon API"
        save()
        await bot.send(event, "api已切换为Lolicon API")
    else:
        await bot.send(event, "api设置失败")

