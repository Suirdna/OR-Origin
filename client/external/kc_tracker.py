from client import exception, embed_creator, console_interface, discord_manager, file_manager, ini_manager, json_manager, origin, permissions, server_timer
from client.config import config as c, language as l
from discord.ext import commands, tasks
from client.external.hiscores import hiscores_kc
from PIL import Image, ImageDraw, ImageFont
import discord, locale

class kc_tracker(commands.Cog):
    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    name = 'kc_tracker'

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    @staticmethod
    async def fun_kctracker(ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            guild_t = await origin.get_region(ctx.guild.id)
            path = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
            target_keys = ['user_id', 'user_status']
            target_values = [ctx.author.id, c.USER_PERMISSIONS['organizer']]

            if await permissions.get_user_permission(path, target_keys, target_values) or ctx.author.id == ctx.guild.owner.id or ctx.author.id == c.CLIENT_ADMINISTRATION_ID:
                if ctx.message.content == '.kctracker':
                    path3 = c.ORIGIN_PATH['embed.tracker.json']
                    guild_current = await server_timer.get_current_time(guild_t)
                    guild_seven_day = await server_timer.get_timedelta(days=7, region=guild_t)

                    json_string = await json_manager.get_json(path3)
                    new_json_string = {'data': []}

                    for key, value in json_string[guild_l]['kc_tracker']['tracker'].items():
                        if int(key) == 1:
                            new_json_string['data'].append({
                                'name{}'.format(key): value['name'],
                                'value{}'.format(key): str(value['value']).format(
                                    guild_current.strftime('%m.%d'), guild_seven_day.strftime('%m.%d'),
                                    guild_current.hour + 1, guild_current.hour + 1
                                )
                            })
                        else:
                            new_json_string['data'].append({
                                'name{}'.format(key): value['name'],
                                'value{}'.format(key): value['value']
                            })
                    await embed_creator.create_embed(ctx, discord.Color.dark_red(), False, ctx.guild.icon_url, c.CLIENT_ICON, l.kc_tracker[guild_l]['embed_1'].format(ctx.guild.name), new_json_string['data'], False)
            else:
                await ctx.author.send(l.user_permissions[guild_l]['msg_restricted_1'])
        except Exception as error:
            await exception.error(error)

    async def fun_addkcevent(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            path1 = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
            target_keys = ['user_id', 'user_status']
            target_values = [ctx.author.id, c.USER_PERMISSIONS['organizer']]

            if await permissions.get_user_permission(path1, target_keys, target_values) or ctx.author.id == ctx.guild.owner.id or ctx.author.id == c.CLIENT_ADMINISTRATION_ID:
                STRING = str(ctx.message.content).split(' ')
                if len(STRING) >= 9:
                    path = c.CLIENT_PATH['guild'] + str(ctx.guild.id) + c.CLIENT_JSON['server']
                    path2 = c.GUILD_PATH['event.json'].format(ctx.guild.id)

                    server_config = await json_manager.get_json(path)
                    LIST1 = self.PRE
                    LIST2 = self.NAME
                    LIST3 = self.ICON

                    DATA1 = await json_manager.get_data(path2)

                    ID = await origin.randomize()
                    STATUS = True
                    STATUS2 = False

                    while STATUS:
                        for data in DATA1:
                            if data['id'] == ID:
                                STATUS2 = True
                        if not STATUS2:
                            STATUS = False
                        else:
                            ID = await origin.randomize()

                    EXTRA = ''
                    NAME = ''

                    for index, value in enumerate(LIST1):
                        if str(value).lower() == STRING[2].lower():
                            NAME = LIST2[index]

                    for index, event in enumerate(LIST1):
                        if STRING[2] == event:

                            RUSH = None
                            if STRING[1].isdigit() and int(STRING[1]) > 1:
                                RUSH = l.kc_tracker[guild_l]['configuration']['rush_point'].format(locale.format_string('%d', int(STRING[1]), grouping=True))

                            path4 = c.ORIGIN_PATH['embed.tracker.json']
                            DESCRIPTION = l.kc_tracker[guild_l]['description_1'].format(
                                ctx.author.mention,
                                STRING[4], STRING[6], NAME, STRING[5] if not RUSH else l.kc_tracker[guild_l]['extra_4'], STRING[7] if not RUSH else l.kc_tracker[guild_l]['extra_4'], RUSH if RUSH else ''
                            )
                            if len(STRING) >= 8:
                                for value in STRING[8:]:
                                    EXTRA += '{} '.format(value)

                            json_string = await json_manager.get_json(path4)
                            new_json_string = {'data': []}

                            for key, value in json_string[guild_l]['kc_tracker']['addevent'].items():
                                if int(key) == 1:
                                    new_json_string['data'].append({
                                        'name{}'.format(key): value['name'],
                                        'value{}'.format(key): str(value['value']).format(EXTRA)
                                    })
                                if int(key) == 2:
                                    new_json_string['data'].append({
                                        'name{}'.format(key): value['name'],
                                        'value{}'.format(key): value['value']
                                    })

                            if STRING[1].isdigit():
                                mode_type = 0
                                if int(STRING[1]) == c.EVENT_MODE[0]:
                                    mode_type = 3
                                elif int(STRING[1]) >= c.EVENT_MODE[1]:
                                    mode_type = 4

                                EVENT_CHANNEL = await discord_manager.get_channel(self.client, ctx.guild.id, server_config['events'])
                                embed = await embed_creator.create_embed(ctx, discord.Color.dark_red(), False, ctx.guild.icon_url, LIST3[index], l.kc_tracker[guild_l]['embed_2'].format(ctx.guild.name), new_json_string['data'], False, False, EVENT_CHANNEL, DESCRIPTION)

                                json_string = {'id': ID, 'user_id': ctx.author.id, 'message_id': embed.id, 'event_name': STRING[2], 'kc_target': int(STRING[1]), 'prize_count': int(STRING[3]), 'date_start': STRING[4], 'date_end': STRING[5], 'time_start': int(STRING[6]), 'time_end': int(STRING[7]), 'participants': 0, 'status': 0, 'type': mode_type, 'win_message': 0}
                                await json_manager.create(path2, json_string)
                                await ctx.author.send(l.kc_tracker[guild_l]['msg_success_1'])

                                CHANNEL1 = await discord_manager.get_channel(self.client, ctx.guild.id, server_config['chat0'])
                                CHANNEL2 = await discord_manager.get_channel(self.client, ctx.guild.id, server_config['chat1'])

                                if CHANNEL1:
                                    await CHANNEL1.send(l.kc_tracker[guild_l]['msg_post_1'].format(NAME, server_config['events']))
                                if CHANNEL2:
                                    await CHANNEL2.send(l.kc_tracker[guild_l]['msg_post_1'].format(NAME, server_config['events']))
                            else:
                                await ctx.author.send(l.kc_tracker[guild_l]['msg_badformat_1'])
                else:
                    await ctx.author.send(l.kc_tracker[guild_l]['msg_badformat_1'])
            else:
                await ctx.author.send(l.user_permissions[guild_l]['msg_restricted_1'])
        except Exception as error:
            await exception.error(error)

    @staticmethod
    async def fun_removeallkc(ctx, system=None):
        try:
            guild_l = await origin.get_language(ctx.guild.id if hasattr(ctx, 'guild') else ctx)
            path1 = c.GUILD_PATH['special_member.json'].format(ctx.guild.id if hasattr(ctx, 'guild') else ctx)
            path2 = c.GUILD_PATH['kc_tracker.json'].format(ctx.guild.id if hasattr(ctx, 'guild') else ctx)
            path3 = c.GUILD_PATH['event.json'].format(ctx.guild.id if hasattr(ctx, 'guild') else ctx)

            LIST1 = await json_manager.get_data(path3)

            NEW_LIST1 = {'data': []}
            NEW_LIST2 = {'data': []}

            if hasattr(ctx, 'guild'):
                target_keys = ['user_id', 'user_status']
                target_values = [ctx.author.id, c.USER_PERMISSIONS['organizer']]

                if await permissions.get_user_permission(path1, target_keys, target_values) or ctx.author.id == ctx.guild.owner.id or ctx.author.id == c.CLIENT_ADMINISTRATION_ID:
                    for data in LIST1:
                        if data['type'] == 0 and data['status'] == 0:
                            NEW_LIST2['data'].append(data)
                        elif data['type'] == 1 and data['status'] >= 0:
                            NEW_LIST2['data'].append(data)
                        elif data['type'] == 2 and data['status'] >= 0:
                            NEW_LIST2['data'].append(data)

                    await json_manager.clear_and_update(path2, NEW_LIST1)
                    await json_manager.clear_and_update(path3, NEW_LIST2)
                    await ctx.author.send(l.xp_tracker[guild_l]['msg_success_2'])
                else:
                    await ctx.author.send(l.user_permissions[guild_l]['msg_restricted_1'])
            elif system == 1:
                if LIST1:
                    for data in LIST1:
                        if data['type'] == 0 and data['status'] == 0:
                            NEW_LIST2['data'].append(data)
                        elif data['type'] == 1 and data['status'] >= 0:
                            NEW_LIST2['data'].append(data)
                        elif data['type'] == 2 and data['status'] >= 0:
                            NEW_LIST2['data'].append(data)

                await json_manager.clear_and_update(path2, NEW_LIST1)
                await json_manager.clear_and_update(path3, NEW_LIST2)
        except Exception as error:
            await exception.error(error)

    async def fun_akc(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            STRING = str(ctx.message.content).split(' ')
            if len(STRING) >= 2:
                path = c.CLIENT_PATH['guild'] + str(ctx.guild.id) + c.CLIENT_JSON['server']
                path1 = c.GUILD_PATH['kc_tracker.json'].format(ctx.guild.id)
                path2 = c.GUILD_PATH['event.json'].format(ctx.guild.id)
                server_config = await json_manager.get_json(path)
                LIST1 = await json_manager.get_data(path1)
                LIST2 = await json_manager.get_data(path2)
                LIST3 = self.NAME
                LIST4 = self.PRE

                CHECK = True
                user = self.client.get_user(ctx.author.id)

                STATUS1 = False
                STATUS2 = False
                EVENT_NAME = []
                EVENT_NAME2 = None
                EVENT_LIST_DATA = []

                SAFE_CHECK = 0

                userName = ''
                for name in STRING[1:]:
                    userName += '{} '.format(name)

                userName = userName.replace('_', ' ')
                userName = userName.rstrip()

                for value in LIST1:
                    if value['user_id'] == ctx.author.id or value['user_rsn'] == userName:
                        STATUS1 = True

                if not STATUS1:
                    for value2 in LIST2:
                        if value2['type'] >= 3:
                            STATUS2 = True
                            EVENT_NAME.append(value2['event_name'])
                            SUM = value2['participants'] + 1
                            EVENT_LIST_DATA.append({'id': value2['id'], 'type': value2['type'], 'sum': SUM})

                    if STATUS2:
                        while CHECK:
                            USERNAME = userName.replace(' ', '%20')
                            USER = hiscores_kc.Hiscores2V(USERNAME, LIST3, LIST4)
                            USERNAME = USERNAME.replace('%20', ' ')
                            if USER.status != 404:
                                if USER.getKc(EVENT_NAME[0]):
                                    CHECK = False
                                    stats_data = USER.getKc(EVENT_NAME[0])
                                    json_string = {'user_id': ctx.author.id, 'user_username': ctx.author.mention, 'user_rsn': userName}

                                    for value in EVENT_NAME:
                                        json_string.update({value: int(stats_data['kc'])})
                                        json_string.update({'{}_current'.format(value): int(stats_data['kc'])})

                                    await json_manager.create(path1, json_string)
                                    for event_data in EVENT_LIST_DATA:
                                        await json_manager.update(path2, 'id', event_data['id'], 'participants', event_data['sum'])

                                    path4 = c.GUILD_PATH['{}.ini'.format(self.name)].format(ctx.guild.id)
                                    role_id = await ini_manager.get_data('SECTION1', 'EVENT_ROLE', path4)
                                    role = await discord_manager.get_role(self.client, ctx.guild.id, int(role_id))

                                    if role:
                                        user = await discord_manager.get_member(self.client, ctx.guild.id, ctx.author.id)
                                        await user.add_roles(role, reason='{}'.format(c.DISCORD_MESSAGES['event_role_added']), atomic=True)

                                    await ctx.send(l.kc_tracker[guild_l]['msg_1'].format(USERNAME, server_config['events']))
                                else:
                                    SAFE_CHECK += 1
                                    if SAFE_CHECK >= 10:
                                        CHECK = False
                                        await user.send(l.kc_tracker[guild_l]['msg_error_1'])
                            else:
                                CHECK = False
                                await user.send(l.kc_tracker[guild_l]['msg_error_1'])
                    else:
                        await user.send(l.kc_tracker[guild_l]['msg_2'])
                else:
                    EVENT_STATUS = False
                    MEMBER_DATA = None
                    for MEMBER in LIST1:
                        if ctx.author.id == MEMBER['user_id']:
                            MEMBER_DATA = MEMBER

                    for EVENT in LIST2:
                        for key, value in MEMBER_DATA.items():
                            if (EVENT['type'] == 3 or EVENT['type'] == 4) and key == EVENT['event_name']:
                                EVENT_STATUS = True

                            for index2, event_name in enumerate(LIST4):
                                if event_name == EVENT['event_name']:
                                    EVENT_NAME2 = LIST3[index2]

                        if not EVENT_STATUS and (EVENT['type'] == 3 or EVENT['type'] == 4):
                            EVENT_STATUS = False
                            CHECK = True
                            while CHECK:
                                USERNAME = userName.replace(' ', '%20')
                                USER = hiscores_kc.Hiscores2V(USERNAME, LIST3, LIST4)
                                if USER.status != 404:
                                    if USER.getKc(EVENT['event_name']):
                                        USER_STATS = USER.getKc(EVENT['event_name'])
                                        CHECK = False
                                        target_keys = ['{}'.format(EVENT['event_name']), '{}_current'.format(EVENT['event_name'])]
                                        target_values = [int(USER_STATS['kc']), int(USER_STATS['kc'])]
                                        await json_manager.update(path1, 'user_id', ctx.author.id, target_keys, target_values)
                                        await user.send(l.kc_tracker[guild_l]['msg_6'].format(EVENT_NAME2))

                                        for value2 in LIST2:
                                            if value2['type'] >= 3:
                                                EVENT_NAME.append(value2['event_name'])
                                                SUM = value2['participants'] + 1
                                                EVENT_LIST_DATA.append({'id': value2['id'], 'type': value2['type'], 'sum': SUM})

                                        for event_data in EVENT_LIST_DATA:
                                            await json_manager.update(path2, 'id', event_data['id'], 'participants', event_data['sum'])

                                    else:
                                        SAFE_CHECK += 1
                                        if SAFE_CHECK >= 10:
                                            CHECK = False
                                            await user.send(l.kc_tracker[guild_l]['msg_error_1'])
                                else:
                                    CHECK = False
                                    await user.send(l.kc_tracker[guild_l]['msg_error_1'])
                        else:
                            EVENT_STATUS = False
                    await user.send(l.kc_tracker[guild_l]['msg_7'])
            else:
                await ctx.send(l.kc_tracker[guild_l]['msg_badformat_2'].format(ctx.author.mention))
        except Exception as error:
            await exception.error(error)

    async def fun_kcupdate(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            guild_t = await origin.get_region(ctx.guild.id)
            path1 = c.GUILD_PATH['kc_tracker.json'].format(ctx.guild.id)
            path2 = c.GUILD_PATH['event.json'].format(ctx.guild.id)
            LIST1 = await json_manager.get_data(path1)
            LIST2 = await json_manager.get_data(path2)
            LIST3 = self.NAME
            LIST4 = self.PRE

            CHECK = True
            user = self.client.get_user(ctx.author.id)
            guild_current = await server_timer.get_current_time(guild_t)

            STATUS1 = False
            STATUS2 = False
            EVENT_NAME = []

            SAFE_CHECK = 0
            MEMBER = None
            userName = ''

            for value in LIST1:
                if value['user_id'] == ctx.author.id:
                    STATUS1 = True
                    userName = value['user_rsn']
                    MEMBER = value

            if STATUS1:
                for value2 in LIST2:
                    if value2['type'] == 3 or value2['type'] == 4:
                        STATUS2 = True
                        EVENT_NAME.append(value2['event_name'])

                if STATUS2:
                    while CHECK:
                        USERNAME = userName.replace(' ', '%20')
                        USER = hiscores_kc.Hiscores2V(USERNAME, LIST3, LIST4)
                        if USER.status != 404:
                            if USER.getKc(EVENT_NAME[0]):
                                CHECK = False
                                stats_data = USER.getKc(EVENT_NAME[0])
                                for value in EVENT_NAME:
                                    await json_manager.update(path1, 'user_id', ctx.author.id, '{}_current'.format(value), int(stats_data['kc']))
                                    client_message = 'Guild id: {} | Event: {} | RSN: {} | Registration KC: {} | Current KC: {} | Guild time: {} | Status: {}'.format(ctx.guild.id, value, userName, MEMBER[value], stats_data['kc'], guild_current.strftime('%H:%M'), 'KC self update')
                                    await console_interface.console_message('KC self update', client_message)

                                await user.send(l.kc_tracker[guild_l]['msg_success_4'])
                            else:
                                SAFE_CHECK += 1
                                if SAFE_CHECK >= 10:
                                    CHECK = False
                                    await user.send(l.kc_tracker[guild_l]['msg_error_3'])
                        else:
                            CHECK = False
                            await user.send(l.kc_tracker[guild_l]['msg_error_4'].format(userName))
                else:
                    await user.send(l.kc_tracker[guild_l]['msg_2'])
            else:
                await user.send(l.kc_tracker[guild_l]['msg_error_5'])
        except Exception as error:
            await exception.error(error)

    async def fun_kcrank(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            path = c.CLIENT_PATH['guild'] + str(ctx.guild.id) + c.CLIENT_JSON['server']
            path1 = c.GUILD_PATH['{}.ini'.format(self.name)].format(ctx.guild.id)
            path2 = c.GUILD_PATH['event.json'].format(ctx.guild.id)
            path3 = c.GUILD_PATH['kc_tracker.json'].format(ctx.guild.id)
            ini = await ini_manager.get_ini(path1)
            LIST1 = self.PNG
            LIST2 = self.PRE
            INFO_PANEL_IMAGE = self.INFO_PANEL_IMAGE
            INFO_PANEL_FIRST_IMAGE = self.INFO_PANEL_FIRST_IMAGE
            INFO_PANEL_SECOND_IMAGE = self.INFO_PANEL_SECOND_IMAGE
            INFO_PANEL_THIRD_IMAGE = self.INFO_PANEL_THIRD_IMAGE
            FIRST_COLOR = (246, 151, 2)
            SECOND_COLOR = (218, 218, 218)
            THIRD_COLOR = (255, 72, 0)
            DEFAULT_COLOR = (255, 0, 0)
            FONT_PATH = self.FONT_PATH
            INFO_PANEL_OBJECT = None
            RANK = 0
            sum = None

            CHANNEL_PERMISSIONS = int(ini['CHANNEL_PERMISSIONS']['STATUS'])
            server_config = await json_manager.get_json(path)
            CHANNEL_STATUS = True

            if CHANNEL_PERMISSIONS == 1:
                pass
            else:
                if ctx.message.channel.id == server_config['chat0']:
                    CHANNEL_STATUS = False

            if CHANNEL_STATUS:
                STRING = str(ctx.message.content).split(' ')

                def get_id(data_value):
                    return int(data_value.get('sum'))

                if len(STRING) == 1:
                    user = self.client.get_user(ctx.author.id)
                else:
                    DCID = await origin.find_and_replace(STRING[1])
                    user = self.client.get_user(DCID)

                TEMP_DATA = await json_manager.get_data(path2)
                DATA1 = []
                DATA2 = await json_manager.get_data(path3)
                DATA3 = []

                STATUS = None

                for value in TEMP_DATA:
                    if value['type'] >= 3:
                        DATA1.append(value)

                if DATA1:
                    for index, data in enumerate(DATA1):
                        if DATA2:
                            for index2, data2 in enumerate(DATA2):
                                for key, value in data2.items():
                                    if str(data['event_name']) == str(key):
                                        sum = data2['{}_current'.format(key)] - data2[key]
                                        DATA3.append({'user_rsn': data2['user_rsn'], 'user_id': data2['user_id'], 'sum': sum})
                                        for index3, value3 in enumerate(LIST2):
                                            if str(value3) == str(key):
                                                INFO_PANEL_OBJECT = LIST1[index3]

                            DATA3.sort(key=get_id, reverse=True)
                            for index3, data3 in enumerate(DATA3):
                                RANK += 1

                                if RANK == 1:
                                    PLACE_IMAGE = INFO_PANEL_FIRST_IMAGE
                                    PLACE_COLOR = FIRST_COLOR
                                elif RANK == 2:
                                    PLACE_IMAGE = INFO_PANEL_SECOND_IMAGE
                                    PLACE_COLOR = SECOND_COLOR
                                elif RANK == 3:
                                    PLACE_IMAGE = INFO_PANEL_THIRD_IMAGE
                                    PLACE_COLOR = THIRD_COLOR
                                else:
                                    PLACE_IMAGE = INFO_PANEL_IMAGE
                                    PLACE_COLOR = DEFAULT_COLOR

                                if hasattr(user, 'id'):
                                    if user.id == data3['user_id']:
                                        with Image.open(PLACE_IMAGE).convert('RGBA') as im:
                                            with Image.open(INFO_PANEL_OBJECT).convert('RGBA') as im2:

                                                size1 = im.size
                                                size2 = im2.size
                                                y = int(size1[1] / 2) - int(size2[1] / 2)
                                                im.paste(im2, (160, y), im2)

                                                draw = ImageDraw.Draw(im)
                                                font = ImageFont.truetype(FONT_PATH, 16)
                                                draw.text((15, y + 5), l.kc_tracker[guild_l]['configuration']['rsn'], PLACE_COLOR, font=font)
                                                draw.text((15, y + 21), l.kc_tracker[guild_l]['configuration']['rank'], PLACE_COLOR, font=font)
                                                draw.text((15, y + 37), l.kc_tracker[guild_l]['configuration']['kc'], PLACE_COLOR, font=font)

                                                draw.text((75 if guild_l == 'LT' else 60, y + 5), '{}'.format(data3['user_rsn']), (255, 255, 255), font=font)
                                                draw.text((95 if guild_l == 'LT' else 70, y + 21), '{}'.format(RANK), (255, 255, 255), font=font)
                                                draw.text((35, y + 37), '{}'.format(locale.format_string('%d', data3['sum'], grouping=True)), (255, 255, 255), font=font)

                                                TEMP_FILE = '{}_{}_{}.png'.format(data3['user_rsn'], data['event_name'], sum)
                                                im.save(TEMP_FILE, 'PNG')
                                                rank = open(TEMP_FILE, 'rb')
                                                await ctx.send(file=discord.File(rank))
                                                rank.close()
                                                await file_manager.delete_file(TEMP_FILE)
                                                STATUS = True

                            if not STATUS:
                                await ctx.send(l.kc_tracker[guild_l]['msg_error_6'].format(ctx.author.mention))
                            RANK = 0
                            DATA3.clear()
                        else:
                            await ctx.send(l.kc_tracker[guild_l]['msg_4'])
                else:
                    await ctx.send(l.kc_tracker[guild_l]['msg_5'])
            else:
                await ctx.send(l.module_permissions[guild_l]['msg_restricted'])
        except Exception as error:
            await exception.error(error)

    async def fun_kcstats(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            path = c.CLIENT_PATH['guild'] + str(ctx.guild.id) + c.CLIENT_JSON['server']
            server_config = await json_manager.get_json(path)

            path1 = c.GUILD_PATH['{}.ini'.format(self.name)].format(ctx.guild.id)
            ini = await ini_manager.get_ini(path1)
            CHANNEL_PERMISSIONS = int(ini['CHANNEL_PERMISSIONS']['STATUS'])

            CHANNEL_STATUS = True

            if CHANNEL_PERMISSIONS == 1:
                pass
            else:
                if ctx.message.channel.id == server_config['chat0']:
                    CHANNEL_STATUS = False

            if CHANNEL_STATUS:
                path2 = c.GUILD_PATH['event.json'].format(ctx.guild.id)
                path3 = c.GUILD_PATH['kc_tracker.json'].format(ctx.guild.id)
                LIST1 = self.ICON
                LIST2 = self.PRE
                LIST3 = self.NAME
                IMAGE = None
                EVENT_NAME = None

                await origin.get_locale()

                TEMP_DATA = await json_manager.get_data(path2)
                DATA1 = []
                DATA2 = await json_manager.get_data(path3)
                DATA3 = []

                for value in TEMP_DATA:
                    if value['type'] >= 3:
                        DATA1.append(value)

                def get_id(INFO):
                    return int(INFO.get('sum'))

                if DATA1:
                    for data1 in DATA1:
                        if DATA2:
                            for data2 in DATA2:
                                for key, value in data2.items():
                                    if str(key) == str(data1['event_name']):
                                        sum = data2['{}_current'.format(key)]-data2[key]
                                        DATA3.append({'user_username': data2['user_username'], 'user_rsn': data2['user_rsn'], 'sum': sum})
                                        EVENT_NAME = str(data1['event_name'])

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

                            path4 = c.ORIGIN_PATH['embed.tracker.json']
                            json_string = await json_manager.get_json(path4)
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

                                        STRING += l.kc_tracker[guild_l]['configuration']['total_kc'].format(locale.format_string('%d', SUM, grouping=True))
                                        new_json_string['data'].append({
                                            'name{}'.format(key): value['name'].format('\u200D'),
                                            'value{}'.format(key): str(value['value']).format(STRING)
                                        })
                                    else:
                                        STRING += l.kc_tracker[guild_l]['configuration']['total_kc'].format(locale.format_string('%d', SUM, grouping=True))
                                        new_json_string['data'].append({
                                            'name{}'.format(key): value['name'],
                                            'value{}'.format(key): str(value['value']).format(ctx.guild.name)
                                        })

                            await embed_creator.create_embed(ctx, discord.Color.dark_red(), False, ctx.guild.icon_url, IMAGE, l.kc_tracker[guild_l]['embed_3'].format(ctx.guild.name, EVENT_NAME), new_json_string['data'], False)
                            DATA3.clear()
                        else:
                            await ctx.send(l.kc_tracker[guild_l]['msg_4'])
                else:
                    await ctx.send(l.kc_tracker[guild_l]['msg_5'])
            else:
                await ctx.send(l.module_permissions[guild_l]['msg_restricted'])
        except Exception as error:
            await exception.error(error)

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    @tasks.loop(count=1)
    async def variable_init(self):
        try:
            path_global = c.GUILD_PATH['{}_g.ini'.format(self.name)]
            ini = await ini_manager.get_ini(path_global)

            self.PRE = await json_manager.get_ini_list(path_global, 'CONSTANT2', 'PRE')
            self.NAME = await json_manager.get_ini_list(path_global, 'CONSTANT1', 'NAME')
            self.ICON = await json_manager.get_ini_list(path_global, 'CONSTANT3', 'ICON')
            self.PNG = await json_manager.get_ini_list(path_global, 'CONSTANT5', 'PNG')
            self.INFO_PANEL_IMAGE = ini['CONSTANT5']['INFO_PANEL']
            self.INFO_PANEL_FIRST_IMAGE = ini['CONSTANT5']['INFO_PANEL_FIRST']
            self.INFO_PANEL_SECOND_IMAGE = ini['CONSTANT5']['INFO_PANEL_SECOND']
            self.INFO_PANEL_THIRD_IMAGE = ini['CONSTANT5']['INFO_PANEL_THIRD']
            self.FONT_PATH = ini['CONSTANT5']['FONT']

            await console_interface.console_message(c.CLIENT_MESSAGES['variable_init'].format(self.name))
        except Exception as error:
            await exception.error(error)

    def __init__(self, client):
        self.PRE = None
        self.NAME = None
        self.ICON = None
        self.PNG = None
        self.INFO_PANEL_IMAGE = None
        self.INFO_PANEL_FIRST_IMAGE = None
        self.INFO_PANEL_SECOND_IMAGE = None
        self.INFO_PANEL_THIRD_IMAGE = None
        self.FONT_PATH = None

        self.variable_init.start()
        self.client = client

    @commands.command()
    async def kctracker(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_kctracker)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def addkcevent(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_addkcevent)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def removeallkc(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_removeallkc)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def akc(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_akc)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def kcupdate(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_kcupdate)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def kcrank(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_kcrank)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def kcstats(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_kcstats)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

def setup(client):
    client.add_cog(kc_tracker(client))