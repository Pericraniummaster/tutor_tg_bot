from telebot.types import Message, CallbackQuery
from services.booking_service import get_user_events, cancel_event
from utils.keyboards import generate_cancel_keyboard

def register_handlers(bot):

    @bot.message_handler(commands=['cancel'])
    def cancel_booking(message: Message):
        events = get_user_events(message.from_user)

        if not events:
            bot.send_message(message.chat.id, "У вас нет активных записей.")
            return

        markup = generate_cancel_keyboard(events)
        bot.send_message(message.chat.id, "Выберите запись для отмены:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: call.data.startswith('cancel_'))
    def confirm_cancellation(call: CallbackQuery):
        event_id = call.data.replace('cancel_', '')
        success = cancel_event(event_id)

        if success:
            bot.send_message(call.message.chat.id, "✅ Ваша запись отменена.")
        else:
            bot.send_message(call.message.chat.id, "❌ Произошла ошибка при отмене.")
