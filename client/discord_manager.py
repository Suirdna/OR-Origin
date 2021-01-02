from client.config import config as c
from client import exception, file_manager
import discord

async def get_role(client, guild_id, role_id):
    try:
        SERVER = await get_server(client, guild_id)
        ROLE = None
        if SERVER:
            ROLE = SERVER.get_role(role_id)

        if ROLE:
            return ROLE
        else:
            return

    except Exception as error:
        await exception.error(error)

async def get_member(client, guild_id, member_id):
    try:
        SERVER = await get_server(client, guild_id)
        MEMBER = None
        if SERVER:
            MEMBER = SERVER.get_member(member_id)

        if MEMBER:
            return MEMBER
        else:
            return

    except Exception as error:
        await exception.error(error)

async def get_channel(client, guild_id, channel_id):
    try:
        SERVER = await get_server(client, guild_id)
        CHANNEL = None
        if SERVER:
            CHANNEL = SERVER.get_channel(channel_id)

        if CHANNEL:
            return CHANNEL
        else:
            return
    except Exception as error:
        await exception.error(error)

async def get_servers(client, directories):
    try:
        list_of_guild_folders = await file_manager.get_guild_directory(directories)
        guilds = []

        for guild in list_of_guild_folders:
            guilds.append(await get_server(client, guild))

        return guilds
    except Exception as error:
        await exception.error(error)

async def get_server(client, guild_id):
    try:
        SERVER = client.get_guild(guild_id)
        if SERVER:
            return SERVER
    except Exception as error:
        await exception.error(error)

async def find_general_channel(client, guild):
    try:
        SERVER = client.get_guild(guild.id)
        if SERVER:
            for channel_name in c.GUILD_CHANNELS:
                channel = discord.utils.get(client.get_all_channels(), guild__name=guild.name, name=channel_name)
                if channel:
                    return channel
    except Exception as error:
        await exception.error(error)