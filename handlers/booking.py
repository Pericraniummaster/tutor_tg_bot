from telebot.types import CallbackQuery
from states.booking_states import BookingState
from services.booking_service import get_available_slots, book_slot
from utils.keyboards import generate_slots_keyboard

def register_handlers(bot):
    
    @bot.callback_query_handler(func=lambda call: call.data == 'book')
    def start_booking(call: CallbackQuery):
        slots = get_available_slots()

        if not slots:
            bot.send_message(call.message.chat.id, "Свободных слотов нет. Попробуйте позже.")
            return

        markup = generate_slots_keyboard(slots)
        bot.send_message(call.message.chat.id, "Выберите удобное время:", reply_markup=markup)
        bot.set_state(call.from_user.id, BookingState.choosing_time, call.message.chat.id)

    @bot.callback_query_handler(state=BookingState.choosing_time)
    def choose_slot(call: CallbackQuery):
        slot_time = call.data  # дата и время слота в формате строки
        success = book_slot(call.from_user, slot_time)

        if success:
            bot.send_message(call.message.chat.id, "✅ Вы успешно записались!")
        else:
            bot.send_message(call.message.chat.id, "❌ Этот слот уже занят.")
        
        bot.delete_state(call.from_user.id, call.message.chat.id)
