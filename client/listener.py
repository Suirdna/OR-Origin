from client import exception, console_interface, file_manager, json_manager, permissions, discord_manager, embed_creator
from client.config import config as c, language as l
import discord

async def message(message_content, client):
    try:
        if str(message_content.channel.type) == 'text':
            await permissions.event_listener_message_permission(message_content, client)
    except Exception as error:
        await exception.error(error)

async def raw_reaction_add(payload, client, status):
    try:
        await permissions.event_listener_reaction_permission(payload, client, status)
    except Exception as error:
        await exception.error(error)

async def raw_reaction_remove(payload, client, status):
    try:
        await permissions.event_listener_reaction_permission(payload, client, status)
    except Exception as error:
        await exception.error(error)

async def guild_join(client, guild):
    try:
        client_message = 'Guild id: {}'.format(guild.id)
        new_json_string = {'data': []}
        path1 = c.ORIGIN_PATH['embed.server.json']
        json_string = await json_manager.get_json(path1)

        json_data = {
            'guild_id': guild.id,
            'owner_id': guild.owner_id,
            'guild_name': guild.name,
            'language': 'EN',
            'time_line': c.CLIENT_REGION
        }

        if await json_manager.get_status(c.CLIENT_JSON['guild'], 'guild_id', guild.id):
            target_keys = []
            target_values = []

            for key in json_data.keys():
                target_keys.append(key)

            for value in json_data.values():
                target_values.append(value)

            await json_manager.update(c.CLIENT_JSON['guild'], 'guild_id', guild.id, target_keys, target_values)
            await console_interface.console_message(c.CLIENT_MESSAGES['guild_rejoin'], client_message)
        else:
            await file_manager.create_directory(c.CLIENT_PATH['guild'], guild.id)
            await file_manager.create_directory(c.CLIENT_PATH['guild'] + str(guild.id), c.CLIENT_PATH['logs'])
            await file_manager.copy_directory(c.CLIENT_PATH['guild'] + c.CLIENT_PATH['default'], c.CLIENT_PATH['guild'] + str(guild.id))
            await json_manager.create(c.CLIENT_JSON['guild'], json_data)
            await console_interface.console_message(c.CLIENT_MESSAGES['guild_join'], client_message)

        channel = await discord_manager.find_general_channel(client, guild)

        for key, value in json_string['EN']['join'].items():
            if int(key) == 1:
                new_json_string['data'].append({
                    'name{}'.format(key): str(value['name']).format(guild.name, c.CLIENT_NAME),
                    'value{}'.format(key): str(value['value'].format(c.WEB_LINKS['setup']))
                })
            else:
                new_json_string['data'].append({
                    'name{}'.format(key): str(value['name']),
                    'value{}'.format(key): str(value['value'])
                })

        if channel:
            await embed_creator.create_embed(guild.id, discord.Color.gold(), False, guild.icon_url, c.CLIENT_ICON, l.server['EN']['embed_3'].format(guild.name), new_json_string['data'], False, author=False, channel=channel, description=False)

        await embed_creator.create_embed(guild.id, discord.Color.gold(), False, guild.icon_url, c.CLIENT_ICON, l.server['EN']['embed_3'].format(guild.name), new_json_string['data'], False, author=guild.owner, channel=False, description=False)
    except Exception as error:
        await exception.error(error)