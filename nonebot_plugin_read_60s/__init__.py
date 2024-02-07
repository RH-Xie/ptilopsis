import requests
from pathlib import Path
from .config import Config
from nonebot import require, on_command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import json
import nonebot
from nonebot.adapters.red import Message, MessageEvent, MessageSegment
from nonebot.adapters.red.bot import Bot
from httpx import AsyncClient


global_config = nonebot.get_driver().config
nonebot.logger.info("global_config:{}".format(global_config))
plugin_config = Config(**global_config.dict())
nonebot.logger.info("plugin_config:{}".format(plugin_config))
scheduler = require("nonebot_plugin_apscheduler").scheduler  # type:AsyncIOScheduler

def remove_upprintable_chars(s):
    return ''.join(x for x in s if x.isprintable())#去除imageUrl可能存在的不可见字符

get_60s = on_command("今日快讯", block=True, priority=5)
@get_60s.handle()
async def hf(bot: Bot, ev: MessageEvent):
    msg = await suijitu(ev.get_user_id());
    await bot.send(ev, message=Message(msg))

async def read60s():
    msg = await suijitu()
    for qq in plugin_config.read_qq_friends:
        await nonebot.get_bot().send_private_msg(user_id=qq, message=Message(msg))

    for qq_group in plugin_config.read_qq_groups:
        await nonebot.get_bot().send_group_msg(group_id=qq_group, message=Message(msg))# MessageEvent可以使用CQ发图片



async def suijitu(user_id = ''):
    async with AsyncClient() as client:
        try:
            url = "https://api.2xb.cn/zaob"  # 备用网址
            resp = requests.get(url)
            resp = resp.text
            resp = remove_upprintable_chars(resp)
            retdata = json.loads(resp)
            imageUrl = retdata['imageUrl']
            img = await client.get(imageUrl, timeout=8000)
            msgBody = [MessageSegment.text(f"今日60S读世界已送达\n"), MessageSegment.image(img.content)]
            if(user_id != ''): msgBody.insert(0, MessageSegment.at(user_id));
            return msgBody
            
        except:
            return [MessageSegment.text("今日60S获取失败")]
            # 这个API已经挂了
            # url = "https://api.iyk0.com/60s"
            # resp = requests.get(url)
            # resp = resp.text
            # resp = remove_upprintable_chars(resp)
            # retdata = json.loads(resp)
            # lst = retdata['imageUrl']
            # return [MessageSegment.text(f"今日60S读世界已送达\n"), MessageSegment.image(Path(lst))]

for index, time in enumerate(plugin_config.read_inform_time):
    nonebot.logger.info("id:{},time:{}".format(index, time))
    scheduler.add_job(read60s, "cron", hour=time.hour, minute=time.minute, id=str(index))