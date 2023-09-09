from telebot.types import Message
from telebot import TeleBot
from states import DrunkStates


def register_handlers(bot: TeleBot):
    bot.register_message_handler(callback=start_cmd, commands=['start'], pass_bot=True)
    bot.register_message_handler(callback=help_cmd, commands=['help'], pass_bot=True)
    bot.register_message_handler(callback=drunk0_cmd, commands=['go_drunk'], pass_bot=True)


def start_cmd(message: Message, bot: TeleBot):
    bot.send_message(chat_id=message.chat.id, text="Привет, я робот собутыльник! Нажми /help и узнай, что я могу.")


def help_cmd(message: Message, bot: TeleBot):
    bot.send_message(chat_id=message.chat.id, text="/help - вывод всех команд.\n"
                                                   "/go_drunk - начать попойку")


def drunk0_cmd(message: Message, bot: TeleBot):
    bot.set_state(user_id=message.from_user.id, state=DrunkStates.state_1, chat_id=message.chat.id)
    bot.send_message(chat_id=message.chat.id, text="Что будем пить? "
                                                   "Водку или водку?")
