from telebot.handler_backends import State, StatesGroup

class BookingState(StatesGroup):
    choosing_time = State()