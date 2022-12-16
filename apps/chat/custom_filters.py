import pytz
from pytz import timezone
from datetime import datetime
# import tzlocal 
from flask_login import current_user
from . views import chat_router

@chat_router.app_template_filter()
def datetimefilter(value, format="%I:%M %p"):
    tzname = current_user.tzname
    tz = pytz.timezone(tzname) # timezone you want to convert to from UTC

    utc = pytz.timezone('UTC')
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)

    current_date = utc.localize(datetime.utcnow(), is_dst=None).astimezone(pytz.utc)
    current_date = current_date.astimezone(tz)

    new_dt = local_dt.strftime(format)
    if current_date.date() == local_dt.date():
        new_dt = local_dt.strftime('%H:%M')
    elif current_date.day - local_dt.day == 1 and current_date.month == local_dt.month and current_date.year == local_dt.year:
        new_dt = 'yesterday'
    else:
        new_dt = local_dt.strftime('%d/%m/%Y')

    return new_dt

@chat_router.app_template_filter()
def unread_messages_count(messages, other_user):
    count = messages.filter_by(sender=other_user, is_read=False).count()
    return count
