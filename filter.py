from telebot.types import Message
from telebot.custom_filters import SimpleCustomFilter


class MoneyFilter(SimpleCustomFilter):
    key = "money"

    def check(self, update: Message) -> bool:
        try:
            int(update.text)
            return True
        except ValueError:
            return False
