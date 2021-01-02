from client.config import config as c
from client.stream import exception
from datetime import datetime
from pytz import timezone

def get_current_date(region):
    try:
        date = get_current_time(region)
        return date.strftime('%y.%m.%d')
    except Exception as error:
        exception.error(error)

def get_current_time(region):
    try:
        LT = timezone(region)
        return datetime.now(LT)
    except Exception as error:
        exception.error(error)

def get_server_current_date():
    try:
        date = get_server_current_time()
        return date.strftime('%y.%m.%d')
    except Exception as error:
        exception.error(error)

def get_server_current_time():
    try:
        LT = timezone(c.CLIENT_REGION)
        return datetime.now(LT)
    except Exception as error:
        exception.error(error)