from telebot.handler_backends import State, StatesGroup


class DrunkStates(StatesGroup):
    state_1 = State()
    state_2 = State()
    state_3 = State()


class MyOtherStates(StatesGroup):
    state_1 = State()
    state_2 = State()