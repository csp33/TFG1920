from datetime import datetime

import pytz


def get_utc_result(value, timezone='Europe/Madrid'):
    # Get full datetime
    dt = datetime.today()
    tmp = datetime.strptime(value, '%H:%M')
    dt = dt.replace(hour=tmp.hour, minute=tmp.minute, second=0)
    # Add timezone
    timezone = pytz.timezone(timezone)
    result = timezone.localize(dt)
    return result.astimezone(pytz.utc)


def to_locale(time, timezone='Europe/Madrid'):
    return pytz.utc.localize(time).astimezone(pytz.timezone(timezone))