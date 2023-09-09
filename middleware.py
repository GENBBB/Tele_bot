from telebot.types import Message
from telebot import TeleBot
from telebot.handler_backends import BaseMiddleware, CancelUpdate


class AntifloodMiddleware(BaseMiddleware):
    def __init__(self, bot: TeleBot, limit: float, ban_time: float, max_mess: int):
        self.bot = bot
        self.last_time = {}
        self.limit = limit
        self.ban_time = ban_time
        self.ban = False
        self.amount = {}
        self.max_mess = max_mess
        self.update_types = ['message']

    def pre_process(self, message: Message, data):
        if message.from_user.id not in self.last_time:
            self.last_time[message.from_user.id] = message.date
            self.amount[message.from_user.id] = 0
            return
        if self.amount[message.from_user.id] < self.max_mess:
            self.amount[message.from_user.id] += 1
            return
        if message.date - self.last_time[message.from_user.id] < self.limit:
            self.bot.send_message(message.chat.id, 'Время до возможности работать с ботом ' +
                                  str(self.ban_time if not self.ban else self.last_time[
                                                                             message.from_user.id] - message.date + self.ban_time))
            if self.ban:
                self.last_time[message.from_user.id] += self.ban_time
            else:
                self.ban = True
                self.last_time[message.from_user.id] = message.date + self.ban_time
            return CancelUpdate()
        self.ban = False
        self.last_time[message.from_user.id] = message.date
        self.amount[message.from_user.id] = 0

    def post_process(self, message, data, exception):
        pass


class UserMiddleware(BaseMiddleware):
    def __init__(self, bot: TeleBot, user_table: set):
        self.bot = bot
        self.user_table = user_table
        self.update_types = ['message']

    def pre_process(self, message: Message, data):
        if not message.from_user.id in self.user_table:
            self.user_table.add(message.from_user.id)

    def post_process(self, message, data, exception):
        pass
