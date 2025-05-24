from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def generate_slots_keyboard(slots):
    markup = InlineKeyboardMarkup()
    for slot in slots:
        button_text = slot.strftime('%d.%m %H:%M')
        callback_data = slot.isoformat()
        markup.add(InlineKeyboardButton(text=button_text, callback_data=callback_data))
    return markup

def generate_cancel_keyboard(events):
    markup = InlineKeyboardMarkup()
    for event in events:
        start_time = event['start'].get('dateTime', event['start'].get('date'))
        button_text = start_time[:16].replace('T', ' ')
        event_id = event['id']
        markup.add(InlineKeyboardButton(text=button_text, callback_data=f'cancel_{event_id}'))
    return markup