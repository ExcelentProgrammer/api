from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import json

data = open("./media/sendMessage/data.json", "r")
data = json.loads(data.read())
bot = TeleBot(data['token'])
keyboards = data['keyboard']
chat = data['chat']
msg = data['msg']
type = data['type']
parse = data['parse']
kk = None

if keyboards != "null":
    ktype = data['keyboard_type']

    if ktype == "keyboard":
        kk = ReplyKeyboardMarkup(resize_keyboard=True)
    elif ktype == "inline_keyboard":
        kk = InlineKeyboardMarkup()
    for keyboard in keyboards:
        if ktype == "keyboard":
            kk.add(KeyboardButton(keyboard['text']))
        elif ktype == "inline_keyboard":
            kk.add(InlineKeyboardButton(text=keyboard['text'], url=keyboard['url']))

if type == 1:
    for user in data['users']:
        bot.copy_message(chat_id=user, from_chat_id=chat, message_id=msg, reply_markup=kk, parse_mode=parse)
elif type == 2:
    for user in data['users']:
        bot.forward_message(chat_id=user, from_chat_id=chat, message_id=msg)
