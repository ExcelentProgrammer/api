import asyncio
import time

from pyrogram import Client
from environs import Env
from re import match
from requests import get
from urllib import parse

from celery import shared_task

from logger import logger

env = Env()
env.read_env()


@shared_task
def run(token, chat_id, message_id, url):
    global start_time

    start_time = round(time.time())

    def progress(down, size):
        global start_time
        now_time = round(time.time())-3

        if (now_time - 3) > start_time:
            start_time = now_time
            print(start_time,now_time)
            down = round(down / (1024 * 1024), 2)
            size = round(size / (1024 * 1024), 2)
            if match(r"^(.*)\?(.*)=(.*)$", url):
                get(f"{url}&down={down}&size={size}&status=progress")
            else:
                get(f"{url}?down={down}&size={size}&status=progress")

    async def main(chat_id, message_id):
        async with Client("bot", api_id=env.int("api_id"), api_hash=env.str("api_hash"), bot_token=token) as app:
            # Send a message, Markdown is enabled by default
            try:
                message = await app.get_messages(chat_id=int(chat_id), message_ids=int(message_id))
                res = await app.download_media(message, file_name=f"./../../media/down/", progress=progress)
                res = res.split("/")[-1]
                logger.info(f"Downloaded: {message_id} {res}")
                return res
            except Exception as e:
                logger.error(e)
                logger.error(f"Download Error: {message_id}")
                return ""

    loop = asyncio.get_event_loop()
    res = loop.run_until_complete(main(chat_id, message_id))

    domain = env.str("domain")

    file_url = f"{domain}/media/down/{parse.quote(res)}"

    if match(r"^(.*)\?(.*)=(.*)$", url):
        get(f"{url}&status=finish&url={file_url}")
    else:
        get(f"{url}?status=finish&url={file_url}")
