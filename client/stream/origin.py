from client.config import config as c
from client.stream import json_manager, exception

def get_region(guild):
    try:
        path = c.CLIENT_JSON['guild']
        if json_manager.get_status(path, 'guild_id', guild):
            data = json_manager.get_data(path)
            for guild_data in data:
                if guild_data['guild_id'] == guild:
                    return guild_data['time_line']
    except Exception as error:
        exception.error(error)