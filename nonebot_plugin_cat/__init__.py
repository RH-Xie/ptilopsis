from nonebot import on_command
from nonebot.adapters.red.bot import Bot
from nonebot.adapters.red import MessageSegment
from nonebot.adapters.red.event import Event
# from utils.http_utils import AsyncHttpx
from httpx import AsyncClient
from nonebot.log import logger as logger

__zx_plugin_name__ = "随机猫猫"
__plugin_usage__ = """
usage：
随机猫猫
""".strip()
__plugin_des__ = "随机猫猫"
__plugin_type__ = ("一些工具",)
__plugin_cmd__ = ["随机猫猫"]
__plugin_version__ = 0.1
__plugin_author__ = "yajiwa & Copaan"
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": ["随机猫猫"],
}

miao = on_command("随机猫猫", block=True, priority=5)
fox = on_command("随机狐狐", block=True, priority=5)
husky = on_command("随机二哈", block=True, priority=5)


@miao.handle()
async def hf(bot: Bot, ev: Event):
    try:
        # img = await AsyncHttpx().get("http://edgecats.net/")
        async with AsyncClient() as client:
            logger.info("START")
            img = await client.get("https://edgecats.net/", timeout=8000)
            # data = resp.text.strip()
            logger.info(img.content)
    except:
        return await bot.send(event=ev, message="获取猫猫图片超时")
    await bot.send(event=ev, message=MessageSegment.image(img.content))

@fox.handle()
async def hf(bot: Bot, ev: Event):
    try:
        # img = await AsyncHttpx().get("http://edgecats.net/")
        async with AsyncClient() as client:
            resp = await client.get("https://randomfox.ca/floof/")
            json = resp.json();
            # data = resp.text.strip()
            logger.info(resp)
    except:
        return await bot.send(event=ev, message="获取狐狐图片超时")
    await bot.send(event=ev, message=MessageSegment.image(json["image"]))

@husky.handle()
async def hf(bot: Bot, ev: Event):
    try:
        # img = await AsyncHttpx().get("http://edgecats.net/")
        async with AsyncClient() as client:
            resp = await client.get("https://dog.ceo/api/breed/husky/images/random")
            json = resp.json();
            # data = resp.text.strip()
            logger.info(json)
    except:
        return await bot.send(event=ev, message="获取二哈图片超时")
    await bot.send(event=ev, message=MessageSegment.image(json["message"]))
