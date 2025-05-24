from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

def register_handlers(bot):
    
    @bot.message_handler(commands=['start'])
    def start_command(message: Message):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Записаться на урок', callback_data='book'))
        markup.add(InlineKeyboardButton('Отменить урок', callback_data='cancel'))
        
        bot.send_message(
            message.chat.id,
            "Привет! Я помогу тебе забронировать время для занятий.\n Выбери действие:",
            reply_markup=markup
        )
