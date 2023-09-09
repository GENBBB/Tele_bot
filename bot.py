from telebot import TeleBot
from middleware import AntifloodMiddleware, UserMiddleware
from telebot.custom_filters import StateFilter
from states import DrunkStates, MyOtherStates
from telebot.types import Message, ChatMemberUpdated
from filter import MoneyFilter
from telebot.util import update_types

Token_file = open("Token")
Token = Token_file.readline()
bot = TeleBot(Token, use_class_middlewares=True)
bot.setup_middleware(AntifloodMiddleware(bot, 3.0, 1.0, 4))
user_table = set()
ban_user_table = set()
bot.setup_middleware(UserMiddleware(bot, user_table=user_table))
bot.add_custom_filter(StateFilter(bot))
bot.add_custom_filter(MoneyFilter())


@bot.message_handler(commands=['start'])
def start_cmd(message: Message):
    bot.send_message(chat_id=message.chat.id, text="Привет, я робот собутыльник! Нажми /help и узнай, что я могу.")


@bot.message_handler(commands=['help'])
def help_cmd(message: Message):
    bot.send_message(chat_id=message.chat.id, text="/help - вывод всех команд.\n"
                                                   "/go_drunk - начать попойку\n"
                                                   "/users - вывести всех пользователей\n"
                                                   "/ban_users - вывести всех пользователей")


@bot.message_handler(commands=['users'])
def user_cmd(message: Message):
    text = ''
    for i in user_table:
        text += str(i) + "\n"
    bot.send_message(chat_id=message.chat.id, text=text)


@bot.message_handler(commands=['ban_users'])
def ban_user_cmd(message: Message):
    text = ''
    for i in ban_user_table:
        text += str(i) + "\n"
        bot.send_message(chat_id=message.chat.id, text=text)


@bot.message_handler(commands=['go_drunk'])
def drunk0_cmd(message: Message):
    bot.set_state(user_id=message.from_user.id, state=DrunkStates.state_1, chat_id=message.chat.id)
    bot.send_message(chat_id=message.chat.id, text="Что будем пить? "
                                                   "Водку или водку?")


@bot.message_handler(state=DrunkStates.state_1)
def drunk1_cmd(message: Message):
    bot.set_state(user_id=message.from_user.id, chat_id=message.chat.id, state=DrunkStates.state_2)
    bot.send_message(chat_id=message.chat.id, text="Ну вот и выпьем за это\n"
                                                   "*через некоторое время*\n"
                                                   "Ты меня уважаешь?\n")


@bot.message_handler(state=DrunkStates.state_2)
def drunk2_cmd(message: Message):
    bot.set_state(user_id=message.from_user.id, state=DrunkStates.state_3, chat_id=message.chat.id)
    bot.send_message(chat_id=message.chat.id, text="Ладно, пойдем покурить? Расскажи хоть анекдот")


@bot.message_handler(state=DrunkStates.state_3)
def drunk3_cmd(message: Message):
    bot.delete_state(user_id=message.from_user.id)
    bot.send_message(chat_id=message.chat.id, text="Видишь собаку, а смог бы ее порвать за ноги. Я смогу\n"
                                                   "*И тут началось начало конца*"
                                                   "*200 кг алабай разорвал в клочья твоего собутыльника, а после и тебя\n*"
                                                   "*Но утром ты проснулся, как ни в чем не бывало в своей кровати*"
                                                   "*И лишь помнишь мутный силуэт огромного черного паука и имя Василий*")


@bot.message_handler(money=True)
def sum_cmd(message: Message):
    bot.set_state(user_id=message.from_user.id, state=MyOtherStates.state_1, chat_id=message.chat.id)
    bot.send_message(chat_id=message.chat.id, text="О, ты мне даешь денег, кайфово. Пасиб за " + message.text)


@bot.message_handler(state=MyOtherStates.state_1)
def sum_cmd(message: Message):
    bot.set_state(user_id=message.from_user.id, state=MyOtherStates.state_2, chat_id=message.chat.id)
    bot.send_message(chat_id=message.chat.id, text="А я пивка купил на эти деньги, го разопьем\n"
                                                   "*Через некоторое время*"
                                                   "Что-то не хватило дай еще")


@bot.message_handler(state=MyOtherStates.state_2)
def sum_cmd(message: Message):
    bot.delete_state(user_id=message.from_user.id)
    bot.send_message(chat_id=message.chat.id, text="Ну ладно попойка кончилась")


@bot.message_handler(content_types=['text', 'audio', 'document', 'animation', 'game', 'photo', 'sticker', 'video',
                                    'video_note', 'voice', 'contact', 'location', 'venue', 'dice', 'invoice',
                                    'successful_payment', 'connected_website', 'poll', 'passport_data', 'web_app_data'])
def drunk_cmd(message: Message):
    bot.send_message(chat_id=message.chat.id, text="Поздоровайся с Василием")


@bot.my_chat_member_handler()
def ban_user(chat_member: ChatMemberUpdated):
    if not (chat_member.from_user.id in user_table or chat_member.from_user.id in ban_user_table):
        ban_user_table.add(chat_member.from_user.id)
    elif chat_member.from_user.id in user_table:
        user_table.remove(chat_member.from_user.id)
        ban_user_table.add(chat_member.from_user.id)
    elif chat_member.from_user.id in ban_user_table:
        ban_user_table.remove(chat_member.from_user.id)
        user_table.add(chat_member.from_user.id)


bot.infinity_polling(allowed_updates=update_types)
