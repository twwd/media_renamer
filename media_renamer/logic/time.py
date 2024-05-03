from datetime import datetime

from dateutil import tz


def utc_to_local(date_utc: datetime):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()
    # Tell the datetime object that it's in UTC time zone since
    # datetime objects are 'naive' by default
    date_utc = date_utc.replace(tzinfo=from_zone)
    # Convert time zone
    local_date = date_utc.astimezone(to_zone)
    return local_date
