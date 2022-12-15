import pytz
from pytz import timezone
import tzlocal 
from flask_login import current_user
from setup.main import app as flask_app

def datetimefilter(value, format="%I:%M %p"):
    tz = pytz.timezone(current_user.tz.name) # timezone you want to convert to from UTC

    utc = pytz.timezone('UTC')  
    value = utc.localize(value, is_dst=None).astimezone(pytz.utc)
    local_dt = value.astimezone(tz)
    return local_dt.strftime(format)

flask_app.jinja_env.filters['datetimefilter'] = datetimefilter