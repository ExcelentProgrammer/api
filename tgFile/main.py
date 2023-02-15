import asyncio

from telethon.errors import FileIdInvalidError
from telethon.sync import TelegramClient, utils

# Your API ID and hash can be obtained from https://my.telegram.org/apps
api_id = 7878494
api_hash = '3b7035773fde7b903fa430a6f1540e32'

# Create a client instance
client = TelegramClient('bot', api_id, api_hash)

# Connect to Telegram servers
client.start()
exit()

result = client.send_file('@azamov_samandar', 'video.mp4')

msg = client.get_messages(1769851684,ids=17547)

client.download_media(msg)

# Disconnect from Telegram servers
client.disconnect()
