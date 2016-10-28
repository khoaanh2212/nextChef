from datetime import datetime

from django.utils.timezone import utc


def str_to_datetime(date):
    """
    Convert datetimes sent to the API to python datetime objects
    """
    return datetime.fromtimestamp(int(date), tz=utc)
