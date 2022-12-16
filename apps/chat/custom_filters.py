import pytz
from pytz import timezone
# import tzlocal 
from flask_login import current_user
from . views import chat_router

@chat_router.app_template_filter()
def datetimefilter(value, format="%I:%M %p"):
    tzname = current_user.tzname
    print(tzname)
    tz = pytz.timezone(tzname) # timezone you want to convert to from UTC

    utc = pytz.timezone('UTC')  
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(format)

@chat_router.app_template_filter()
def unread_messages_count(messages, other_user):
    count = messages.filter_by(sender=other_user, is_read=False).count()
    return count
