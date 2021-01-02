from client import exception, json_manager, ini_manager, origin
from client.external import admin, organizer, rsn_register, vote
from client.config import config as c, language as l


async def module_status_check(ctx, name, guild_path, function, typef=None):
    try:
        guild_l = await origin.get_language(ctx.guild.id)
        if str(ctx.message.channel.type) == 'text':
            msg_noconfig = l.module_permissions[guild_l]['msg_noconfig'].format(name)
            msg_deactive = l.module_permissions[guild_l]['msg_deactive'].format(name)
            msg_private = l.module_permissions[guild_l]['msg_private'].format(name)

            if typef is None:
                if await permission_status(ctx, name):
                    path = guild_path.format(ctx.guild.id)
                    if await ini_manager.get_status('STATUS', 'STATUS', path):
                        await function(ctx)
                    else:
                        await ctx.send(msg_noconfig)
                else:
                    await ctx.send(msg_deactive)
            elif not typef:
                if await private_permission_status(ctx, name):
                    await function(ctx)
                else:
                    await ctx.send(msg_private.format(name))
            else:
                if await permission_status(ctx, name):
                    path = guild_path.format(ctx.guild.id)
                    path0 = '{}{}{}'.format(c.CLIENT_PATH['guild'], str(ctx.guild.id), c.CLIENT_JSON['server'])
                    server_config = await json_manager.get_json(path0)

                    ini = await ini_manager.get_ini(path)
                    CHANNEL_PERMISSIONS = int(ini['CHANNEL_PERMISSIONS']['STATUS'])
                    if await ini_manager.get_status('STATUS', 'STATUS', path):
                        if server_config['chat0'] == ctx.channel.id:
                            if CHANNEL_PERMISSIONS == 1:
                                await function(ctx)
                            else:
                                await ctx.send(l.module_permissions[guild_l]['msg_restricted'])
                        else:
                            await function(ctx)
                    else:
                        await ctx.send(msg_noconfig)
                else:
                    await ctx.send(msg_deactive)

            if ctx.guild.owner.id != ctx.author.id or ctx.message.author.guild_permissions.administrator is not True:
                await ctx.message.delete()
        else:
            await ctx.send(l.module_permissions[guild_l]['msg_restricted_pm'])
    except Exception as error:
        await exception.error(error)


async def get_user_permission(source1, keys, values):
    try:
        STATUS = False
        STATUS_COUNT = 0
        source = await json_manager.get_json(source1)

        for line in source:
            if line[keys[0]] == values[0]:
                STATUS_COUNT += 1

                if line[keys[1]] >= values[1]:
                    STATUS_COUNT += 1

            if STATUS_COUNT == len(keys):
                STATUS = True
        return STATUS
    except Exception as error:
        await exception.error(error)


async def permission_status(ctx, module):
    try:
        permission = await check_module_permission(ctx)
        for perm in permission:
            if perm == module:
                return True
    except Exception as error:
        await exception.error(error)


async def private_permission_status(ctx, module):
    try:
        permission = await check_private_module_permission(ctx)
        for perm in permission:
            if perm == module:
                return True
    except Exception as error:
        await exception.error(error)


async def check_module_permission(ctx):
    try:
        modules = await json_manager.get_json(c.CLIENT_PATH['guild'] + str(ctx.guild.id) + c.CLIENT_JSON['modules'])
        permissions = []
        for module_p, permission in modules.items():
            if permission == 1:
                permissions.append(module_p)
        return permissions
    except Exception as error:
        await exception.error(error)


async def check_private_module_permission(ctx):
    try:
        modules = await json_manager.get_json(c.CLIENT_PATH['guild'] + c.CLIENT_JSON['private'])
        permissions = []
        for module_p, guild in modules.items():
            for id in guild['guild']:
                if id == ctx.guild.id:
                    permissions.append(module_p)
        return permissions
    except Exception as error:
        await exception.error(error)


async def event_listener_message_permission(message, client):
    try:
        server_config = await json_manager.get_json(c.CLIENT_PATH['guild'] + str(message.guild.id) + c.CLIENT_JSON['server'])
        modules = await json_manager.get_json(c.CLIENT_PATH['guild'] + str(message.guild.id) + c.CLIENT_JSON['modules'])
        for module_p, permission in modules.items():
            if module_p == 'admin' and permission == 1:
                if server_config['chat1'] != message.channel.id:
                    await admin.admin.remove_message(message)

            if module_p == rsn_register.rsn_register.name and permission == 1:
                if server_config['rsn'] == message.channel.id:
                    await rsn_register.rsn_register.rsn_registration(client, message)

    except Exception as error:
        await exception.error(error)


async def event_listener_reaction_permission(payload, client, status):
    try:
        server_config = await json_manager.get_json(c.CLIENT_PATH['guild'] + str(payload.guild_id) + c.CLIENT_JSON['server'])
        modules = await json_manager.get_json(c.CLIENT_PATH['guild'] + str(payload.guild_id) + c.CLIENT_JSON['modules'])
        for module_p, permission in modules.items():
            if module_p == 'vote' and permission == 1:
                await vote.vote.check_vote(payload, status)

            if module_p == 'organizer' and permission == 1:
                if server_config['events'] == payload.channel_id:
                    await organizer.organizer.event_participants(client, payload, server_config, status)
    except Exception as error:
        await exception.error(error)
