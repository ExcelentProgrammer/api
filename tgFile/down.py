from telethon.sync import TelegramClient
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

client = TelegramClient('bot', env.str("api_id"), env.str("api_hash"))
client.start(bot_token=token)

msg = client.get_messages(int(chat_id), ids=int(message_id))


def progress(down, size):
    down = round(down / (1024 * 1024), 2)
    size = round(size / (1024 * 1024), 2)

    if match(r"^(.*)\?(.*)=(.*)$", url):
        get(f"{url}&down={down}&size={size}&status=progress")
    else:
        get(f"{url}?down={down}&size={size}&status=progress")


res = client.download_media(msg, file="media/down/", progress_callback=progress)

domain = env.str("domain")
file_url = f"{domain}/{parse.quote(res)}"


if match(r"^(.*)\?(.*)=(.*)$", url):
    get(f"{url}&status=finish&url={file_url}")
else:
    get(f"{url}?status=finish&url={file_url}")
