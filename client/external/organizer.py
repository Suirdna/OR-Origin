from client import exception, embed_creator, console_interface, discord_manager, ini_manager, json_manager, logger, origin, permissions, server_timer
from client.config import config as c, language as l
from discord.ext import commands, tasks
import discord, locale

class organizer(commands.Cog):
    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    name = 'organizer'

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    @staticmethod
    async def event_participants(client, payload, server, status):
        try:
            if payload.channel_id == server['events'] and payload.emoji.name == l.DISCORD_EMOTE['positive']:
                path = c.GUILD_PATH['event.json'].format(payload.guild_id)
                path1 = c.GUILD_PATH['organizer.ini'].format(payload.guild_id)

                role_id = await ini_manager.get_data('SECTION1', 'EVENT_ROLE', path1)
                role = await discord_manager.get_role(client, payload.guild_id, int(role_id))

                if role:
                    user = await discord_manager.get_member(client, payload.guild_id, payload.user_id)
                    await user.add_roles(role, reason='{}'.format(c.DISCORD_MESSAGES['event_role_added']), atomic=True)

                if await json_manager.get_status(path, 'message_id', payload.message_id):
                    data = await json_manager.get_data(path)
                    for value in data:
                        if value['message_id'] == payload.message_id:
                            if status:
                                SUM = value['participants'] + 1
                            else:
                                SUM = value['participants'] - 1
                            await json_manager.update(path, 'message_id', payload.message_id, 'participants', SUM)
        except Exception as error:
            await exception.error(error)

    async def preprocessor(self, ctx, arg, option, extra):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            path = c.CLIENT_PATH['guild'] + str(ctx.guild.id) + c.CLIENT_JSON['server']
            path2 = c.GUILD_PATH['event.json'].format(ctx.guild.id)
            LIST1 = self.NAME
            LIST2 = self.ICON
            STRING = str(arg).split(' ')

            DATA = await json_manager.get_data(path2)
            ID = await origin.randomize()
            STATUS = True
            STATUS2 = False

            while STATUS:
                for data in DATA:
                    if data['id'] == ID:
                        STATUS2 = True
                if not STATUS2:
                    STATUS = False
                else:
                    ID = await origin.randomize()

            server_config = await json_manager.get_json(path)
            CHANNEL = await discord_manager.get_channel(self.client, ctx.guild.id, server_config['events'])

            if CHANNEL:
                win = discord.Embed(
                    description=l.organizer[guild_l]['embed_configuration']['description'].format(
                    ctx.author.mention,
                    STRING[2], STRING[3], LIST1[option], l.DISCORD_EMOTE['positive']),
                    color=discord.Color.dark_blue(),
                )
                win.set_author(name=l.organizer[guild_l]['embed_1'].format(ctx.guild.name), icon_url=ctx.guild.icon_url)
                win.set_thumbnail(url=LIST2[option])
                if extra != '':
                    win.add_field(name=l.organizer[guild_l]['embed_configuration']['field_1'], value='{}'.format(extra), inline=False)
                win.add_field(name=l.organizer[guild_l]['embed_configuration']['field_2'], value='{}'.format(l.organizer[guild_l]['embed_configuration']['extra_1']), inline=False)
                message = await CHANNEL.send(embed=win)

                await message.add_reaction(l.DISCORD_EMOTE['positive'])
                json_string = {'id': ID, 'user_id': ctx.author.id, 'message_id': message.id, 'event_name': LIST1[option], 'date_start': STRING[2], 'date_end': '', 'time_start': int(STRING[3]), 'time_end': 0, 'participants': 0, 'status': 0, 'type': 0}

                await json_manager.create(path2, json_string)

                CHANNEL1 = await discord_manager.get_channel(self.client, ctx.guild.id, server_config['chat0'])
                CHANNEL2 = await discord_manager.get_channel(self.client, ctx.guild.id, server_config['chat1'])

                await ctx.author.send(l.organizer[guild_l]['msg_success_1'])

                if CHANNEL1:
                    await CHANNEL1.send(l.organizer[guild_l]['msg_1'].format(LIST1[option], server_config['events']))
                if CHANNEL2:
                    await CHANNEL2.send(l.organizer[guild_l]['msg_1'].format(LIST1[option], server_config['events']))
            else:
                await ctx.send(l.organizer[guild_l]['msg_error_1'].format(ctx.author.mention))
        except Exception as error:
            await exception.error(error)

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    @staticmethod
    async def fun_organize(ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            guild_t = await origin.get_region(ctx.guild.id)
            path = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
            target_keys1 = ['user_id', 'user_status']
            target_values1 = [ctx.author.id, c.USER_PERMISSIONS['organizer']]

            if await permissions.get_user_permission(path, target_keys1, target_values1) or ctx.author.id == ctx.guild.owner.id or ctx.author.id == c.CLIENT_ADMINISTRATION_ID:
                if ctx.message.content == ".organize":
                    path3 = c.ORIGIN_PATH['embed.organizer.json']
                    current_guild = await server_timer.get_current_time(guild_t)
                    json_string = await json_manager.get_json(path3)
                    new_json_string = {'data': []}

                    for key, value in json_string[guild_l]['organize'].items():
                        if int(key) == 1:
                            new_json_string['data'].append({
                                'name{}'.format(key): str(value['name']),
                                'value{}'.format(key): value['value'].format(
                                    current_guild.strftime('%m.%d'),
                                    current_guild.hour + 1
                                )
                            })

                    await embed_creator.create_embed(ctx, discord.Color.dark_blue(), False, ctx.guild.icon_url, c.CLIENT_ICON, l.organizer[guild_l]['embed_2'].format(ctx.guild.name), new_json_string['data'], False)
            else:
                await ctx.author.send(l.user_permissions[guild_l]['msg_restricted_1'])
        except Exception as error:
            await exception.error(error)

    async def fun_add(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            guild_t = await origin.get_region(ctx.guild.id)
            path = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
            target_keys1 = ['user_id', 'user_status']
            target_values1 = [ctx.author.id, c.USER_PERMISSIONS['organizer']]

            if await permissions.get_user_permission(path, target_keys1, target_values1) or ctx.author.id == ctx.guild.owner.id or ctx.author.id == c.CLIENT_ADMINISTRATION_ID:
                LIST = self.PRE

                STRING = str(ctx.message.content).split(' ')
                EXTRA = ''
                count = 0

                for value in STRING[4:]:
                    EXTRA += '{} '.format(value)

                for event in LIST:
                    if STRING[1] == event:
                        await self.preprocessor(ctx, ctx.message.content, count, EXTRA)
                        guild_current = await server_timer.get_current_time(guild_t)
                        client_message = 'Guild id: {} | Guild time: {} | Member id: {} | Event: {}'.format(ctx.guild.id, guild_current.strftime('%H:%M'), ctx.author.id, event)
                        await console_interface.console_message(c.CLIENT_MESSAGES['organizer_add'], client_message)
                        await logger.log_event(ctx, 'organizer', c.CLIENT_MESSAGES['organizer_add'], client_message)
                    count += 1
            else:
                await ctx.author.send(l.user_permissions[guild_l]['msg_restricted_1'])
        except Exception as error:
            await exception.error(error)

    @staticmethod
    async def fun_remove(ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            guild_t = await origin.get_language(ctx.guild.id)
            path = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
            target_keys1 = ['user_id', 'user_status']
            target_values1 = [ctx.author.id, c.USER_PERMISSIONS['organizer']]

            if await permissions.get_user_permission(path, target_keys1, target_values1) or ctx.author.id == ctx.guild.owner.id or ctx.author.id == c.CLIENT_ADMINISTRATION_ID:
                STRING = str(ctx.message.content).split(' ')
                if len(STRING) == 2 and STRING[1].isdigit():
                    path1 = c.GUILD_PATH['event.json'].format(ctx.guild.id)
                    if await json_manager.get_status(path1, 'id', int(STRING[1])):
                        guild_current = await server_timer.get_current_time(guild_t)
                        await json_manager.delete(path1, 'id', int(STRING[1]))
                        client_message = 'Guild id: {} | Guild time: {} | Member id: {} | Event id: {}'.format(ctx.guild.id, guild_current.strftime('%H:%M'), ctx.author.id, STRING[1])
                        await console_interface.console_message(c.CLIENT_MESSAGES['organizer_remove'], client_message)
                        await logger.log_event(ctx, 'organizer', c.CLIENT_MESSAGES['organizer_remove'], client_message)
                        await ctx.author.send(l.organizer[guild_l]['msg_success_2'])
                    else:
                        await ctx.author.send(l.organizer[guild_l]['msg_error_2'])
                else:
                    await ctx.send(l.organizer[guild_l]['msg_badformat_2'])
            else:
                await ctx.author.send(l.user_permissions[guild_l]['msg_restricted_1'])
        except Exception as error:
            await exception.error(error)

    @staticmethod
    async def fun_events(ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            path = c.CLIENT_PATH['guild'] + str(ctx.guild.id) + c.CLIENT_JSON['server']
            server_config = await json_manager.get_json(path)
            await origin.get_locale()

            path1 = c.GUILD_PATH['event.json'].format(ctx.guild.id)
            DATA = await json_manager.get_data(path1)

            if DATA:
                win = discord.Embed(
                    color=discord.Color.dark_blue(),
                )
                win.set_thumbnail(url=ctx.guild.icon_url)
                win.set_author(name=l.organizer[guild_l]['embed_1'].format(ctx.guild.name), icon_url=ctx.guild.icon_url)
                for value in DATA:
                    if value['type'] == 0:
                        win.add_field(name=l.organizer[guild_l]['embed_configuration']['field_3'].format(value['event_name'], value['id']).upper(), value=l.organizer[guild_l]['embed_configuration']['value_3'].format(str(value['date_start']), str(value['time_start']), value['user_id'], value['participants']), inline=False)

                    if value['type'] == 1 or value['type'] == 3:
                        win.add_field(name='{}'.format(value['event_name']).upper(), value=l.organizer[guild_l]['embed_configuration']['value_4'].format(str(value['date_start']), str(value['date_end']), str(value['time_start']), str(value['time_end']), value['user_id'], value['participants']), inline=False)

                    if value['type'] == 2 or value['type'] == 4:
                        win.add_field(name='{}'.format(value['event_name']).upper(), value=l.organizer[guild_l]['embed_configuration']['value_5'].format(str(value['date_start']), str(value['time_start']), locale.format_string('%d', value['xp_target'] if value['type'] == 2 else value['kc_target'], grouping=True), value['user_id'], value['participants']), inline=False)
                win.add_field(name='{}'.format(l.organizer[guild_l]['embed_configuration']['field_1']), value=l.organizer[guild_l]['embed_configuration']['extra_2'].format(server_config['events']), inline=True)
                await ctx.send(embed=win)
            else:
                await ctx.send(l.organizer[guild_l]['msg_2'])
        except Exception as error:
            await exception.error(error)

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    @tasks.loop(count=1)
    async def variable_init(self):
        try:
            path_global = c.GUILD_PATH['{}_g.ini'.format(self.name)]

            self.NAME = await json_manager.get_ini_list(path_global, 'CONSTANT1', 'NAME')
            self.ICON = await json_manager.get_ini_list(path_global, 'CONSTANT3', 'ICON')
            self.PRE = await json_manager.get_ini_list(path_global, 'CONSTANT2', 'PRE')

            await console_interface.console_message(c.CLIENT_MESSAGES['variable_init'].format(self.name))
        except Exception as error:
            await exception.error(error)

    def __init__(self, client):
        self.NAME = None
        self.ICON = None
        self.PRE = None

        self.variable_init.start()
        self.client = client

    @commands.command()
    async def organize(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_organize)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def add(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_add)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def remove(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_remove)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def events(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_events)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

def setup(client):
    client.add_cog(organizer(client))