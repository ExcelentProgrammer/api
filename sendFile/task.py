import asyncio
import os

import requests
from pyrogram import Client
from environs import Env

import sys
from re import match
from requests import get
import time

from celery import shared_task

from logger import logger

env = Env()
env.read_env()


@shared_task
def run(chat_id, caption, fileType, token: str, url: str, callback_url: str):

    global start_time

    ex = url.split(".")[-1]
    if url.startswith("https://api.iprogrammer.uz"):
        file_name = url.replace("https://api.iprogrammer.uz/", "")
        logger.info(f"File Already: {file_name}")
    else:
        file_name = f"media/sendFile/{time.time() * 1000}.{ex}"
        try:
            with open(file_name, "wb") as f:
                print("Downloading %s" % url)
                response = requests.get(url, stream=True)
                total_length = response.headers.get('content-length')
                d1 = ''
                d2 = ''
                if total_length is None:  # no content length header
                    f.write(response.content)
                else:
                    dl = 0
                    total_length = int(total_length)
                    start_time = round(time.time())
                    for data in response.iter_content(chunk_size=4096):
                        f.write(data)
                        dl += len(data)
                        now_time = round(time.time())
                        if (now_time - 3) >= start_time:

                            start_time = now_time

                            d1 = round(dl / (1024 * 1024), 2)
                            d2 = round(total_length / (1024 * 1024), 2)

                            try:
                                done = int(50 * int(d1) / int(d2))
                            except:
                                done = 1
                            sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
                            sys.stdout.flush()

                            if match(r"^(.*)\?(.*)=(.*)$", callback_url):
                                get(f"{callback_url}&down={d1}&size={d2}&status=downloading")
                            else:
                                get(f"{callback_url}?down={d1}&size={d2}&status=downloading")
                    get(f"{callback_url}?down={d1}&size={d2}&status=downloaded")
            print(f"\n\nDownloaded {url}")
            logger.info(f"Downloaded: {url}")
        except:
            print(f"\n\nDownload Error {url}")
            logger.error(f"Download Error: {url}")

    start_time = round(time.time())-3

    def progress(down, size):
        
        global start_time

        now_time = round(time.time())

        if (now_time - 3) > start_time:
            start_time = now_time
            down = round(down / (1024 * 1024), 2)
            size = round(size / (1024 * 1024), 2)
            try:
                done = int(50 * int(down) / int(size))
            except:
                done = 1
            sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50 - done)))
            sys.stdout.flush()
            if match(r"^(.*)\?(.*)=(.*)$", callback_url):
                get(f"{callback_url}&send={down}&size={size}&status=sending")
            else:
                get(f"{callback_url}?send={down}&size={size}&status=sending")

    async def main(file):
        async with Client("bot", api_id=env.int("api_id"), api_hash=env.str("api_hash"), bot_token=token) as app:
            # Send a message, Markdown is enabled by default
            if fileType == "video":
                res = await app.send_video(chat_id=chat_id, caption=caption, video=file, progress=progress)
            elif fileType == "audio":
                res = await app.send_audio(chat_id=chat_id, caption=caption, audio=file, progress=progress)
            elif fileType == "document":
                res = await app.send_document(chat_id=chat_id, caption=caption, document=file, progress=progress)
            elif fileType == "photo":
                res = await app.send_photo(chat_id=chat_id, caption=caption, photo=file, progress=progress)
            else:
                return []
            return res

    loop = asyncio.get_event_loop()

    f = ""
    try:
        loop.run_until_complete(main(file=file_name))
        print(f"\n\nSend Success {chat_id}")
        logger.info(f"Send File Success: {chat_id}")
        f = "finish"
    except:
        logger.error(f"Send File Error: {chat_id}")
        f = "error"

    os.remove(file_name)

    if match(r"^(.*)\?(.*)=(.*)$", callback_url):
        get(f"{callback_url}&status={f}")
    else:
        get(f"{callback_url}?status={f}")
