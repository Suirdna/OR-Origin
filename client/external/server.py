from client import exception, embed_creator, discord_manager, ini_manager, json_manager, permissions, origin, server_timer
from client.external import admin, dc_bank, organizer, rsn_register, vote, xp_tracker, kc_tracker
from client.config import config as c, language as l
from discord.ext import commands
import discord, locale

class server(commands.Cog):
    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    name = 'server'

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def deactive(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            if str(ctx.message.channel.type) == 'text':
                path = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
                target_keys = ['user_id', 'user_status']
                target_values = [ctx.author.id, c.USER_PERMISSIONS['dc_bank']]

                if ctx.author.id == c.CLIENT_ADMINISTRATION_ID or ctx.author.id == ctx.guild.owner.id or await permissions.get_user_permission(path, target_keys, target_values):
                    STRING = str(ctx.message.content).split(' ')
                    if len(STRING) == 2:
                        if STRING[1] == admin.admin.name:
                            path = c.GUILD_PATH['{}.ini'.format(admin.admin.name)].format(ctx.guild.id)
                            await ini_manager.update_data('STATUS', 'STATUS', '0', path)
                            await ctx.send(l.server[guild_l]['msg_success_4'])
                        elif STRING[1] == dc_bank.dc_bank.name:
                            path = c.GUILD_PATH['{}.ini'.format(dc_bank.dc_bank.name)].format(ctx.guild.id)
                            await ini_manager.update_data('STATUS', 'STATUS', '0', path)
                            await ctx.send(l.server[guild_l]['msg_success_4'])
                        elif STRING[1] == organizer.organizer.name:
                            path = c.GUILD_PATH['{}.ini'.format(organizer.organizer.name)].format(ctx.guild.id)
                            await ini_manager.update_data('STATUS', 'STATUS', '0', path)
                            await ctx.send(l.server[guild_l]['msg_success_4'])
                        elif STRING[1] == rsn_register.rsn_register.name:
                            path = c.GUILD_PATH['{}.ini'.format(rsn_register.rsn_register.name)].format(ctx.guild.id)
                            await ini_manager.update_data('STATUS', 'STATUS', '0', path)
                            await ctx.send(l.server[guild_l]['msg_success_4'])
                        elif STRING[1] == xp_tracker.xp_tracker.name:
                            path = c.GUILD_PATH['{}.ini'.format(xp_tracker.xp_tracker.name)].format(ctx.guild.id)
                            await ini_manager.update_data('STATUS', 'STATUS', '0', path)
                            await ctx.send(l.server[guild_l]['msg_success_4'])
                        elif STRING[1] == kc_tracker.kc_tracker.name:
                            path = c.GUILD_PATH['{}.ini'.format(kc_tracker.kc_tracker.name)].format(ctx.guild.id)
                            await ini_manager.update_data('STATUS', 'STATUS', '0', path)
                            await ctx.send(l.server[guild_l]['msg_success_4'])
                        elif STRING[1] == vote.vote.name:
                            path = c.GUILD_PATH['{}.ini'.format(vote.vote.name)].format(ctx.guild.id)
                            await ini_manager.update_data('STATUS', 'STATUS', '0', path)
                            await ctx.send(l.server[guild_l]['msg_success_4'])
                    else:
                        await ctx.send(l.server[guild_l]['msg_1'])
                else:
                    await ctx.send(l.user_permissions[guild_l]['msg_restricted_1'])
                await ctx.message.delete()
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def active(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            if str(ctx.message.channel.type) == 'text':
                path = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
                target_keys = ['user_id', 'user_status']
                target_values = [ctx.author.id, c.USER_PERMISSIONS['dc_bank']]

                if ctx.author.id == c.CLIENT_ADMINISTRATION_ID or ctx.author.id == ctx.guild.owner.id or await permissions.get_user_permission(path, target_keys, target_values):
                    STRING = str(ctx.message.content).split(' ')
                    if len(STRING) == 2:
                        path1 = c.CLIENT_PATH['guild'] + str(ctx.guild.id) + c.CLIENT_JSON['server']
                        server_config = await json_manager.get_json(path1)
                        if STRING[1] == admin.admin.name:
                            path = c.GUILD_PATH['{}.ini'.format(admin.admin.name)].format(ctx.guild.id)
                            ini = await ini_manager.get_ini(path)
                            admin_channel = await discord_manager.get_channel(self.client, ctx.guild.id, server_config['admin'])
                            role = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION1']['BAN']) if ini['SECTION1']['BAN'] != '' else None)
                            if role and admin_channel:
                                await ini_manager.update_data('STATUS', 'STATUS', '2', path)
                                await ctx.send(l.server[guild_l]['msg_success_3'])
                            else:
                                await ctx.send(l.server[guild_l]['msg_error_5'])
                        elif STRING[1] == dc_bank.dc_bank.name:
                            path = c.GUILD_PATH['{}.ini'.format(dc_bank.dc_bank.name)].format(ctx.guild.id)
                            ini = await ini_manager.get_ini(path)

                            accounting_channel = await discord_manager.get_channel(self.client, ctx.guild.id, server_config['dc_bank'])
                            sponsor_channel = await discord_manager.get_channel(self.client, ctx.guild.id, server_config['sponsor'])
                            thanks_channel = await discord_manager.get_channel(self.client, ctx.guild.id, server_config['thanks'])
                            admins = await discord_manager.get_member(self.client, ctx.guild.id, int(ini['SECTION1']['ADMIN']) if ini['SECTION1']['ADMIN'] != '' else None)

                            discord_top_1_role = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION2']['DISCORD_TOP_1']) if ini['SECTION2']['DISCORD_TOP_1'] != '' else None)
                            discord_top_2_role = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION2']['DISCORD_TOP_2']) if ini['SECTION2']['DISCORD_TOP_2'] != '' else None)
                            discord_top_3_role = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION2']['DISCORD_TOP_3']) if ini['SECTION2']['DISCORD_TOP_3'] != '' else None)
                            discord_top_4_role = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION2']['DISCORD_TOP_4']) if ini['SECTION2']['DISCORD_TOP_4'] != '' else None)
                            discord_top_5_role = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION2']['DISCORD_TOP_5']) if ini['SECTION2']['DISCORD_TOP_5'] != '' else None)

                            discord_top_1_count = ini['SECTION3']['DISCORD_TOP_1_COUNT'] if ini['SECTION3']['DISCORD_TOP_1_COUNT'] != '' else None
                            discord_top_2_count = ini['SECTION3']['DISCORD_TOP_2_COUNT'] if ini['SECTION3']['DISCORD_TOP_2_COUNT'] != '' else None
                            discord_top_3_count = ini['SECTION3']['DISCORD_TOP_3_COUNT'] if ini['SECTION3']['DISCORD_TOP_3_COUNT'] != '' else None
                            discord_top_4_count = ini['SECTION3']['DISCORD_TOP_4_COUNT'] if ini['SECTION3']['DISCORD_TOP_4_COUNT'] != '' else None
                            discord_top_5_count = ini['SECTION3']['DISCORD_TOP_5_COUNT'] if ini['SECTION3']['DISCORD_TOP_5_COUNT'] != '' else None

                            if admins and accounting_channel and sponsor_channel and thanks_channel and discord_top_1_role and discord_top_2_role and discord_top_3_role and discord_top_4_role and discord_top_5_role and discord_top_1_count and discord_top_2_count and discord_top_3_count and discord_top_4_count and discord_top_5_count:
                                await ini_manager.update_data('STATUS', 'STATUS', '2', path)
                                await ctx.send(l.server[guild_l]['msg_success_3'])
                            else:
                                await ctx.send(l.server[guild_l]['msg_error_5'])
                        elif STRING[1] == organizer.organizer.name:
                            path = c.GUILD_PATH['{}.ini'.format(organizer.organizer.name)].format(ctx.guild.id)
                            ini = await ini_manager.get_ini(path)

                            event_channel = await discord_manager.get_channel(self.client, ctx.guild.id, server_config['events'])
                            role = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION1']['EVENT_ROLE']) if ini['SECTION1']['EVENT_ROLE'] != '' else None)
                            if role and event_channel:
                                await ini_manager.update_data('STATUS', 'STATUS', '2', path)
                                await ctx.send(l.server[guild_l]['msg_success_3'])
                            else:
                                await ctx.send(l.server[guild_l]['msg_error_5'])
                        elif STRING[1] == rsn_register.rsn_register.name:
                            path = c.GUILD_PATH['{}.ini'.format(rsn_register.rsn_register.name)].format(ctx.guild.id)
                            ini = await ini_manager.get_ini(path)

                            rsn_registration_channel = await discord_manager.get_channel(self.client, ctx.guild.id, server_config['rsn'])
                            role = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION1']['ROLE']) if ini['SECTION1']['ROLE'] != '' else None)

                            if role and rsn_registration_channel:
                                await ini_manager.update_data('STATUS', 'STATUS', '2', path)
                                await ctx.send(l.server[guild_l]['msg_success_3'])
                            else:
                                await ctx.send(l.server[guild_l]['msg_error_5'])
                        elif STRING[1] == xp_tracker.xp_tracker.name:
                            path = c.GUILD_PATH['{}.ini'.format(xp_tracker.xp_tracker.name)].format(ctx.guild.id)
                            ini = await ini_manager.get_ini(path)

                            event_channel = await discord_manager.get_channel(self.client, ctx.guild.id, server_config['events'])
                            xp_event_channel = await discord_manager.get_channel(self.client, ctx.guild.id, server_config['xp_event'])
                            event_winner = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION1']['EVENT_WINNER']) if ini['SECTION1']['EVENT_WINNER'] != '' else None)
                            event_role = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION1']['EVENT_ROLE']) if ini['SECTION1']['EVENT_ROLE'] != '' else None)
                            if event_winner and event_role and event_channel and xp_event_channel:
                                await ini_manager.update_data('STATUS', 'STATUS', '2', path)
                                await ctx.send(l.server[guild_l]['msg_success_3'])
                            else:
                                await ctx.send(l.server[guild_l]['msg_error_5'])
                        elif STRING[1] == kc_tracker.kc_tracker.name:
                            path = c.GUILD_PATH['{}.ini'.format(kc_tracker.kc_tracker.name)].format(ctx.guild.id)
                            ini = await ini_manager.get_ini(path)

                            event_channel = await discord_manager.get_channel(self.client, ctx.guild.id, server_config['events'])
                            kc_event_channel = await discord_manager.get_channel(self.client, ctx.guild.id, server_config['kc_event'])
                            event_winner = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION1']['EVENT_WINNER']) if ini['SECTION1']['EVENT_WINNER'] != '' else None)
                            event_role = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION1']['EVENT_ROLE']) if ini['SECTION1']['EVENT_ROLE'] != '' else None)
                            if event_winner and event_role and event_channel and kc_event_channel:
                                await ini_manager.update_data('STATUS', 'STATUS', '2', path)
                                await ctx.send(l.server[guild_l]['msg_success_3'])
                            else:
                                await ctx.send(l.server[guild_l]['msg_error_5'])
                        elif STRING[1] == vote.vote.name:
                            path = c.GUILD_PATH['{}.ini'.format(vote.vote.name)].format(ctx.guild.id)
                            ini = await ini_manager.get_ini(path)

                            restriction = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION1']['RESTRICTION']) if ini['SECTION1']['RESTRICTION'] != '' else None)
                            count = ini['SECTION2']['COUNT'] if ini['SECTION2']['COUNT'] != '' else None
                            if restriction and count:
                                await ini_manager.update_data('STATUS', 'STATUS', '2', path)
                                await ctx.send(l.server[guild_l]['msg_success_3'])
                            else:
                                await ctx.send(l.server[guild_l]['msg_error_5'])
                    else:
                        await ctx.send(l.server[guild_l]['msg_1'])
                else:
                    await ctx.send(l.user_permissions[guild_l]['msg_restricted_1'])
                await ctx.message.delete()
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def setup(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            if str(ctx.message.channel.type) == 'text':
                path = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
                target_keys = ['user_id', 'user_status']
                target_values = [ctx.author.id, c.USER_PERMISSIONS['dc_bank']]

                if ctx.author.id == c.CLIENT_ADMINISTRATION_ID or ctx.author.id == ctx.guild.owner.id or await permissions.get_user_permission(path, target_keys, target_values):
                    STRING = str(ctx.message.content).split(' ')
                    if len(STRING) >= 5:
                        if STRING[1] == admin.admin.name:
                            path = c.GUILD_PATH['{}.ini'.format(admin.admin.name)].format(ctx.guild.id)
                            value = await origin.find_and_replace(STRING[4])
                            status = await ini_manager.update_data(STRING[2], STRING[3], value, path)
                            if status:
                                await ctx.send(l.server[guild_l]['msg_success_2'])
                            else:
                                await ctx.send(l.server[guild_l]['msg_error_4'])

                        elif STRING[1] == dc_bank.dc_bank.name:
                            path = c.GUILD_PATH['{}.ini'.format(dc_bank.dc_bank.name)].format(ctx.guild.id)
                            value = await origin.find_and_replace(STRING[4])
                            status = await ini_manager.update_data(STRING[2], STRING[3], value, path)
                            if status:
                                await ctx.send(l.server[guild_l]['msg_success_2'])
                            else:
                                await ctx.send(l.server[guild_l]['msg_error_4'])

                        elif STRING[1] == organizer.organizer.name:
                            path = c.GUILD_PATH['{}.ini'.format(organizer.organizer.name)].format(ctx.guild.id)
                            value = await origin.find_and_replace(STRING[4])
                            status = await ini_manager.update_data(STRING[2], STRING[3], value, path)
                            if status:
                                await ctx.send(l.server[guild_l]['msg_success_2'])
                            else:
                                await ctx.send(l.server[guild_l]['msg_error_4'])

                        elif STRING[1] == rsn_register.rsn_register.name:
                            path = c.GUILD_PATH['{}.ini'.format(rsn_register.rsn_register.name)].format(ctx.guild.id)
                            value = await origin.find_and_replace(STRING[4])
                            status = await ini_manager.update_data(STRING[2], STRING[3], value, path)
                            if status:
                                await ctx.send(l.server[guild_l]['msg_success_2'])
                            else:
                                await ctx.send(l.server[guild_l]['msg_error_4'])

                        elif STRING[1] == xp_tracker.xp_tracker.name:
                            path = c.GUILD_PATH['{}.ini'.format(xp_tracker.xp_tracker.name)].format(ctx.guild.id)
                            value = await origin.find_and_replace(STRING[4])
                            status = await ini_manager.update_data(STRING[2], STRING[3], value, path)
                            if status:
                                await ctx.send(l.server[guild_l]['msg_success_2'])
                            else:
                                await ctx.send(l.server[guild_l]['msg_error_4'])

                        elif STRING[1] == kc_tracker.kc_tracker.name:
                            path = c.GUILD_PATH['{}.ini'.format(kc_tracker.kc_tracker.name)].format(ctx.guild.id)
                            value = await origin.find_and_replace(STRING[4])
                            status = await ini_manager.update_data(STRING[2], STRING[3], value, path)
                            if status:
                                await ctx.send(l.server[guild_l]['msg_success_2'])
                            else:
                                await ctx.send(l.server[guild_l]['msg_error_4'])

                        elif STRING[1] == vote.vote.name:
                            path = c.GUILD_PATH['{}.ini'.format(vote.vote.name)].format(ctx.guild.id)
                            value = await origin.find_and_replace(STRING[4])
                            status = await ini_manager.update_data(STRING[2], STRING[3], value, path)
                            if status:
                                await ctx.send(l.server[guild_l]['msg_success_2'])
                            else:
                                await ctx.send(l.server[guild_l]['msg_error_4'])
                        else:
                            await ctx.send(l.server[guild_l]['msg_error_2'])
                    else:
                        await ctx.send(l.server[guild_l]['msg_1'])
                else:
                    await ctx.send(l.user_permissions[guild_l]['msg_restricted_1'])
                await ctx.message.delete()
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def config(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            if str(ctx.message.channel.type) == 'text':
                path = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
                target_keys = ['user_id', 'user_status']
                target_values = [ctx.author.id, c.USER_PERMISSIONS['dc_bank']]

                if ctx.author.id == c.CLIENT_ADMINISTRATION_ID or ctx.author.id == ctx.guild.owner.id or await permissions.get_user_permission(path, target_keys, target_values):
                    path1 = c.CLIENT_PATH['guild'] + str(ctx.guild.id) + c.CLIENT_JSON['server']
                    server_config = await json_manager.get_json(path1)

                    STATUS = False
                    MOD_STATUS = 0
                    TEXT = ''
                    TEXT2 = ''
                    TEXT3 = ''

                    STATUS_EMOTE = ['🟢', '🔴']

                    STRING = str(ctx.message.content).split(' ')
                    if len(STRING) >= 2:
                        if STRING[1] == 'channel':
                            if len(STRING) == 4:
                                for channel in c.DISCORD_CHANNEL[guild_l]:
                                    if STRING[2] == channel:
                                        STATUS = True

                                if STATUS:
                                    CHID = await origin.find_and_replace(STRING[3])
                                    if str(CHID).isdigit():
                                        CH = await discord_manager.get_channel(self.client, ctx.guild.id, CHID)
                                        if CH:
                                            path = c.CLIENT_PATH['guild'] + str(ctx.guild.id) + c.CLIENT_JSON['server']
                                            await json_manager.update_server_config(path, STRING[2], CH.id)
                                            await ctx.send(l.server[guild_l]['msg_success_1'].format(STRING[3]))
                                        else:
                                            await ctx.send(l.server[guild_l]['msg_error_1'].format(STRING[3]))
                                    else:
                                        await ctx.send(l.server[guild_l]['msg_error_1'].format(STRING[3]))
                                else:
                                    await ctx.send(l.server[guild_l]['msg_error_2'].format(STRING[3]))
                            else:
                                await ctx.send(l.server[guild_l]['msg_badformat_1'])

                        if STRING[1] == 'install':
                            if len(STRING) == 4:
                                if len(STRING[2]) == 2 and await server_timer.check_status_timezone(STRING[3]):
                                    path = c.CLIENT_JSON['guild']
                                    target_keys = ['language', 'time_line']
                                    target_values = [STRING[2], STRING[3]]
                                    await json_manager.update(path, 'guild_id', ctx.guild.id, target_keys, target_values)
                                    await ctx.send(l.server[guild_l]['msg_success_5'].format(STRING[3]))
                                else:
                                    await ctx.send(l.server[guild_l]['msg_badformat_2'])
                            else:
                                await ctx.send(l.server[guild_l]['msg_badformat_2'])

                        if STRING[1] == admin.admin.name:
                            path = c.GUILD_PATH['{}.ini'.format(admin.admin.name)].format(ctx.guild.id)
                            ini = await ini_manager.get_ini(path)
                            TEXT = l.server[guild_l]['server.config.admin_1'].format('<#{}>'.format(server_config['admin']) if server_config['admin'] else '', '<@&{}>'.format(ini['SECTION1']['BAN']) if ini['SECTION1']['BAN'] else '')
                            TEXT3 = l.server[guild_l]['server.config.active_deactive'].format(admin.admin.name, admin.admin.name)
                            MOD_STATUS = int(ini['STATUS']['STATUS'])
                        elif STRING[1] == dc_bank.dc_bank.name:
                            path = c.GUILD_PATH['{}.ini'.format(dc_bank.dc_bank.name)].format(ctx.guild.id)
                            ini = await ini_manager.get_ini(path)
                            TEXT = l.server[guild_l]['server.config.dc_bank_1'].format(
                                '<#{}>'.format(server_config['dc_bank']) if server_config['dc_bank'] else '',
                                '<#{}>'.format(server_config['sponsor']) if server_config['sponsor'] else '',
                                '<#{}>'.format(server_config['thanks']) if server_config['thanks'] else '',
                                '<@{}>'.format(ini['SECTION1']['ADMIN']) if ini['SECTION1']['ADMIN'] else l.server[guild_l]['configuration']['extra_1'],
                                '<@&{}>'.format(ini['SECTION2']['DISCORD_TOP_1']) if ini['SECTION2']['DISCORD_TOP_1'] else '',
                                '<@&{}>'.format(ini['SECTION2']['DISCORD_TOP_2']) if ini['SECTION2']['DISCORD_TOP_2'] else '',
                                '<@&{}>'.format(ini['SECTION2']['DISCORD_TOP_3']) if ini['SECTION2']['DISCORD_TOP_3'] else '',
                                '<@&{}>'.format(ini['SECTION2']['DISCORD_TOP_4']) if ini['SECTION2']['DISCORD_TOP_4'] else '',
                                '<@&{}>'.format(ini['SECTION2']['DISCORD_TOP_5']) if ini['SECTION2']['DISCORD_TOP_5'] else '')
                            TEXT2 = l.server[guild_l]['server.config.dc_bank_2'].format(
                                ini['SECTION3']['DISCORD_TOP_1_COUNT'], ini['SECTION3']['DISCORD_TOP_2_COUNT'],
                                ini['SECTION3']['DISCORD_TOP_3_COUNT'], ini['SECTION3']['DISCORD_TOP_4_COUNT'],
                                ini['SECTION3']['DISCORD_TOP_5_COUNT'], ini['CHANNEL_PERMISSIONS']['STATUS'],
                            )
                            TEXT3 = l.server[guild_l]['server.config.active_deactive'].format(dc_bank.dc_bank.name, dc_bank.dc_bank.name)
                            MOD_STATUS = int(ini['STATUS']['STATUS'])
                        elif STRING[1] == organizer.organizer.name:
                            path = c.GUILD_PATH['{}.ini'.format(organizer.organizer.name)].format(ctx.guild.id)
                            ini = await ini_manager.get_ini(path)
                            TEXT = l.server[guild_l]['server.config.organizer_1'].format(
                                '<#{}>'.format(server_config['events']) if server_config['events'] else '',
                                '<@&{}>'.format(ini['SECTION1']['EVENT_ROLE']) if ini['SECTION1']['EVENT_ROLE'] else '',
                                ini['CHANNEL_PERMISSIONS']['STATUS'],
                                ini['NOTIFICATION_TIMER']['HOURS'])
                            MOD_STATUS = int(ini['STATUS']['STATUS'])
                            TEXT3 = l.server[guild_l]['server.config.active_deactive'].format(organizer.organizer.name, organizer.organizer.name)
                        elif STRING[1] == self.name:
                            server_path = c.CLIENT_JSON['guild']
                            server_data = await json_manager.get_json(server_path)
                            server_holder = None

                            for data in server_data:
                                if data['guild_id'] == ctx.guild.id:
                                    server_holder = data

                            guild_current = await server_timer.get_current_time(region=await origin.get_region(ctx.guild.id))

                            TEXT = l.server[guild_l]['server.config.server_1'].format(
                                '<#{}>'.format(server_config['chat0']) if server_config['chat0'] else '',
                                '<#{}>'.format(server_config['chat1']) if server_config['chat1'] else '',
                                server_holder['language'],
                                '{} | {}'.format(guild_current.strftime('%H:%M'), server_holder['time_line'])
                            )
                            MOD_STATUS = 2
                        elif STRING[1] == rsn_register.rsn_register.name:
                            path = c.GUILD_PATH['{}.ini'.format(rsn_register.rsn_register.name)].format(ctx.guild.id)
                            ini = await ini_manager.get_ini(path)
                            TEXT = l.server[guild_l]['server.config.rsn_register_1'].format(
                                '<#{}>'.format(server_config['rsn']) if server_config['rsn'] else '',
                                '<@&{}>'.format(ini['SECTION1']['ROLE']) if ini['SECTION1']['ROLE'] else ''
                            )
                            MOD_STATUS = int(ini['STATUS']['STATUS'])
                            TEXT3 = l.server[guild_l]['server.config.active_deactive'].format(rsn_register.rsn_register.name, rsn_register.rsn_register.name)
                        elif STRING[1] == xp_tracker.xp_tracker.name:
                            path = c.GUILD_PATH['{}.ini'.format(xp_tracker.xp_tracker.name)].format(ctx.guild.id)
                            ini = await ini_manager.get_ini(path)
                            TEXT = l.server[guild_l]['server.config.xp_tracker_1'].format(
                                '<#{}>'.format(server_config['events']) if server_config['events'] else '',
                                '<#{}>'.format(server_config['xp_event']) if server_config['xp_event'] else '',
                                '<@&{}>'.format(ini['SECTION1']['EVENT_WINNER']) if ini['SECTION1']['EVENT_WINNER'] else '',
                                '<@&{}>'.format(ini['SECTION1']['EVENT_ROLE']) if ini['SECTION1']['EVENT_ROLE'] else '',
                                ini['CHANNEL_PERMISSIONS']['STATUS'],
                                ini['NOTIFICATION_TIMER']['HOURS'])
                            MOD_STATUS = int(ini['STATUS']['STATUS'])
                            TEXT3 = l.server[guild_l]['server.config.active_deactive'].format(xp_tracker.xp_tracker.name, xp_tracker.xp_tracker.name)
                        elif STRING[1] == kc_tracker.kc_tracker.name:
                            path = c.GUILD_PATH['{}.ini'.format(kc_tracker.kc_tracker.name)].format(ctx.guild.id)
                            ini = await ini_manager.get_ini(path)
                            TEXT = l.server[guild_l]['server.config.kc_tracker_1'].format(
                                '<#{}>'.format(server_config['events']) if server_config['events'] else '',
                                '<#{}>'.format(server_config['kc_event']) if server_config['kc_event'] else '',
                                '<@&{}>'.format(ini['SECTION1']['EVENT_WINNER']) if ini['SECTION1']['EVENT_WINNER'] else '',
                                '<@&{}>'.format(ini['SECTION1']['EVENT_ROLE']) if ini['SECTION1']['EVENT_ROLE'] else '',
                                ini['CHANNEL_PERMISSIONS']['STATUS'],
                                ini['NOTIFICATION_TIMER']['HOURS'])
                            MOD_STATUS = int(ini['STATUS']['STATUS'])
                            TEXT3 = l.server[guild_l]['server.config.active_deactive'].format(kc_tracker.kc_tracker.name, kc_tracker.kc_tracker.name)
                        elif STRING[1] == vote.vote.name:
                            path = c.GUILD_PATH['{}.ini'.format(vote.vote.name)].format(ctx.guild.id)
                            ini = await ini_manager.get_ini(path)
                            TEXT = l.server[guild_l]['server.config.vote_1'].format(
                                '<@&{}>'.format(ini['SECTION1']['RESTRICTION']) if ini['SECTION1']['RESTRICTION'] else '',
                                ini['SECTION2']['COUNT']
                            )
                            MOD_STATUS = int(ini['STATUS']['STATUS'])
                            TEXT3 = l.server[guild_l]['server.config.active_deactive'].format(vote.vote.name, vote.vote.name)

                        if TEXT:
                            win = discord.Embed(
                                color=discord.Color.gold(),
                            )
                            win.set_thumbnail(url=c.CLIENT_ICON)
                            win.set_author(name='{} - {}'.format(ctx.guild.name, c.CLIENT_NAME), icon_url=ctx.guild.icon_url)
                            win.add_field(name=l.server[guild_l]['configuration']['status_config_field_1'].format(STRING[1].capitalize()), value='{}'.format(TEXT), inline=False)
                            if TEXT2:
                                win.add_field(name='\u2800', value='{}'.format(TEXT2), inline=False)
                            if TEXT3:
                                win.add_field(name=l.server[guild_l]['configuration']['status_config_field_2'], value='{}'.format(TEXT3), inline=False)
                            win.add_field(name='\{} {}'.format(STATUS_EMOTE[0] if MOD_STATUS == 2 else STATUS_EMOTE[1], l.server[guild_l]['configuration']['active'] if MOD_STATUS == 2 else l.server[guild_l]['configuration']['deactive']), value='\u2800', inline=False)
                            await ctx.send(embed=win)
                        else:
                            if not STRING[1] == 'channel' and not STRING[1] == 'install':
                                await ctx.send(l.server[guild_l]['msg_error_3'].format(STRING[1]))
                    else:
                        await ctx.send(l.server[guild_l]['msg_1'])
                else:
                    await ctx.send(l.user_permissions[guild_l]['msg_restricted_1'])
                await ctx.message.delete()
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def server(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            if str(ctx.message.channel.type) == 'text':
                path1 = c.ORIGIN_PATH['embed.server.json']
                await origin.get_locale()
                LIST = ctx.guild.premium_subscribers
                MEMBERS = ''

                json_string = await json_manager.get_json(path1)
                new_json_string = {'data': []}

                if LIST:
                    for value in LIST:
                        MEMBERS += '{}\n'.format(value.mention)

                for key, value in json_string[guild_l]['server'].items():
                    if int(key) == 1:
                        new_json_string['data'].append({
                            'name{}'.format(key): str(value['name']).format(ctx.guild.name),
                            'value{}'.format(key): str(value['value']).format(
                                ctx.guild.owner.mention, str(ctx.guild.region).capitalize(),
                                locale.format_string('%d', int(ctx.guild.member_count), grouping=True),
                                ctx.guild.premium_subscription_count, ctx.guild.created_at.strftime('%y.%m.%d | %H:%M:%S')
                            )
                        })
                    else:
                        new_json_string['data'].append({
                            'name{}'.format(key): value['name'],
                            'value{}'.format(key): str(value['value']).format(MEMBERS if MEMBERS else l.server[guild_l]['configuration']['extra_1'])
                        })

                await embed_creator.create_embed(ctx, discord.Color.dark_orange(), False, ctx.guild.icon_url, ctx.guild.icon_url, l.server[guild_l]['embed_1'].format(ctx.guild.name), new_json_string['data'], False)
                await ctx.message.delete()
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def status(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            if str(ctx.message.channel.type) == 'text':
                path = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
                target_keys = ['user_id', 'user_status']
                target_values = [ctx.author.id, c.USER_PERMISSIONS['dc_bank']]

                if ctx.author.id == c.CLIENT_ADMINISTRATION_ID or ctx.author.id == ctx.guild.owner.id or await permissions.get_user_permission(path, target_keys, target_values):
                    path = c.CLIENT_PATH['guild'] + str(ctx.guild.id) + c.CLIENT_JSON['modules']
                    path1 = c.CLIENT_PATH['guild'] + str(ctx.guild.id) + c.CLIENT_JSON['server']
                    module_status = await json_manager.get_json(path)
                    server_config = await json_manager.get_json(path1)
                    SERVER = ''

                    STATUS = {
                        'active': '\🟢',
                        'deactive': '\🔴',
                        'not_configurated': '\🟡'
                    }

                    for channel, id in server_config.items():
                        SERVER += l.server[guild_l]['configuration']['status_server'].format(id, c.DISCORD_CHANNEL[guild_l].get(channel))

                    win = discord.Embed(
                        color=discord.Color.gold(),
                    )
                    win.set_author(name='{} - {}'.format(c.CLIENT_NAME, ctx.guild.name), icon_url=c.CLIENT_ICON)
                    win.set_thumbnail(url=c.CLIENT_ICON)
                    win.add_field(name=l.server[guild_l]['configuration']['status_server_field_1'], value='{}'.format(SERVER), inline=False)

                    win2 = discord.Embed(
                        color=discord.Color.gold(),
                    )
                    win2.set_author(name='{} - {}'.format(c.CLIENT_NAME, ctx.guild.name), icon_url=c.CLIENT_ICON)
                    win2.set_thumbnail(url=c.CLIENT_ICON)
                    win2.add_field(name=l.server[guild_l]['configuration']['status_server_field_2'], value=l.server[guild_l]['configuration']['status_server_value_2'].format(STATUS['active'], STATUS['not_configurated'], STATUS['deactive']), inline=False)
                    for dont_show_module in c.DONT_SHOW_MODULES:
                        for module, status in module_status.items():
                            SYS_STATUS = None
                            ini = None
                            if str(dont_show_module.replace('client.external.', '')) == module:
                                module_r = module

                                if not module_r == 'server':
                                    path = c.GUILD_PATH['{}.ini'.format(module_r)].format(ctx.guild.id)
                                    ini = await ini_manager.get_ini(path)

                                if status == 0:
                                    SYS_STATUS = STATUS['deactive']
                                elif status == 1:
                                    if ini:
                                        if int(ini['STATUS']['STATUS']) == 2:
                                            SYS_STATUS = STATUS['active']
                                        else:
                                            SYS_STATUS = STATUS['not_configurated']
                                    else:
                                        SYS_STATUS = STATUS['active']

                                modules = str(dont_show_module.replace('client.external.', ''))
                                win2.add_field(name='{} {}'.format(SYS_STATUS, modules), value='{}'.format('```.config {}```\n'.format(modules)), inline=False)
                    win2.add_field(name=l.server[guild_l]['configuration']['status_server_field_3'], value='{}'.format(l.server[guild_l]['configuration']['status_server_value_3']), inline=False)
                    await ctx.send(embed=win)
                    await ctx.send(embed=win2)
                else:
                    await ctx.send(l.user_permissions[guild_l]['msg_restricted_1'])
                await ctx.message.delete()
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def private(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            if str(ctx.message.channel.type) == 'text':
                path1 = c.ORIGIN_PATH['embed.server.json']
                json_string = await json_manager.get_json(path1)
                new_json_string = {'data': []}
                private_json_string = await json_manager.get_json(c.ORIGIN_PATH['private.json'])
                text = ''
                text2 = ''

                for data, data2 in private_json_string.items():
                    for command in data2['commands']:
                        text2 += '`{}` '.format(command)
                    text += (l.server[guild_l]['configuration']['private'].format(data, data2['owner'], text2))

                for key, value in json_string[guild_l]['private'].items():
                    if int(key) == 1:
                        new_json_string['data'].append({
                            'name{}'.format(key): str(value['name']).format(c.CLIENT_NAME),
                            'value{}'.format(key): str(value['value']).format(text)
                        })
                    else:
                        new_json_string['data'].append({
                            'name{}'.format(key): str(value['name']),
                            'value{}'.format(key): str(value['value'])
                        })

                await embed_creator.create_embed(ctx, discord.Color.gold(), False, ctx.guild.icon_url, ctx.guild.icon_url, l.server[guild_l]['embed_2'].format(c.CLIENT_NAME), new_json_string['data'], False)
                await ctx.message.delete()
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

def setup(client):
    client.add_cog(server(client))