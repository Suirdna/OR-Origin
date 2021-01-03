from client import exception, embed_creator, console_interface, discord_manager, ini_manager, json_manager, origin, server_timer, logger
from client.stream import datastream_xp, datastream_kc
from client.external import admin, dc_bank, organizer, vote, xp_tracker, kc_tracker
from client.config import config as c, language as l
from client.external.hiscores import hiscores_xp, hiscores_kc
from discord.ext import commands, tasks
import discord, locale, asyncio

class preprocessor(commands.Cog):
    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    name = 'preprocessor'

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    @staticmethod
    async def notificator(channel, message):
        try:
            await channel.send('{}'.format(message))
        except Exception as error:
            await exception.error(error)

    async def time_saver(self, guild_id, year, month, day, hour, types):
        try:
            if types == 'organizer':
                self.GUILD_EVENT_NOTIFICATION_TIMER.append({'guild': guild_id, 'year': year, 'month': month, 'day': day, 'hour': hour})
            if types == 'xp_tracker':
                self.GUILD_XP_EVENT_NOTIFICATION_TIMER.append({'guild': guild_id, 'year': year, 'month': month, 'day': day, 'hour': hour})
            if types == 'kc_tracker':
                self.GUILD_KC_EVENT_NOTIFICATION_TIMER.append({'guild': guild_id, 'year': year, 'month': month, 'day': day, 'hour': hour})
            if types == 'xp_tracker_auto_xp':
                self.GUILD_XP_EVENT_TIMER.append({'guild': guild_id, 'year': year, 'month': month, 'day': day, 'hour': hour})
            if types == 'kc_tracker_auto_kc':
                self.GUILD_KC_EVENT_TIMER.append({'guild': guild_id, 'year': year, 'month': month, 'day': day, 'hour': hour})
        except Exception as error:
            await exception.error(error)

    async def votemute_delete_mute(self, GUILD, MEMBER, ROLE, server_config, path):
        try:
            guild_l = await origin.get_language(GUILD)
            STATUS = False
            MEMBER_LIST = ROLE.members if hasattr(ROLE, 'members') else None

            if MEMBER_LIST:
                for index, member in enumerate(MEMBER_LIST):
                    if member and MEMBER:
                        if int(member.id) == int(MEMBER.id):
                            STATUS = True

            if STATUS and MEMBER_LIST:
                if MEMBER:
                    await MEMBER.remove_roles(ROLE, reason=c.DISCORD_MESSAGES['unmute_reason'], atomic=True)
                    await json_manager.delete(path, 'user_id', MEMBER.id)
                    CHANNEL = await discord_manager.get_channel(self.client, GUILD, server_config['chat0'])
                    await CHANNEL.send(l.vote[guild_l]['msg_2'].format(MEMBER.mention))
        except Exception as error:
            await exception.error(error)

    @staticmethod
    async def votemute_rejoin_check(MEMBER, ROLE):
        try:
            STATUS = False
            MEMBER_LIST = ROLE.members if hasattr(ROLE, 'members') else None

            if MEMBER_LIST:
                for index, member in enumerate(MEMBER_LIST):
                    if member and MEMBER:
                        if int(member.id) == int(MEMBER.id):
                            STATUS = True

            if not STATUS and MEMBER_LIST:
                if MEMBER:
                    await MEMBER.add_roles(ROLE, reason=c.DISCORD_MESSAGES['mute_reason'], atomic=True)
        except Exception as error:
            await exception.error(error)

    async def votemute_check_mute_2(self, current, value, guild, role, server_config, path5):
        try:
            if current.year >= value['year'] and current.month >= value['month'] and current.day >= value['day'] and current.hour >= value['hour'] and current.minute >= value['minute']:
                MEMBER = guild.get_member(value['user_id'])
                await asyncio.gather(self.votemute_delete_mute(guild.id, MEMBER, role, server_config, path5))
            else:
                MEMBER = guild.get_member(value['user_id'])
                await asyncio.gather(self.votemute_rejoin_check(MEMBER, role))
        except Exception as error:
            await exception.error(error)

    @staticmethod
    async def votemute_check_loop_1(current, value, guild, server_config, vote_count, path5, role, path3):
        try:
            guild_l = await origin.get_language(guild.id)
            guild_t = await origin.get_region(guild.id)
            if current.year >= value['year'] and current.month >= value['month'] and current.day >= value['day'] and current.hour >= value['hour'] and current.minute >= value['minute']:
                CHANNEL = guild.get_channel(server_config['chat0'])
                user = guild.get_member(value['user_id'])
                if value['vote'] >= int(vote_count):
                    guild_current = await server_timer.get_timedelta(hours=1, region=guild_t)
                    json_string = {'user_id': user.id, 'user_username': user.mention, 'year': guild_current.year, 'month': guild_current.month, 'day': guild_current.day, 'hour': guild_current.hour, 'minute': current.minute}

                    await json_manager.create(path5, json_string)
                    await user.add_roles(role, reason=c.DISCORD_MESSAGES['mute_reason'], atomic=True)
                    await CHANNEL.send(l.vote[guild_l]['msg_3'].format(user.mention, guild_current.month, guild_current.day, guild_current.hour, guild_current.minute, l.vote[guild_l]['msg_4'].format(server_config['chat1'] if server_config['chat1'] else '')))
                else:
                    await CHANNEL.send(l.vote[guild_l]['msg_5'].format(user.mention))
                await json_manager.delete(path3, 'user_id', user.id)
        except Exception as error:
            await exception.error(error)

    async def votemute_check_loop(self):
        try:
            path1 = c.CLIENT_PATH['guild']
            list_of_guilds = await discord_manager.get_servers(self.client, path1)

            for guild in list_of_guilds:
                if guild and await discord_manager.get_server(self.client, guild.id):
                    path3 = c.GUILD_PATH['{}.ini'.format(vote.vote.name)].format(guild.id)
                    ini2 = await ini_manager.get_ini(path3)
                    if int(ini2['STATUS']['STATUS']) == 2:
                        guild_t = await origin.get_region(guild.id)
                        guild_current = await server_timer.get_current_time(guild_t)
                        path2 = c.GUILD_PATH['{}.ini'.format(admin.admin.name)].format(guild.id)
                        ini = await ini_manager.get_ini(path2)
                        ban_role = ini['SECTION1']['BAN']
                        vote_count = ini2['SECTION2']['COUNT']
                        role = None

                        if ban_role.isdigit():
                            role = guild.get_role(int(ban_role))

                        if role:
                            path3 = c.GUILD_PATH['voteban.json'].format(guild.id)
                            path4 = c.CLIENT_PATH['guild'] + str(guild.id) + c.CLIENT_JSON['server']
                            path5 = c.GUILD_PATH['muted_member.json'].format(guild.id)

                            DATA1 = await json_manager.get_json(path3)
                            server_config = await json_manager.get_json(path4)

                            if DATA1:
                                for value in DATA1:
                                    await asyncio.gather(self.votemute_check_loop_1(guild_current, value, guild, server_config, vote_count, path5, role, path3))

                            DATA2 = await json_manager.get_json(path5)

                            for value in DATA2:
                                await asyncio.gather(self.votemute_check_mute_2(guild_current, value, guild, role, server_config, path5))
        except Exception as error:
            await exception.error(error)

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ ADMIN.PY | VOTEMUTE.PY #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    @tasks.loop(seconds=30)
    async def update_votemute(self):
        await self.votemute_check_loop()

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ ADMIN.PY | VOTEMUTE.PY #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    async def dc_bank_check_loop_1(self, guild):
        try:
            guild_l = await origin.get_language(guild.id)
            path2 = c.GUILD_PATH['bank.json'].format(guild.id)
            path3 = c.GUILD_PATH['{}.ini'.format(dc_bank.dc_bank.name)].format(guild.id)
            path4 = c.CLIENT_PATH['guild'] + str(guild.id) + c.CLIENT_JSON['server']

            server_config = await json_manager.get_json(path4)
            DATA = await json_manager.get_data(path2)

            await origin.get_locale()

            max_sum = 0
            count = 0
            count_t = 0
            TEXT_DESIGN = []
            TEXT_DATA = ''

            TEXT_DESIGN.append(l.dc_bank[guild_l]['configuration']['line'])
            TEXT_DESIGN.append(l.dc_bank[guild_l]['configuration']['title'].format(guild.name))
            TEXT_DESIGN.append(l.dc_bank[guild_l]['configuration']['line'])

            def get_id(INFO):
                return int(INFO.get('donate'))

            DATA.sort(key=get_id, reverse=True)
            CHANNEL1 = await discord_manager.get_channel(self.client, guild.id, server_config['sponsor'])

            if CHANNEL1:
                async for message in CHANNEL1.history(limit=100):
                    await message.delete()

                for data in DATA:
                    if data['donate'] >= 1000000:
                        user = self.client.get_user(data['user_id'])
                        if user:
                            username = user.display_name

                            if count == 0:
                                TEXT_DESIGN.append(':first_place: {}'.format(l.dc_bank[guild_l]['configuration']['top_gp'].format(username, self.COINS2, locale.format_string('%d', int(data['donate']), grouping=True))))
                            elif count == 1:
                                TEXT_DESIGN.append(':second_place: {}'.format(l.dc_bank[guild_l]['configuration']['top_gp'].format(username, self.COINS2, locale.format_string('%d', int(data['donate']), grouping=True))))
                            elif count == 2:
                                TEXT_DESIGN.append(':third_place: {}'.format(l.dc_bank[guild_l]['configuration']['top_gp'].format(username, self.COINS2, locale.format_string('%d', int(data['donate']), grouping=True))))
                            else:
                                TEXT_DESIGN.append(l.dc_bank[guild_l]['configuration']['top_gp'].format(username, self.COINS2, locale.format_string('%d', int(data['donate']), grouping=True)))
                            count += 1
                        max_sum = max_sum + data['donate']

                TEXT_DESIGN.append(l.dc_bank[guild_l]['configuration']['line'])
                TEXT_DESIGN.append(l.dc_bank[guild_l]['configuration']['total_sponsor'].format(guild.name))
                TEXT_DESIGN.append(l.dc_bank[guild_l]['configuration']['line'])
                TEXT_DESIGN.append(l.dc_bank[guild_l]['configuration']['total_gp'].format(self.COINS1, locale.format_string('%d', max_sum, grouping=True)))

                for text_data in TEXT_DESIGN:
                    TEXT_DATA += '{}\n'.format(text_data)
                    count_t += 1
                    if count_t >= 10:
                        await CHANNEL1.send(TEXT_DATA)
                        TEXT_DATA = ''
                        count_t = 0

                if TEXT_DATA:
                    await CHANNEL1.send(TEXT_DATA)
        except Exception as error:
            await exception.error(error)

    async def dc_bank_check_loop(self):
        try:
            path1 = c.CLIENT_PATH['guild']
            list_of_guilds = await discord_manager.get_servers(self.client, path1)
            for guild in list_of_guilds:
                if guild and await discord_manager.get_server(self.client, guild.id):
                    path2 = c.GUILD_PATH['{}.ini'.format(dc_bank.dc_bank.name)].format(guild.id)
                    ini = await ini_manager.get_ini(path2)
                    if int(ini['STATUS']['STATUS']) == 2:
                        await asyncio.gather(self.dc_bank_check_loop_1(guild))
        except Exception as error:
            await exception.error(error)

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ DC_BANK.PY #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    @tasks.loop(hours=24)
    async def update_dc_bank(self):
        await self.dc_bank_check_loop()

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ DC_BANK.PY #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    EVENT_CHECK_TIMER_ORGANIZER = 0
    GUILD_EVENT_NOTIFICATION_TIMER = []

    async def organizer_check_loop_1(self, guild, current):
        try:
            guild_l = await origin.get_language(guild.id)
            path2 = c.GUILD_PATH['{}.ini'.format(organizer.organizer.name)].format(guild.id)
            path3 = c.CLIENT_PATH['guild'] + str(guild.id) + c.CLIENT_JSON['server']

            server_config = await json_manager.get_json(path3)
            EVENT_ROLE = await ini_manager.get_data('SECTION1', 'EVENT_ROLE', path2)

            CHANNEL1 = await discord_manager.get_channel(self.client, guild.id, server_config['chat0'])
            CHANNEL2 = await discord_manager.get_channel(self.client, guild.id, server_config['chat1'])
            path4 = c.GUILD_PATH['event.json'].format(guild.id)
            DATA = await json_manager.get_data(path4)

            ini = await ini_manager.get_ini(path2)
            CHANNEL_PERMISSIONS = int(ini['CHANNEL_PERMISSIONS']['STATUS'])

            if DATA:
                for value in DATA:
                    USER = await discord_manager.get_member(self.client, guild.id, value['user_id'])

                    if current.month >= int(value['date_start'][:2]):
                        if current.day >= int(value['date_start'][3:]):
                            if ((current.month > int(value['date_start'][:2]) and current.day >= int(value['date_start'][3:])) or current.hour >= value['time_start']) and value['type'] == 0 and value['status'] == 0:
                                await json_manager.update(path4, 'id', value['id'], 'status', 1)
                                client_message = 'Guild id: {} | Event: {} | Status: {}'.format(guild.id, value['event_name'], 'Started')
                                await console_interface.console_message('START_PVM_EVENT', client_message)
                                if CHANNEL_PERMISSIONS == 1:
                                    if CHANNEL1:
                                        await CHANNEL1.send(l.organizer[guild_l]['msg_post_1'].format(EVENT_ROLE, value['event_name'], server_config['events']))
                                if CHANNEL_PERMISSIONS == 0:
                                    if CHANNEL2:
                                        await CHANNEL2.send(l.organizer[guild_l]['msg_post_1'].format(EVENT_ROLE, value['event_name'], server_config['events']))
                                continue

                    if current.month >= int(value['date_start'][:2]):
                        if current.day >= int(value['date_start'][3:]):
                            if ((current.month > int(value['date_start'][:2]) and current.day >= int(value['date_start'][3:])) or current.hour >= value['time_start']) and value['type'] == 0 and value['status'] == 0:
                                client_message = 'Guild id: {} | Event: {} | Status: {}'.format(guild.id, value['event_name'], 'In Last Hour progress')
                                await console_interface.console_message('START_PVM_EVENT', client_message)
                                if CHANNEL_PERMISSIONS == 1:
                                    if CHANNEL1:
                                        await CHANNEL1.send(l.organizer[guild_l]['msg_post_2'].format(EVENT_ROLE, USER.name if USER else 'Administrator', value['event_name'], server_config['events']))
                                if CHANNEL_PERMISSIONS == 0:
                                    if CHANNEL2:
                                        await CHANNEL2.send(l.organizer[guild_l]['msg_post_2'].format(EVENT_ROLE, USER.name if USER else 'Administrator', value['event_name'], server_config['events']))
                                continue

                    if current.month >= int(value['date_start'][:2]):
                        if current.day >= int(value['date_start'][3:]):
                            if value['type'] == 0 and value['status'] == 0:
                                guild_t = await origin.get_region(guild.id)
                                client_message = 'Guild id: {} | Event: {} | Status: {}'.format(guild.id, value['event_name'], 'In Registration progress')
                                await console_interface.console_message('START_PVM_EVENT', client_message)
                                message = l.organizer[guild_l]['msg_post_3'].format(value['time_start'], USER.name if USER else 'Administrator', value['event_name'], server_config['events'])
                                new_time = await server_timer.get_timedelta(hours=int(ini['NOTIFICATION_TIMER']['HOURS']), region=guild_t)

                                if not self.GUILD_EVENT_NOTIFICATION_TIMER:
                                    await self.time_saver(guild.id, new_time.year, new_time.month, new_time.day, new_time.hour, 'organizer')
                                else:
                                    STATUS_A = False
                                    for index, data in enumerate(self.GUILD_EVENT_NOTIFICATION_TIMER):
                                        if data['guild'] == guild.id:
                                            if current.year >= data['year'] and current.month >= data['month'] and current.day >= data['day'] and current.hour >= data['hour']:
                                                if CHANNEL_PERMISSIONS == 1:
                                                    if CHANNEL1:
                                                        await self.notificator(CHANNEL1, message)
                                                if CHANNEL_PERMISSIONS == 0:
                                                    if CHANNEL2:
                                                        await self.notificator(CHANNEL2, message)
                                                self.GUILD_EVENT_NOTIFICATION_TIMER.pop(index)
                                                await self.time_saver(guild.id, new_time.year, new_time.month, new_time.day, new_time.hour, 'organizer')
                                            STATUS_A = True
                                            continue
                                    if not STATUS_A:
                                        await self.time_saver(guild.id, new_time.year, new_time.month, new_time.day, new_time.hour, 'organizer')

        except Exception as error:
            await exception.error(error)

    async def organizer_check_loop(self):
        try:
            server_current = await server_timer.get_server_current_time()

            if self.EVENT_CHECK_TIMER_ORGANIZER != server_current.hour:
                path1 = c.CLIENT_PATH['guild']
                list_of_guilds = await discord_manager.get_servers(self.client, path1)

                for guild in list_of_guilds:
                    if guild and await discord_manager.get_server(self.client, guild.id):
                        guild_t = await origin.get_region(guild.id)
                        path2 = c.GUILD_PATH['{}.ini'.format(organizer.organizer.name)].format(guild.id)
                        ini = await ini_manager.get_ini(path2)
                        guild_current = await server_timer.get_current_time(guild_t)
                        if int(ini['STATUS']['STATUS']) == 2:
                            await asyncio.gather(self.organizer_check_loop_1(guild, guild_current))
                self.EVENT_CHECK_TIMER_ORGANIZER = server_current.hour
        except Exception as error:
            await exception.error(error)

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ ORGANIZER.PY #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬
    
    @tasks.loop(minutes=1)
    async def update_organizer(self):
        await self.organizer_check_loop()

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ ORGANIZER.PY #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    EVENT_CHECK_TIMER_XP_TRACKER = 0
    GUILD_XP_EVENT_NOTIFICATION_TIMER = []
    GUILD_XP_EVENT_TIMER = []

    async def autostats_xp(self, guild):
        try:
            AUTO_NOTIFICATION_STATUS = False
            current = await server_timer.get_server_current_time()

            if not self.GUILD_XP_EVENT_TIMER:
                await self.time_saver(guild.id, current.year, current.month, current.day, current.hour+1, 'xp_tracker_auto_xp')
                AUTO_NOTIFICATION_STATUS = False
            else:
                STATUS_XX = False
                for index, data in enumerate(self.GUILD_XP_EVENT_TIMER):
                    if data['guild'] == guild.id:
                        if current.year >= data['year'] and current.month >= data['month'] and current.day >= data['day'] and current.hour >= data['hour']:
                            self.GUILD_XP_EVENT_TIMER.pop(index)
                            await self.time_saver(guild.id, current.year, current.month, current.day, current.hour+1, 'xp_tracker_auto_xp')
                            AUTO_NOTIFICATION_STATUS = False
                        STATUS_XX = True
                        continue
                if not STATUS_XX:
                    await self.time_saver(guild.id, current.year, current.month, current.day, current.hour+1, 'xp_tracker_auto_xp')
                    AUTO_NOTIFICATION_STATUS = False

            if not AUTO_NOTIFICATION_STATUS:
                guild_l = await origin.get_language(guild.id)
                path1 = c.GUILD_PATH['{}.ini'.format(xp_tracker.xp_tracker.name)].format(guild.id)
                path2 = c.GUILD_PATH['event.json'].format(guild.id)
                path3 = c.GUILD_PATH['tracker.json'].format(guild.id)
                path4 = c.CLIENT_PATH['guild'] + str(guild.id) + c.CLIENT_JSON['server']
                path5 = c.ORIGIN_PATH['embed.tracker.json']

                ini = await ini_manager.get_ini(path1)
                server_config = await json_manager.get_json(path4)
                LIST1 = self.XP_ICON
                LIST2 = self.XP_PRE

                IMAGE = None
                IMAGE2 = self.XP_INFO_ICON

                WINNER_ROLE = ini['SECTION1']['EVENT_WINNER']
                EVENT_NAME = None
                EMBED_TEXT = ''

                EVENT_COUNT = 0
                ENDED_EVENT_COUNT = 0

                TEMP_DATA = await json_manager.get_data(path2)
                DATA2 = await json_manager.get_data(path3)

                DATA = []
                DATA3 = []

                CHANNEL = await discord_manager.get_channel(self.client, guild.id, server_config['xp_event'])
                await origin.get_locale()

                if CHANNEL:
                    async for message in CHANNEL.history(limit=10):
                        if message:
                            await message.delete()

                for value in TEMP_DATA:
                    if value['type'] == 1 or value['type'] == 2:
                        DATA.append(value)
                        EVENT_COUNT += 1

                def get_id(INFO):
                    return INFO.get('sum')

                if DATA:
                    for data1 in DATA:
                        if DATA2:
                            for data2 in DATA2:
                                for key, value in data2.items():
                                    if key == data1['event_name']:
                                        sum = data2['{}_current'.format(key)] - data2[key]
                                        DATA3.append({'user_id': data2['user_id'], 'user_username': data2['user_username'], 'user_rsn': data2['user_rsn'], 'sum': sum})

                                        if data1['type'] == 1:
                                            EVENT_NAME = '{} [ S ]'.format(str(data1['event_name']).capitalize())

                                        if data1['type'] == 2:
                                            EVENT_NAME = '{} [ R ]'.format(str(data1['event_name']).capitalize())

                                        for index, value3 in enumerate(LIST2):
                                            if str(value3) == str(key):
                                                IMAGE = LIST1[index]

                            DATA3.sort(key=get_id, reverse=True)

                            json_string = await json_manager.get_json(path5)
                            new_json_string = {'data': []}

                            STRING = ''
                            SUM = 0

                            for key, value in json_string[guild_l]['xp_tracker']['stats'].items():
                                if DATA3:
                                    if int(key) == 1:
                                        for index, data in enumerate(DATA3):
                                            index = index + 1
                                            if index <= 10:
                                                if index == 1:
                                                    title = ':first_place: {}'.format(l.DISCORD_TOP[guild_l][index - 1])
                                                elif index == 2:
                                                    title = ':second_place: {}'.format(l.DISCORD_TOP[guild_l][index - 1])
                                                elif index == 3:
                                                    title = ':third_place: {}'.format(l.DISCORD_TOP[guild_l][index - 1])
                                                else:
                                                    title = '{}'.format(l.DISCORD_TOP[guild_l][index - 1])

                                                STRING += l.xp_tracker[guild_l]['configuration']['current_xp'].format(title, data['user_username'], data['user_rsn'], locale.format_string('%d', data['sum'], grouping=True))
                                                SUM += data['sum']

                                                if data1['status'] == 2 and data1['prize_count'] >= index and data1['win_message'] == 0:
                                                    member = await discord_manager.get_member(self.client, guild.id, data['user_id'])
                                                    role = await discord_manager.get_role(self.client, guild.id, int(WINNER_ROLE))

                                                    if index == 1 and member and role:
                                                        await member.add_roles(role, reason='{}'.format(c.DISCORD_MESSAGES['xp_event_winner']), atomic=True)
                                                        EMBED_TEXT += '{}\n'.format(l.xp_tracker[guild_l]['extra_1'].format(EVENT_NAME.capitalize(), member.mention if member else data['user_id']))
                                                    elif int(data1['prize_count']) >= index and member:
                                                        EMBED_TEXT += '{}\n'.format(l.xp_tracker[guild_l]['extra_2'].format(EVENT_NAME.capitalize(), member.mention if member else data['user_id']))
                                                    else:
                                                        EMBED_TEXT += '{}\n'.format(l.xp_tracker[guild_l]['msg_error_7'].format(EVENT_NAME.capitalize(), data['user_id'], data['user_rsn']))

                                                    await json_manager.update(path2, 'id', data1['id'], 'win_message', 1)

                                        STRING += l.xp_tracker[guild_l]['configuration']['total_xp'].format(locale.format_string('%d', SUM, grouping=True))
                                        new_json_string['data'].append({
                                            'name{}'.format(key): value['name'].format('\u200D'),
                                            'value{}'.format(key): str(value['value']).format(STRING)
                                        })
                                    else:
                                        STRING += l.xp_tracker[guild_l]['configuration']['total_xp'].format(locale.format_string('%d', SUM, grouping=True))
                                        new_json_string['data'].append({
                                            'name{}'.format(key): value['name'],
                                            'value{}'.format(key): str(value['value']).format(guild.name)
                                        })

                            await asyncio.gather(embed_creator.create_embed(guild.id, discord.Color.dark_green(), False, guild.icon_url, IMAGE, l.xp_tracker[guild_l]['embed_3'].format(guild.name, EVENT_NAME), new_json_string['data'], False, False, CHANNEL))
                            DATA3.clear()

                        if data1['type'] >= 1 and data1['status'] == 2:
                            ENDED_EVENT_COUNT += 1

                    if EMBED_TEXT != '':
                        embed_json_string = {'data': [
                            {
                                'name1': '{}'.format(l.xp_tracker[guild_l]['embed_4'].format(guild.name)),
                                'value1': EMBED_TEXT
                            }
                        ]}

                        CHANNEL2 = await discord_manager.get_channel(self.client, guild.id, server_config['admin'])

                        if CHANNEL2:
                            await asyncio.gather(embed_creator.create_embed(guild.id, discord.Color.dark_green(), False, guild.icon_url, IMAGE, l.xp_tracker[guild_l]['embed_4'].format(guild.name, EVENT_NAME), embed_json_string['data'], False, False, CHANNEL2))

                    json_string2 = await json_manager.get_json(path5)
                    new_json_string1 = {'data': []}

                    for key, value in json_string2[guild_l]['xp_tracker']['autostats'].items():
                        if int(key) == 1:
                            new_json_string1['data'].append({
                                'name{}'.format(key): value['name'],
                                'value{}'.format(key): value['value']
                            })
                        else:
                            new_json_string1['data'].append({
                                'name{}'.format(key): value['name'],
                                'value{}'.format(key): value['value']
                            })

                    await asyncio.gather(embed_creator.create_embed(guild.id, discord.Color.dark_green(), False, guild.icon_url, IMAGE2, l.xp_tracker[guild_l]['embed_2'].format(guild.name), new_json_string1['data'], False, False, CHANNEL))
        except Exception as error:
            await exception.error(error)

    async def start_xp_event(self, event_name, date_start, time_start, guild_id):
        try:
            if guild_id:
                guild_t = await origin.get_region(guild_id)
                path1 = c.GUILD_PATH['tracker.json'].format(guild_id)
                DATA = await json_manager.get_data(path1)

                guild_current = await server_timer.get_current_time(guild_t)
                COUNTER = 0

                if date_start == guild_current.strftime('%m.%d') and time_start == guild_current.hour:
                    if DATA:
                        for data in DATA:
                            CHECK = True
                            USERNAME = data['user_rsn']
                            USERNAME = USERNAME.replace(' ', '%20')
                            while CHECK:
                                USER = hiscores_xp.Hiscores(USERNAME, 'N')
                                if hasattr(USER, 'stats'):
                                    CHECK = False
                                    target_keys = [event_name, '{}_current'.format(event_name)]
                                    target_values = [USER.stats[event_name]['experience'], USER.stats[event_name]['experience']]
                                    await json_manager.update(path1, 'user_rsn', data['user_rsn'], target_keys, target_values)

                                    client_message = 'Guild id: {} | Guild time: {} | Event: {} | Rsn: {} | Registration XP: {} | Status: {}'.format(guild_id, guild_current, event_name, data['user_rsn'], USER.stats[str(event_name)]['experience'], 'XP event start reset')
                                    await console_interface.console_message('START_XP_EVENT_RESET', client_message)
                                    await logger.log_event(guild_id, 'xp_tracker', c.CLIENT_MESSAGES['xp_tracker_reset'], client_message)
                                else:
                                    if COUNTER >= 10:
                                        CHECK = False
                                        COUNTER = 0
                                    else:
                                        COUNTER += 1

                guild = await discord_manager.get_server(self.client, guild_id)
                await asyncio.gather(self.autostats_xp(guild))
        except Exception as error:
            await exception.error(error)

    async def end_xp_event(self, event_name, date_end, time_end, guild_id, mode):
        try:
            if guild_id:
                guild_t = await origin.get_region(guild_id)
                path1 = c.GUILD_PATH['tracker.json'].format(guild_id)
                DATA = await json_manager.get_data(path1)

                guild_current = await server_timer.get_current_time(guild_t)
                STATUS = False
                COUNTER = 0

                if mode == c.MODE_NAME['std']:
                    if date_end == guild_current.strftime('%m.%d') and time_end == guild_current.hour:
                        STATUS = True
                elif mode == c.MODE_NAME['rush']:
                    STATUS = True

                if STATUS:
                    if DATA:
                        for data in DATA:
                            CHECK = True
                            USERNAME = data['user_rsn']
                            USERNAME = USERNAME.replace(' ', '%20')
                            while CHECK:
                                USER = hiscores_xp.Hiscores(USERNAME, 'N')
                                if hasattr(USER, 'stats'):
                                    CHECK = False
                                    target_keys = ['{}_current'.format(event_name)]
                                    target_values = [USER.stats[event_name]['experience']]
                                    await json_manager.update(path1, 'user_rsn', data['user_rsn'], target_keys, target_values)

                                    client_message = 'Guild id: {} | Guild time: {} | Event: {} | Rsn: {} | Registration XP: {} | Current XP: {} | Status: {}'.format(guild_id, guild_current.strftime('%H:%M'), event_name, data['user_rsn'], data[event_name], data['{}_current'.format(event_name)], 'Last XP update')
                                    await console_interface.console_message('START_LAST_XP_EVENT_CHECK', client_message)
                                    await logger.log_event(guild_id, 'xp_tracker', c.CLIENT_MESSAGES['xp_tracker_update'], client_message)
                                else:
                                    if COUNTER >= 10:
                                        CHECK = False
                                        COUNTER = 0
                                    else:
                                        COUNTER += 1

                guild = await discord_manager.get_server(self.client, guild_id)
                await asyncio.gather(self.autostats_xp(guild))
        except Exception as error:
            await exception.error(error)

    async def xp_tracker_check_loop_1(self, guild, current):
        try:
            guild_l = await origin.get_language(guild.id)
            guild_t = await origin.get_region(guild.id)
            path = c.CLIENT_PATH['guild'] + str(guild.id) + c.CLIENT_JSON['server']
            path2 = c.GUILD_PATH['event.json'].format(guild.id)
            server_config = await json_manager.get_json(path)
            CHANNEL1 = await discord_manager.get_channel(self.client, guild.id, server_config['chat0'])
            CHANNEL2 = await discord_manager.get_channel(self.client, guild.id, server_config['chat1'])

            path1 = c.GUILD_PATH['{}.ini'.format(xp_tracker.xp_tracker.name)].format(guild.id)
            ini = await ini_manager.get_ini(path1)
            CHANNEL_PERMISSIONS = int(ini['CHANNEL_PERMISSIONS']['STATUS'])

            LIST1 = await json_manager.get_data(path2)
            if LIST1:
                for value in LIST1:
                    if value['type'] == 1 or value['type'] == 2:
                        if current.month >= int(value['date_start'][:2]):
                            if current.day >= int(value['date_start'][3:]):
                                if current.hour >= value['time_start'] and value['status'] == 0:
                                    await json_manager.update(path2, 'id', value['id'], 'status', 1)
                                    await asyncio.gather(self.start_xp_event(value['event_name'], value['date_start'], value['time_start'], guild.id))
                                    client_message = 'Guild id: {} | Guild time: {} | Event: {} | Mode: {} | Status: {}'.format(guild.id, current.strftime('%H:%M'), value['event_name'], c.MODE_NAME['std'] if value['type'] == 1 else c.MODE_NAME['rush'], 'Started')
                                    await console_interface.console_message('START_XP_EVENT', client_message)

                                    if CHANNEL_PERMISSIONS == 1:
                                        if CHANNEL1:
                                            await CHANNEL1.send(l.xp_tracker[guild_l]['msg_post_4'].format(str(value['event_name']).capitalize()))
                                    if CHANNEL2:
                                        await CHANNEL2.send(l.xp_tracker[guild_l]['msg_post_4'].format(str(value['event_name']).capitalize()))
                                    continue

                        if value['type'] == 1 and value['status'] == 1:
                            if current.month >= int(value['date_end'][:2]):
                                if current.day >= int(value['date_end'][3:]):
                                    if current.hour >= value['time_end']:
                                        await json_manager.update(path2, 'id', value['id'], 'status', 2)
                                        await asyncio.gather(self.end_xp_event(value['event_name'], value['date_end'], value['time_end'], guild.id, c.MODE_NAME['std']))
                                        client_message = 'Guild id: {} | Guild time: {} | Event: {} | Mode: {} | Status: {}'.format(guild.id, current.strftime('%H:%M'), value['event_name'], c.MODE_NAME['std'], 'Ended')
                                        await console_interface.console_message('END_XP_EVENT', client_message)

                                        if CHANNEL_PERMISSIONS == 1:
                                            if CHANNEL1:
                                                await CHANNEL1.send(l.xp_tracker[guild_l]['msg_post_5'].format(str(value['event_name']).capitalize(), server_config['xp_event']))
                                        if CHANNEL2:
                                            await CHANNEL2.send(l.xp_tracker[guild_l]['msg_post_5'].format(str(value['event_name']).capitalize(), server_config['xp_event']))
                                        continue
                        elif value['type'] == 2 and value['status'] == 1:
                            path3 = c.GUILD_PATH['tracker.json'].format(guild.id)
                            player_data = await json_manager.get_data(path3)

                            COUNTER = 0

                            for player_xp in player_data:
                                if player_xp['{}_current'.format(value['event_name'])] - player_xp['{}'.format(value['event_name'])] >= value['xp_target']:
                                    COUNTER += 1

                            if COUNTER >= value['prize_count']:
                                await json_manager.update(path2, 'id', value['id'], 'status', 2)
                                await asyncio.gather(self.end_xp_event(value['event_name'], value['date_end'], value['time_end'], guild.id, c.MODE_NAME['rush']))
                                client_message = 'Guild id: {} | Guild time: {} | Event: {} | Mode: {} | Status: {}'.format(guild.id, current.strftime('%H:%M'), value['event_name'], c.MODE_NAME['rush'], 'Ended')
                                await console_interface.console_message('END_XP_EVENT', client_message)

                                if CHANNEL_PERMISSIONS == 1:
                                    if CHANNEL1:
                                        await CHANNEL1.send(l.xp_tracker[guild_l]['msg_post_5'].format(str(value['event_name']).capitalize(), server_config['xp_event']))
                                if CHANNEL2:
                                    await CHANNEL2.send(l.xp_tracker[guild_l]['msg_post_5'].format(str(value['event_name']).capitalize(), server_config['xp_event']))
                                continue

                        if value['type'] >= 1 and value['status'] == 0:
                            client_message = 'Guild id: {} | Guild time: {} | Event: {} | Mode: {} | Status: {}'.format(guild.id, current.strftime('%H:%M'), value['event_name'], c.MODE_NAME['std'] if value['type'] == 1 else c.MODE_NAME['rush'], 'In registration progress')
                            await console_interface.console_message('REGISTRATION_XP_EVENT', client_message)

                            message = l.xp_tracker[guild_l]['msg_post_6'].format(str(value['event_name']).capitalize(), server_config['events'])
                            new_time = await server_timer.get_timedelta(hours=int(ini['NOTIFICATION_TIMER']['HOURS']), region=guild_t)

                            if not self.GUILD_XP_EVENT_NOTIFICATION_TIMER:
                                await self.time_saver(guild.id, new_time.year, new_time.month, new_time.day, new_time.hour, 'xp_tracker')
                            else:
                                STATUS_X = False
                                for index, data in enumerate(self.GUILD_XP_EVENT_NOTIFICATION_TIMER):
                                    if data['guild'] == guild.id:
                                        if current.year >= data['year'] and current.month >= data['month'] and current.day >= data['day'] and current.hour >= data['hour']:
                                            if CHANNEL_PERMISSIONS == 1:
                                                if CHANNEL1:
                                                    await self.notificator(CHANNEL1, message)
                                            if CHANNEL_PERMISSIONS == 0:
                                                if CHANNEL2:
                                                    await self.notificator(CHANNEL2, message)

                                            self.GUILD_XP_EVENT_NOTIFICATION_TIMER.pop(index)
                                            await self.time_saver(guild.id, new_time.year, new_time.month, new_time.day, new_time.hour, 'xp_tracker')
                                        STATUS_X = True
                                        continue
                                if not STATUS_X:
                                    if not STATUS_X:
                                        await self.time_saver(guild.id, new_time.year, new_time.month, new_time.day, new_time.hour, 'xp_tracker')

                        if value['type'] >= 1 and value['status'] == 1:
                            client_message = 'Guild id: {} | Guild time: {} | Event: {} | Mode: {} | Status: {}'.format(guild.id, current.strftime('%H:%M'), value['event_name'], c.MODE_NAME['std'] if value['type'] == 1 else c.MODE_NAME['rush'], 'In collection data progress')
                            await console_interface.console_message('COLLECTION_XP_EVENT', client_message)
                            await asyncio.gather(self.autostats_xp(guild))

                            message = l.xp_tracker[guild_l]['msg_post_7'].format(str(value['event_name']).capitalize(), server_config['xp_event'])
                            new_time = await server_timer.get_timedelta(hours=int(ini['NOTIFICATION_TIMER']['HOURS']), region=guild_t)

                            if not self.GUILD_XP_EVENT_NOTIFICATION_TIMER:
                                await self.time_saver(guild.id, new_time.year, new_time.month, new_time.day, new_time.hour, 'xp_tracker')
                            else:
                                STATUS_XX = False
                                for index, data in enumerate(self.GUILD_XP_EVENT_NOTIFICATION_TIMER):
                                    if data['guild'] == guild.id:
                                        if current.year >= data['year'] and current.month >= data['month'] and current.day >= data['day'] and current.hour >= data['hour']:
                                            if CHANNEL_PERMISSIONS == 1:
                                                if CHANNEL1:
                                                    await self.notificator(CHANNEL1, message)
                                            if CHANNEL_PERMISSIONS == 0:
                                                if CHANNEL2:
                                                    await self.notificator(CHANNEL2, message)
                                            self.GUILD_XP_EVENT_NOTIFICATION_TIMER.pop(index)
                                            await self.time_saver(guild.id, new_time.year, new_time.month, new_time.day, new_time.hour, 'xp_tracker')
                                        STATUS_XX = True
                                        continue
                                if not STATUS_XX:
                                    await self.time_saver(guild.id, new_time.year, new_time.month, new_time.day, new_time.hour, 'xp_tracker')
        except Exception as error:
            await exception.error(error)

    async def xp_tracker_check_loop(self):
        try:
            server_current = await server_timer.get_server_current_time()

            if self.EVENT_CHECK_TIMER_XP_TRACKER != server_current.hour:
                path1 = c.CLIENT_PATH['guild']
                list_of_guilds = await discord_manager.get_servers(self.client, path1)

                for guild in list_of_guilds:
                    if guild and await discord_manager.get_server(self.client, guild.id):
                        path2 = c.GUILD_PATH['{}.ini'.format(xp_tracker.xp_tracker.name)].format(guild.id)
                        ini = await ini_manager.get_ini(path2)
                        if int(ini['STATUS']['STATUS']) == 2:
                            guild_t = await origin.get_region(guild.id)
                            guild_current = await server_timer.get_current_time(guild_t)
                            await asyncio.gather(self.xp_tracker_check_loop_1(guild, guild_current))
                self.EVENT_CHECK_TIMER_XP_TRACKER = server_current.hour
        except Exception as error:
            await exception.error(error)

    LIST_OF_SERVERS_XP_TRACKER = []

    async def xp_tracker_datastream_loop(self):
        try:
            path1 = c.CLIENT_PATH['guild']
            list_of_guilds = await discord_manager.get_servers(self.client, path1)

            for guild in list_of_guilds:
                STATUS = False
                STATUS_EVENT = False
                if guild and await discord_manager.get_server(self.client, guild.id):
                    path2 = c.GUILD_PATH['{}.ini'.format(xp_tracker.xp_tracker.name)].format(guild.id)
                    ini = await ini_manager.get_ini(path2)
                    if int(ini['STATUS']['STATUS']) == 2:
                        path3 = c.GUILD_PATH['event.json'].format(guild.id)
                        LIST1 = await json_manager.get_data(path3)
                        if LIST1:
                            for data in LIST1:
                                if data['type'] == 1 or data['type'] == 2:
                                    STATUS_EVENT = True

                            for server in self.LIST_OF_SERVERS_XP_TRACKER:
                                if server == guild.id:
                                    STATUS = True

                            if STATUS:
                                pass
                            else:
                                if STATUS_EVENT:
                                    self.LIST_OF_SERVERS_XP_TRACKER.append(guild.id)
                                    thread = datastream_xp.datastream(guild.id)
                                    thread.start()
                                    client_message = 'Guild id: {} | Datastream: {} | Status: {}'.format(guild.id, 'XP datastream', 'Added thread {}'.format(thread))
                                    await console_interface.console_message('THREAD_ADDED', client_message)

        except Exception as error:
            await exception.error(error)

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ XP_TRACKER.PY #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    @tasks.loop(minutes=1)
    async def update_xp_tracker(self):
        await self.xp_tracker_check_loop()

    @tasks.loop(minutes=10)
    async def update_datastream(self):
        await self.xp_tracker_datastream_loop()

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ _TRACKER.PY #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    EVENT_CHECK_TIMER_KC_TRACKER = 0
    GUILD_KC_EVENT_NOTIFICATION_TIMER = []
    GUILD_KC_EVENT_TIMER = []

    async def autostats_kc(self, guild):
        try:
            AUTO_NOTIFICATION_STATUS = False
            current = await server_timer.get_server_current_time()

            if not self.GUILD_KC_EVENT_TIMER:
                await self.time_saver(guild.id, current.year, current.month, current.day, current.hour+1, 'kc_tracker_auto_kc')
                AUTO_NOTIFICATION_STATUS = False
            else:
                STATUS_XX = False
                for index, data in enumerate(self.GUILD_KC_EVENT_TIMER):
                    if data['guild'] == guild.id:
                        if current.year >= data['year'] and current.month >= data['month'] and current.day >= data['day'] and current.hour >= data['hour']:
                            self.GUILD_KC_EVENT_TIMER.pop(index)
                            await self.time_saver(guild.id, current.year, current.month, current.day, current.hour+1, 'kc_tracker_auto_kc')
                            AUTO_NOTIFICATION_STATUS = False
                        STATUS_XX = True
                        continue
                if not STATUS_XX:
                    await self.time_saver(guild.id, current.year, current.month, current.day, current.hour+1, 'kc_tracker_auto_kc')
                    AUTO_NOTIFICATION_STATUS = False

            if not AUTO_NOTIFICATION_STATUS:
                guild_l = await origin.get_language(guild.id)
                self.GUILD_KC_EVENT_TIMER.append({'guild_id': guild, 'time': current.hour})

                path1 = c.GUILD_PATH['{}.ini'.format(kc_tracker.kc_tracker.name)].format(guild.id)
                path2 = c.GUILD_PATH['event.json'].format(guild.id)
                path3 = c.GUILD_PATH['kc_tracker.json'].format(guild.id)
                path4 = c.CLIENT_PATH['guild'] + str(guild.id) + c.CLIENT_JSON['server']
                path5 = c.ORIGIN_PATH['embed.tracker.json']

                ini = await ini_manager.get_ini(path1)
                server_config = await json_manager.get_json(path4)
                LIST1 = self.KC_ICON
                LIST2 = self.KC_PRE
                LIST3 = self.KC_NAME

                IMAGE = None
                IMAGE2 = self.KC_INFO_ICON
                WINNER_ROLE = ini['SECTION1']['EVENT_WINNER']

                DATA = []
                DATA3 = []

                TEMP_DATA = await json_manager.get_data(path2)
                DATA2 = await json_manager.get_data(path3)

                EVENT_NAME = None
                EMBED_TEXT = ''

                await origin.get_locale()
                CHANNEL = await discord_manager.get_channel(self.client, guild.id, server_config['kc_event'])

                if CHANNEL:
                    async for message in CHANNEL.history(limit=10):
                        if message:
                            await message.delete()

                for value in TEMP_DATA:
                    if value['type'] == 3 or value['type'] == 4:
                        DATA.append(value)

                def get_id(INFO):
                    return INFO.get('sum')

                if DATA:
                    for data1 in DATA:
                        if DATA2:
                            for data2 in DATA2:
                                for key, value in data2.items():
                                    if key == data1['event_name']:
                                        sum = data2['{}_current'.format(key)] - data2[key]
                                        DATA3.append({'user_id': data2['user_id'], 'user_username': data2['user_username'], 'user_rsn': data2['user_rsn'], 'sum': sum})

                                        for index, event_name in enumerate(LIST2):
                                            if event_name == data1['event_name']:
                                                if data1['type'] == 3:
                                                    EVENT_NAME = '{} [ S ]'.format(LIST3[index])

                                                if data1['type'] == 4:
                                                    EVENT_NAME = '{} [ R ]'.format(LIST3[index])

                                        for index, value3 in enumerate(LIST2):
                                            if str(value3) == str(key):
                                                IMAGE = LIST1[index]

                            DATA3.sort(key=get_id, reverse=True)

                            json_string = await json_manager.get_json(path5)
                            new_json_string = {'data': []}
                            STRING = ''
                            SUM = 0

                            for key, value in json_string[guild_l]['kc_tracker']['stats'].items():
                                if DATA3:
                                    if int(key) == 1:
                                        for index, data in enumerate(DATA3):
                                            index = index + 1
                                            if index <= 10:
                                                if index == 1:
                                                    title = ':first_place: {}'.format(l.DISCORD_TOP[guild_l][index - 1])
                                                elif index == 2:
                                                    title = ':second_place: {}'.format(l.DISCORD_TOP[guild_l][index - 1])
                                                elif index == 3:
                                                    title = ':third_place: {}'.format(l.DISCORD_TOP[guild_l][index - 1])
                                                else:
                                                    title = '{}'.format(l.DISCORD_TOP[guild_l][index - 1])

                                                STRING += l.kc_tracker[guild_l]['configuration']['current_kc'].format(title, data['user_username'], data['user_rsn'], locale.format_string('%d', data['sum'], grouping=True))
                                                SUM += data['sum']

                                                if data1['status'] == 2 and data1['prize_count'] >= index and data1['win_message'] == 0:
                                                    member = await discord_manager.get_member(self.client, guild.id, data['user_id'])
                                                    role = await discord_manager.get_role(self.client, guild.id, int(WINNER_ROLE))

                                                    if index == 1 and member and role:
                                                        await member.add_roles(role, reason='{}'.format(c.DISCORD_MESSAGES['kc_event_winner']), atomic=True)
                                                        EMBED_TEXT += '{}\n'.format(l.kc_tracker[guild_l]['extra_1'].format(EVENT_NAME.capitalize(), member.mention if member else data['user_id']))
                                                    elif int(data1['prize_count']) >= index and member:
                                                        EMBED_TEXT += '{}\n'.format(l.kc_tracker[guild_l]['extra_2'].format(EVENT_NAME.capitalize(), member.mention if member else data['user_id']))
                                                    else:
                                                        EMBED_TEXT += '{}\n'.format(l.kc_tracker[guild_l]['msg_error_7'].format(EVENT_NAME.capitalize(), data['user_id'], data['user_rsn']))

                                                    await json_manager.update(path2, 'id', data1['id'], 'win_message', 1)

                                        STRING += l.kc_tracker[guild_l]['configuration']['total_kc'].format(locale.format_string('%d', SUM, grouping=True))
                                        new_json_string['data'].append({
                                            'name{}'.format(key): value['name'].format('\u200D'),
                                            'value{}'.format(key): str(value['value']).format(STRING)
                                        })
                                    else:
                                        STRING += l.kc_tracker[guild_l]['configuration']['total_kc'].format(locale.format_string('%d', SUM, grouping=True))
                                        new_json_string['data'].append({
                                            'name{}'.format(key): value['name'],
                                            'value{}'.format(key): str(value['value']).format(guild.name)
                                        })

                            await asyncio.gather(embed_creator.create_embed(guild.id, discord.Color.dark_red(), False, guild.icon_url, IMAGE, l.kc_tracker[guild_l]['embed_3'].format(guild.name, EVENT_NAME), new_json_string['data'], False, False, CHANNEL))
                            DATA3.clear()

                    if EMBED_TEXT != '':
                        embed_json_string = {'data': [
                            {
                                'name1': '{}'.format(l.kc_tracker[guild_l]['embed_4'].format(guild.name)),
                                'value1': EMBED_TEXT
                            }
                        ]}
                        CHANNEL2 = await discord_manager.get_channel(self.client, guild.id, server_config['admin'])
                        if CHANNEL2:
                            await asyncio.gather(embed_creator.create_embed(guild.id, discord.Color.dark_red(), False, guild.icon_url, IMAGE, l.kc_tracker[guild_l]['embed_4'].format(guild.name, EVENT_NAME), embed_json_string['data'], False, False, CHANNEL2))

                    json_string2 = await json_manager.get_json(path5)
                    new_json_string1 = {'data': []}

                    for key, value in json_string2[guild_l]['kc_tracker']['autostats'].items():
                        if int(key) == 1:
                            new_json_string1['data'].append({
                                'name{}'.format(key): value['name'],
                                'value{}'.format(key): value['value']
                            })
                        else:
                            new_json_string1['data'].append({
                                'name{}'.format(key): value['name'],
                                'value{}'.format(key): value['value']
                            })

                    await asyncio.gather(embed_creator.create_embed(guild.id, discord.Color.dark_red(), False, guild.icon_url, IMAGE2, l.kc_tracker[guild_l]['embed_2'].format(guild.name), new_json_string1['data'], False, False, CHANNEL))
        except Exception as error:
            await exception.error(error)

    async def start_kc_event(self, event_name, date_start, time_start, guild_id):
        try:
            if guild_id:
                guild_t = await origin.get_region(guild_id)
                path1 = c.GUILD_PATH['kc_tracker.json'].format(guild_id)
                DATA = await json_manager.get_data(path1)

                guild_current = await server_timer.get_current_time(guild_t)
                COUNTER = 0

                if date_start == guild_current.strftime('%m.%d') and time_start == guild_current.hour:
                    if DATA:
                        LIST3 = self.KC_NAME
                        LIST4 = self.KC_PRE
                        for data in DATA:
                            CHECK = True
                            USERNAME = data['user_rsn']
                            USERNAME = USERNAME.replace(' ', '%20')
                            while CHECK:
                                USER = hiscores_kc.Hiscores2V(USERNAME, LIST3, LIST4)
                                if USER.status != 404:
                                    CHECK = False
                                    USER_STATS = USER.getKc(event_name)
                                    target_keys = [event_name, '{}_current'.format(event_name)]
                                    target_values = [int(USER_STATS['kc']), int(USER_STATS['kc'])]
                                    await json_manager.update(path1, 'user_rsn', data['user_rsn'], target_keys, target_values)

                                    client_message = 'Guild id: {} | Guild time: {} | Event: {} | Rsn: {} | Registration KC: {} | Status: {}'.format(guild_id, guild_current.strftime('%H:%M'), event_name, data['user_rsn'], USER_STATS['kc'], 'KC event start reset')
                                    await console_interface.console_message('START_KC_EVENT_RESET', client_message)
                                    await logger.log_event(guild_id, 'kc_tracker', c.CLIENT_MESSAGES['kc_tracker_reset'], client_message)
                                else:
                                    if COUNTER >= 10:
                                        CHECK = False
                                        COUNTER = 0
                                    else:
                                        COUNTER += 1

                guild = await discord_manager.get_server(self.client, guild_id)
                await asyncio.gather(self.autostats_kc(guild))
        except Exception as error:
            await exception.error(error)

    async def end_kc_event(self, event_name, date_end, time_end, guild_id, mode):
        try:
            if guild_id:
                guild_t = await origin.get_region(guild_id)
                path1 = c.GUILD_PATH['kc_tracker.json'].format(guild_id)
                DATA = await json_manager.get_data(path1)

                guild_current = await server_timer.get_current_time(guild_t)
                STATUS = False
                COUNTER = 0

                if mode == c.MODE_NAME['std']:
                    if date_end == guild_current.strftime('%m.%d') and time_end == guild_current.hour:
                        STATUS = True
                elif mode == c.MODE_NAME['rush']:
                    STATUS = True

                if STATUS:
                    if DATA:
                        LIST3 = self.KC_NAME
                        LIST4 = self.KC_PRE
                        for data in DATA:
                            CHECK = True
                            USERNAME = data['user_rsn']
                            USERNAME = USERNAME.replace(' ', '%20')
                            while CHECK:
                                USER = hiscores_kc.Hiscores2V(USERNAME, LIST3, LIST4)
                                USER_STATS = USER.getKc(event_name)
                                if USER.status != 404:
                                    CHECK = False
                                    target_keys = ['{}_current'.format(event_name)]
                                    target_values = [int(USER_STATS['kc'])]
                                    await json_manager.update(path1, 'user_rsn', data['user_rsn'], target_keys, target_values)

                                    client_message = 'Guild id: {} | Guild time: {} | Event: {} | Rsn: {} | Registration KC: {} | Current_KC: {} | Status: {}'.format(guild_id, guild_current.strftime('%H:%M'), event_name, data['user_rsn'], data[event_name], data['{}_current'.format(event_name)], 'Last KC update')
                                    await console_interface.console_message('START_LAST_KC_EVENT_CHECK', client_message)
                                    await logger.log_event(guild_id, 'kc_tracker', c.CLIENT_MESSAGES['kc_tracker_update'], client_message)
                                else:
                                    if COUNTER >= 10:
                                        CHECK = False
                                        COUNTER = 0
                                    else:
                                        COUNTER += 1

                guild = await discord_manager.get_server(self.client, guild_id)
                await asyncio.gather(self.autostats_kc(guild))
        except Exception as error:
            await exception.error(error)

    async def kc_tracker_check_loop_1(self, guild, current):
        try:
            guild_l = await origin.get_language(guild.id)
            guild_t = await origin.get_region(guild.id)
            path = c.CLIENT_PATH['guild'] + str(guild.id) + c.CLIENT_JSON['server']
            path2 = c.GUILD_PATH['event.json'].format(guild.id)
            server_config = await json_manager.get_json(path)
            CHANNEL1 = await discord_manager.get_channel(self.client, guild.id, server_config['chat0'])
            CHANNEL2 = await discord_manager.get_channel(self.client, guild.id, server_config['chat1'])

            path1 = c.GUILD_PATH['{}.ini'.format(kc_tracker.kc_tracker.name)].format(guild.id)
            ini = await ini_manager.get_ini(path1)
            CHANNEL_PERMISSIONS = int(ini['CHANNEL_PERMISSIONS']['STATUS'])

            LIST1 = await json_manager.get_data(path2)
            if LIST1:
                for value in LIST1:
                    if value['type'] == 3 or value['type'] == 4:
                        if current.month >= int(value['date_start'][:2]):
                            if current.day >= int(value['date_start'][3:]):
                                if current.hour >= value['time_start'] and value['status'] == 0:
                                    await json_manager.update(path2, 'id', value['id'], 'status', 1)
                                    await asyncio.gather(self.start_kc_event(value['event_name'], value['date_start'], value['time_start'], guild.id))
                                    client_message = 'Guild id: {} | Guild time: {} | Event: {} | Mode: {} | Status: {}'.format(guild.id, current.strftime('%H:%M'), value['event_name'], c.MODE_NAME['std'] if value['type'] == 1 else c.MODE_NAME['rush'], 'Started')
                                    await console_interface.console_message('START_KC_EVENT', client_message)

                                    if CHANNEL_PERMISSIONS == 1:
                                        if CHANNEL1:
                                            await CHANNEL1.send(l.kc_tracker[guild_l]['msg_post_4'].format(str(value['event_name']).capitalize()))
                                    if CHANNEL2:
                                        await CHANNEL2.send(l.kc_tracker[guild_l]['msg_post_4'].format(str(value['event_name']).capitalize()))
                                    continue

                        if value['type'] == 3 and value['status'] == 1:
                            if current.month >= int(value['date_end'][:2]):
                                if current.day >= int(value['date_end'][3:]):
                                    if current.hour >= value['time_end']:
                                        await json_manager.update(path2, 'id', value['id'], 'status', 2)
                                        await asyncio.gather(self.end_kc_event(value['event_name'], value['date_end'], value['time_end'], guild.id, c.MODE_NAME['std']))
                                        client_message = 'Guild id: {} | Guild time: {} | Event: {} | Mode: {} | Status: {}'.format(guild.id, current.strftime('%H:%M'), value['event_name'], c.MODE_NAME['std'], 'Ended')
                                        await console_interface.console_message('END_KC_EVENT', client_message)

                                        if CHANNEL_PERMISSIONS == 1:
                                            if CHANNEL1:
                                                await CHANNEL1.send(l.kc_tracker[guild_l]['msg_post_5'].format(str(value['event_name']).capitalize(), server_config['kc_event']))
                                        if CHANNEL2:
                                            await CHANNEL2.send(l.kc_tracker[guild_l]['msg_post_5'].format(str(value['event_name']).capitalize(), server_config['kc_event']))
                                        continue
                        elif value['type'] == 4 and value['status'] == 1:
                            path3 = c.GUILD_PATH['tracker.json'].format(guild.id)
                            player_data = await json_manager.get_data(path3)

                            COUNTER = 0

                            for player_kc in player_data:
                                if '{}_current'.format(value['event_name']) in player_kc.keys() and '{}'.format(value['event_name']) in player_kc.keys():
                                    if player_kc['{}_current'.format(value['event_name'])] - player_kc['{}'.format(value['event_name'])] >= value['kc_target']:
                                        COUNTER += 1

                            if COUNTER >= value['prize_count']:
                                await json_manager.update(path2, 'id', value['id'], 'status', 2)
                                await asyncio.gather(self.end_kc_event(value['event_name'], value['date_end'], value['time_end'], guild.id, c.MODE_NAME['rush']))
                                client_message = 'Guild id: {} | Guild time: {} | Event: {} | Mode: {} | Status: {}'.format(guild.id, current.strftime('%H:%M'), value['event_name'], c.MODE_NAME['rush'], 'Ended')
                                await console_interface.console_message('END_KC_EVENT', client_message)

                                if CHANNEL_PERMISSIONS == 1:
                                    if CHANNEL1:
                                        await CHANNEL1.send(l.kc_tracker[guild_l]['msg_post_5'].format(str(value['event_name']).capitalize(), server_config['kc_event']))
                                if CHANNEL2:
                                    await CHANNEL2.send(l.kc_tracker[guild_l]['msg_post_5'].format(str(value['event_name']).capitalize(), server_config['kc_event']))
                                continue

                        if value['type'] >= 3 and value['status'] == 0:
                            client_message = 'Guild id: {} | Guild time: {} | Event: {} | Mode: {} | Status: {}'.format(guild.id, current.strftime('%H:%M'), value['event_name'], c.MODE_NAME['std'] if value['type'] == 1 else c.MODE_NAME['rush'], 'In registration progress')
                            await console_interface.console_message('REGISTRATION_KC_EVENT', client_message)

                            message = l.kc_tracker[guild_l]['msg_post_6'].format(str(value['event_name']).capitalize(), server_config['events'])
                            new_time = await server_timer.get_timedelta(hours=int(ini['NOTIFICATION_TIMER']['HOURS']), region=guild_t)

                            if not self.GUILD_KC_EVENT_NOTIFICATION_TIMER:
                                await self.time_saver(guild.id, new_time.year, new_time.month, new_time.day, new_time.hour, 'kc_tracker')
                            else:
                                STATUS_X = False
                                for index, data in enumerate(self.GUILD_KC_EVENT_NOTIFICATION_TIMER):
                                    if data['guild'] == guild.id:
                                        if current.year >= data['year'] and current.month >= data['month'] and current.day >= data['day'] and current.hour >= data['hour']:
                                            if CHANNEL_PERMISSIONS == 1:
                                                if CHANNEL1:
                                                    await self.notificator(CHANNEL1, message)
                                            if CHANNEL_PERMISSIONS == 0:
                                                if CHANNEL2:
                                                    await self.notificator(CHANNEL2, message)

                                            self.GUILD_KC_EVENT_NOTIFICATION_TIMER.pop(index)
                                            await self.time_saver(guild.id, new_time.year, new_time.month, new_time.day, new_time.hour, 'kc_tracker')
                                        STATUS_X = True
                                        continue
                                if not STATUS_X:
                                    if not STATUS_X:
                                        await self.time_saver(guild.id, new_time.year, new_time.month, new_time.day, new_time.hour, 'kc_tracker')

                        if value['type'] >= 3 and value['status'] == 1:
                            client_message = 'Guild id: {} | Guild time: {} | Event: {} | Mode: {} | Status: {}'.format(guild.id, current.strftime('%H:%M'), value['event_name'], c.MODE_NAME['std'] if value['type'] == 1 else c.MODE_NAME['rush'], 'In collection data progress')
                            await console_interface.console_message('COLLECTION_KC_EVENT', client_message)
                            await asyncio.gather(self.autostats_kc(guild))

                            message = l.kc_tracker[guild_l]['msg_post_7'].format(str(value['event_name']).capitalize(), server_config['kc_event'])
                            new_time = await server_timer.get_timedelta(hours=int(ini['NOTIFICATION_TIMER']['HOURS']), region=guild_t)

                            if not self.GUILD_KC_EVENT_NOTIFICATION_TIMER:
                                await self.time_saver(guild.id, new_time.year, new_time.month, new_time.day, new_time.hour, 'kc_tracker')
                            else:
                                STATUS_XX = False
                                for index, data in enumerate(self.GUILD_KC_EVENT_NOTIFICATION_TIMER):
                                    if data['guild'] == guild.id:
                                        if current.year >= data['year'] and current.month >= data['month'] and current.day >= data['day'] and current.hour >= data['hour']:
                                            if CHANNEL_PERMISSIONS == 1:
                                                if CHANNEL1:
                                                    await self.notificator(CHANNEL1, message)
                                            if CHANNEL_PERMISSIONS == 0:
                                                if CHANNEL2:
                                                    await self.notificator(CHANNEL2, message)
                                            self.GUILD_KC_EVENT_NOTIFICATION_TIMER.pop(index)
                                            await self.time_saver(guild.id, new_time.year, new_time.month, new_time.day, new_time.hour, 'kc_tracker')
                                        STATUS_XX = True
                                        continue
                                if not STATUS_XX:
                                    await self.time_saver(guild.id, new_time.year, new_time.month, new_time.day, new_time.hour, 'kc_tracker')
        except Exception as error:
            await exception.error(error)

    async def kc_tracker_check_loop(self):
        try:
            server_current = await server_timer.get_server_current_time()

            if self.EVENT_CHECK_TIMER_KC_TRACKER != server_current.hour:
                path1 = c.CLIENT_PATH['guild']
                list_of_guilds = await discord_manager.get_servers(self.client, path1)

                for guild in list_of_guilds:
                    if guild and await discord_manager.get_server(self.client, guild.id):
                        guild_t = await origin.get_region(guild.id)
                        guild_current = await server_timer.get_current_time(guild_t)
                        path2 = c.GUILD_PATH['{}.ini'.format(kc_tracker.kc_tracker.name)].format(guild.id)
                        ini = await ini_manager.get_ini(path2)
                        if int(ini['STATUS']['STATUS']) == 2:
                            await asyncio.gather(self.kc_tracker_check_loop_1(guild, guild_current))
                self.EVENT_CHECK_TIMER_KC_TRACKER = server_current.hour
        except Exception as error:
            await exception.error(error)

    LIST_OF_SERVERS_KC_TRACKER = []

    async def kc_tracker_datastream_loop(self):
        try:
            path1 = c.CLIENT_PATH['guild']
            list_of_guilds = await discord_manager.get_servers(self.client, path1)

            for guild in list_of_guilds:
                STATUS = False
                STATUS_EVENT = False
                if guild and await discord_manager.get_server(self.client, guild.id):
                    path2 = c.GUILD_PATH['{}.ini'.format(kc_tracker.kc_tracker.name)].format(guild.id)
                    ini = await ini_manager.get_ini(path2)
                    if int(ini['STATUS']['STATUS']) == 2:
                        path3 = c.GUILD_PATH['event.json'].format(guild.id)
                        LIST1 = await json_manager.get_data(path3)
                        if LIST1:
                            for data in LIST1:
                                if data['type'] == 3 or data['type'] == 4:
                                    STATUS_EVENT = True

                            for server in self.LIST_OF_SERVERS_KC_TRACKER:
                                if guild.id == server:
                                    STATUS = True

                            if STATUS:
                                pass
                            else:
                                if STATUS_EVENT:
                                    self.LIST_OF_SERVERS_KC_TRACKER.append(guild.id)
                                    thread = datastream_kc.datastream(guild.id)
                                    thread.start()
                                    client_message = 'Guild id: {} | Datastream: {} | Status: {}'.format(guild.id, 'KC datastream', 'Added thread {}'.format(thread))
                                    await console_interface.console_message('THREAD ADDED', client_message)

        except Exception as error:
            await exception.error(error)

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ KC_TRACKER.PY #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    @tasks.loop(minutes=1)
    async def update_kc_tracker(self):
        await self.kc_tracker_check_loop()

    @tasks.loop(minutes=10)
    async def update_datastream2(self):
        await asyncio.sleep(60*10)
        await self.kc_tracker_datastream_loop()

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ KC_TRACKER.PY #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    EVENT_CHECK_TIMER_REGISTER = 0

    async def event_register_loop(self, guild):
        try:
            NEW_LIST = {'data': []}
            CLEAR_LIST = {'data': []}
            path = c.GUILD_PATH['event.json'].format(guild.id)
            path1 = c.GUILD_PATH['tracker.json'].format(guild.id)
            path2 = c.GUILD_PATH['kc_tracker.json'].format(guild.id)
            DATA1 = await json_manager.get_data(path)

            XP_EVENT_COUNTER = 0
            KC_EVENT_COUNTER = 0

            XP_EVENT_END_COUNTER = 0
            KC_EVENT_END_COUNTER = 0

            for value1 in DATA1:
                if value1['type'] == 0 and value1['status'] == 0:
                    NEW_LIST['data'].append(value1)

                if (value1['type'] >= 1) and value1['status'] == 0:
                    NEW_LIST['data'].append(value1)

                if (1 <= value1['type'] <= 4) and value1['status'] == 1:
                    NEW_LIST['data'].append(value1)

                if 1 <= value1['type'] <= 4:
                    if value1['type'] == 1 or value1['type'] == 2:
                        XP_EVENT_COUNTER += 1

                    if value1['type'] == 3 or value1['type'] == 4:
                        KC_EVENT_COUNTER += 1

                if (1 <= value1['type'] <= 4) and value1['status'] == 2:
                    NEW_LIST['data'].append(value1)

                    if value1['type'] == 1 or value1['type'] == 2:
                        XP_EVENT_END_COUNTER += 1

                    if value1['type'] == 3 or value1['type'] == 4:
                        KC_EVENT_END_COUNTER += 1

            await json_manager.clear_and_update(path, NEW_LIST)

            if XP_EVENT_END_COUNTER >= XP_EVENT_COUNTER:
                await xp_tracker.xp_tracker.fun_removeallxp(guild.id, 1)

            if KC_EVENT_END_COUNTER >= KC_EVENT_COUNTER:
                await kc_tracker.kc_tracker.fun_removeallkc(guild.id, 1)

            if XP_EVENT_COUNTER >= 1:
                if XP_EVENT_END_COUNTER >= XP_EVENT_COUNTER:
                    await xp_tracker.xp_tracker.fun_removeallxp(guild.id, 1)
                    await json_manager.clear_and_update(path1, CLEAR_LIST)

            if KC_EVENT_COUNTER >= 1:
                if KC_EVENT_END_COUNTER >= KC_EVENT_COUNTER:
                    await kc_tracker.kc_tracker.fun_removeallkc(guild.id, 1)
                    await json_manager.clear_and_update(path2, CLEAR_LIST)

        except Exception as error:
            await exception.error(error)

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ EVENT REGISTER #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    @tasks.loop(minutes=1)
    async def event_register(self):
        server_current = await server_timer.get_server_current_time()

        if self.EVENT_CHECK_TIMER_REGISTER != server_current.hour:
            path1 = c.CLIENT_PATH['guild']
            list_of_guilds = await discord_manager.get_servers(self.client, path1)

            for guild in list_of_guilds:
                if guild and await discord_manager.get_server(self.client, guild.id):
                    await asyncio.gather(self.event_register_loop(guild))

            self.EVENT_CHECK_TIMER_REGISTER = server_current.hour

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬ EVENT REGISTER #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    @tasks.loop(count=1)
    async def variable_init(self):
        try:
            path_global_dc_bank = c.GUILD_PATH['{}_g.ini'.format(dc_bank.dc_bank.name)]
            path_global_xp_tracker = c.GUILD_PATH['{}_g.ini'.format(xp_tracker.xp_tracker.name)]
            path_global_kc_tracker = c.GUILD_PATH['{}_g.ini'.format(kc_tracker.kc_tracker.name)]
            ini_dc_bank = await ini_manager.get_ini(path_global_dc_bank)
            ini_xp_tracker = await ini_manager.get_ini(path_global_xp_tracker)
            ini_kc_tracker = await ini_manager.get_ini(path_global_kc_tracker)

            self.COINS1 = ini_dc_bank['CONSTANT2']['COINS1']
            self.COINS2 = ini_dc_bank['CONSTANT2']['COINS2']

            self.XP_ICON = await json_manager.get_ini_list(path_global_xp_tracker, 'CONSTANT3', 'ICON')
            self.XP_PRE = await json_manager.get_ini_list(path_global_xp_tracker, 'CONSTANT2', 'PRE')
            self.XP_INFO_ICON = ini_xp_tracker['CONSTANT3']['INFO_ICON']

            self.KC_ICON = await json_manager.get_ini_list(path_global_kc_tracker, 'CONSTANT3', 'ICON')
            self.KC_PRE = await json_manager.get_ini_list(path_global_kc_tracker, 'CONSTANT2', 'PRE')
            self.KC_NAME = await json_manager.get_ini_list(path_global_kc_tracker, 'CONSTANT1', 'NAME')
            self.KC_INFO_ICON = ini_kc_tracker['CONSTANT3']['INFO_ICON']

            await console_interface.console_message(c.CLIENT_MESSAGES['variable_init'].format(self.name))
        except Exception as error:
            await exception.error(error)

    def __init__(self, client):
        self.COINS1 = None
        self.COINS2 = None
        self.XP_ICON = None
        self.XP_PRE = None
        self.XP_INFO_ICON = None
        self.KC_ICON = None
        self.KC_PRE = None
        self.KC_NAME = None
        self.KC_INFO_ICON = None

        self.variable_init.start()
        self.client = client

        self.update_dc_bank.start()
        self.update_votemute.start()
        self.event_register.start()
        self.update_organizer.start()
        self.update_xp_tracker.start()
        self.update_datastream.start()
        self.update_kc_tracker.start()
        self.update_datastream2.start()

def setup(client):
    client.add_cog(preprocessor(client))
