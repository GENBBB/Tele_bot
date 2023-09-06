from telebot import TeleBot
from telebot.types import Message
from telebot.util import extract_arguments

Token_file = open("Token")
Token = Token_file.readline()
bot = TeleBot(Token)


@bot.message_handler(commands=['start'])
def start_cmd(message: Message):
    bot.send_message(chat_id=message.chat.id, text="Hello, poebish")


@bot.message_handler(commands=['help'])
def help_cmd(message: Message):
    bot.send_message(chat_id=message.chat.id, text="/start - Nachalo\n"
                                                   "/help - pomosh\n"
                                                   "/beer - pozvat po pivu\n"
                                                   "/cigarettes - pozvat po sizke\n"
                                                   "/vodka - pozvat po pisuliku\n")


@bot.message_handler(commands=['beer', 'cigarettes', 'vodka'])
def other_another_cmds(message: Message):
    bot.send_message(chat_id=message.chat.id, text="Go " + message.text[1:])


@bot.message_handler()
def hello_world(message: Message):
    bot.send_message(chat_id=message.chat.id, text="Est shto vipit?")


bot.infinity_polling()
