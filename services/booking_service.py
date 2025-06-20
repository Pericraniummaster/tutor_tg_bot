from services.calendar_service import calendar_service, CALENDAR_ID
from datetime import datetime, timedelta

def get_available_slots():
    now = datetime.now(datetime.timezone.utc)
    end = now + timedelta(days=7)

    # Generating proposed slots for the next 7 days
    proposed_slots = []
    for day_offset in range(7):
        for hour in range(10, 19):
            slot = now.replace(hour=hour, minute=0, second=0, microsecond=0) + timedelta(days=day_offset)
            if slot > now:
                proposed_slots.append(slot)

    # checking busy times in the calendar
    body = {
        "timeMin": now.isoformat(),
        "timeMax": end.isoformat(),
        "timeZone": "UTC",
        "items": [{"id": CALENDAR_ID}],
    }

    busy_times = calendar_service.freebusy().query(body=body).execute()
    busy_periods = busy_times['calendars'][CALENDAR_ID]['busy']

    # Filtering out busy slots
    available_slots = []
    for slot in proposed_slots:
        slot_end = slot + timedelta(hours=1)
        is_busy = any(
            slot < datetime.fromisoformat(busy['end']) and slot_end > datetime.fromisoformat(busy['start'])
            for busy in busy_periods
        )
        if not is_busy:
            available_slots.append(slot)

    return available_slots

def book_slot(user, slot_time_str):
    try:
        slot_time = datetime.fromisoformat(slot_time_str)
        slot_end = slot_time + timedelta(hours=1)

        # checking if the slot is free
        body = {
            "timeMin": slot_time.isoformat(),
            "timeMax": slot_end.isoformat(),
            "timeZone": "UTC",
            "items": [{"id": CALENDAR_ID}],
        }

        busy = calendar_service.freebusy().query(body=body).execute()
        if busy['calendars'][CALENDAR_ID]['busy']:
            return False

        # If the slot is free, create an event
        description = f"User: @{user.username or 'no_username'} | ID: {user.id}"
        event = {
            'summary': 'Бронирование через Telegram',
            'description': description,
            'start': {'dateTime': slot_time.isoformat(), 'timeZone': 'UTC'},
            'end': {'dateTime': slot_end.isoformat(), 'timeZone': 'UTC'},
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
