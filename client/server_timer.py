from client import exception
from client.config import config as c
from datetime import datetime, timedelta
from pytz import timezone
import pytz

async def get_specdate(date, weeks=None, days=None, hours=None, minutes=None):
    try:
        if weeks:
            date = date + timedelta(weeks=weeks)

        if days:
            date = date + timedelta(days=days)

        if hours:
            date = date + timedelta(hours=hours)

        if minutes:
            date = date + timedelta(minutes=minutes)

        return date
    except Exception as error:
        await exception.error(error)

async def get_timedelta(weeks=None, days=None, hours=None, minutes=None, region=None):
    try:
        date = await get_current_time(region)
        if weeks:
            date = date + timedelta(weeks=weeks)

        if days:
            date = date + timedelta(days=days)

        if hours:
            date = date + timedelta(hours=hours)

        if minutes:
            date = date + timedelta(minutes=minutes)

        return date
    except Exception as error:
        await exception.error(error)

async def get_current_date(region):
    try:
        date = await get_current_time(region)
        return date.strftime('%y.%m.%d')
    except Exception as error:
        await exception.error(error)

async def get_current_time(region):
    try:
        LT = timezone(region)
        return datetime.now(LT)
    except Exception as error:
        await exception.error(error)

async def get_server_current_date():
    try:
        date = await get_server_current_time()
        return date.strftime('%y.%m.%d')
    except Exception as error:
        await exception.error(error)

async def get_server_current_time():
    try:
        LT = timezone(c.CLIENT_REGION)
        return datetime.now(LT)
    except Exception as error:
        await exception.error(error)

async def check_status_timezone(tzone):
    try:
        if tzone in pytz.all_timezones:
            return True
    except Exception as error:
        await exception.error(error)