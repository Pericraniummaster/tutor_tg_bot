from services.calendar_service import calendar_service, CALENDAR_ID
from datetime import datetime, timedelta

def get_available_slots():
    now = datetime.now(datetime.timezone.utc)
    slots = []
    for day_offset in range(7):  # nearest week
        for hour in range(10, 19):  # checking hours 10:00-18:00
            slot = now + timedelta(days=day_offset, hours=hour-now.hour, minutes=-now.minute, seconds=-now.second, microseconds=-now.microsecond)
            if slot > now:
                slots.append(slot)
    return slots

def book_slot(user, slot_time_str):
    try:
        slot_time = datetime.fromisoformat(slot_time_str)
        description = f"User: @{user.username or 'no_username'} | ID: {user.id}"

        event = {
            'summary': 'Бронирование через Telegram',
            'description': description,
            'start': {
                'dateTime': slot_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': (slot_time + timedelta(hours=1)).isoformat(),
                'timeZone': 'UTC',
            },
        }

        calendar_service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
        return True

    except Exception as e:
        print(e)
        return False

def get_user_events(user):
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = calendar_service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=now,
        maxResults=20,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    user_events = []

    for event in events:
        description = event.get('description', '')
        if str(user.id) in description or (user.username and f"@{user.username}" in description):
            user_events.append(event)

    return user_events

def cancel_event(event_id):
    try:
        calendar_service.events().delete(calendarId=CALENDAR_ID, eventId=event_id).execute()
        return True
    except Exception as e:
        print(e)
        return False
