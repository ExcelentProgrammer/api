import asyncio

from pyrogram import Client
from environs import Env
from sys import argv
from os import remove
from re import match
from requests import get
from urllib import parse

env = Env()
env.read_env()

token = argv[1]
chat_id = argv[2]
message_id = argv[3]
url = argv[4]


# Create a new Client instance


def progress(down, size):
    down = round(down / (1024 * 1024), 2)
    size = round(size / (1024 * 1024), 2)

    if match(r"^(.*)\?(.*)=(.*)$", url):
        get(f"{url}&down={down}&size={size}&status=progress")
    else:
        get(f"{url}?down={down}&size={size}&status=progress")


async def main(chat_id, message_id):
    async with Client("bot", api_id=env.int("api_id"), api_hash=env.str("api_hash"), bot_token=token) as app:
        # Send a message, Markdown is enabled by default
        message = await app.get_messages(chat_id=int(chat_id), message_ids=int(message_id))
        res = await app.download_media(message, file_name="../media/down/", progress=progress)
        return res.split("/")[-1]


loop = asyncio.get_event_loop()
res = loop.run_until_complete(main(chat_id, message_id))

domain = env.str("domain")


file_url = f"{domain}/media/down/{parse.quote(res)}"

if match(r"^(.*)\?(.*)=(.*)$", url):
    get(f"{url}&status=finish&url={file_url}")
else:
    get(f"{url}?status=finish&url={file_url}")
