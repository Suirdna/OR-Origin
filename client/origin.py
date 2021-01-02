from client import json_manager, exception
from client.config import config as c
import random
import locale

async def get_region(guild):
    try:
        path = c.CLIENT_JSON['guild']
        if await json_manager.get_status(path, 'guild_id', guild):
            data = await json_manager.get_data(path)
            for guild_data in data:
                if guild_data['guild_id'] == guild:
                    return guild_data['time_line']
    except Exception as error:
        await exception.error(error)

async def get_language(guild):
    try:
        path = c.CLIENT_JSON['guild']
        if await json_manager.get_status(path, 'guild_id', guild):
            data = await json_manager.get_data(path)
            for guild_data in data:
                if guild_data['guild_id'] == guild:
                    return guild_data['language']
    except Exception as error:
        await exception.error(error)

async def get_locale(region='en_US.utf8'):
    try:
        return locale.setlocale(locale.LC_ALL, region)
    except Exception as error:
        await exception.error(error)

async def find_and_replace(string):
    try:
        data = str(string).replace('<', '')
        data = data.replace('>', '')
        data = data.replace('!', '')
        data = data.replace('@', '')
        data = data.replace('#', '')
        data = data.replace('&', '')
        if str(data).isdigit():
            return int(data)
        else:
            return data
    except Exception as error:
        await exception.error(error)

async def randomize():
    try:
        value = random.randint(1, 50000000)
        return value
    except Exception as error:
        await exception.error(error)
