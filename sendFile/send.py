import asyncio
import os

import requests
from pyrogram import Client
from environs import Env
from sys import argv
from os import remove
from re import match
from requests import get
from urllib import parse
import json
import time

env = Env()
env.read_env()

data = json.loads(open("./media/sendFile/data.json", "r").read())

chat_id = data['chat_id']
caption = data['caption']
fileType = data['fileType']
token = data['token']
url = str(data['url'])
callback_url = str(data['callback_url'])

ex = url.split(".")[-1]

file_name = f"media/sendFile/{time.time() * 1000}.{ex}"

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

                if match(r"^(.*)\?(.*)=(.*)$", callback_url):
                    get(f"{callback_url}&down={d1}&size={d2}&status=downloading")
                else:
                    get(f"{callback_url}?down={d1}&size={d2}&status=downloading")
        get(f"{callback_url}?down={d1}&size={d2}&status=downloaded")


def progress(down, size):
    down = round(down / (1024 * 1024), 2)
    size = round(size / (1024 * 1024), 2)
    print(down,size)

    if match(r"^(.*)\?(.*)=(.*)$", url):
        get(f"{url}&send={down}&size={size}&status=progress")
    else:
        get(f"{url}?send={down}&size={size}&status=progress")


async def main(file):
    async with Client("bot", api_id=env.int("api_id"), api_hash=env.str("api_hash"), bot_token=token) as app:
        # Send a message, Markdown is enabled by default

        if fileType == "video":
            res = await app.send_video(chat_id=chat_id, caption=caption, video=file,progress=progress)
        elif fileType == "audio":
            res = await app.send_audio(chat_id=chat_id, caption=caption, audio=file,progress=progress)
        elif fileType == "document":
            res = await app.send_document(chat_id=chat_id, caption=caption, document=file,progress=progress)
        elif fileType == "photo":
            res = await app.send_photo(chat_id=chat_id, caption=caption, photo=file,progress=progress)
        else:
            return []
        return res


loop = asyncio.get_event_loop()

loop.run_until_complete(main(file=open(file_name,"rb")))

# os.remove(file_name)

if match(r"^(.*)\?(.*)=(.*)$", callback_url):
    get(f"{url}&status=finish")
else:
    get(f"{url}?status=finish")
