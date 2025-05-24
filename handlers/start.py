from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

def register_handlers(bot):
    
    @bot.message_handler(commands=['start'])
    def start_command(message: Message):
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton('Записаться на встречу', callback_data='book'))
        markup.add(InlineKeyboardButton('Отменить встречу', callback_data='cancel'))
        
        bot.send_message(
            message.chat.id,
            "Привет! Я помогу тебе выбрать время для встречи.\n Выбери действие:",
            reply_markup=markup
        )
