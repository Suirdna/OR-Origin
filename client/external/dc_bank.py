from client import exception, embed_creator, console_interface, discord_manager, ini_manager, json_manager, server_timer, logger, origin, permissions
from client.config import config as c, language as l
from discord.ext import commands, tasks
import discord, locale

class dc_bank(commands.Cog):
    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    name = 'dc_bank'

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    async def add_recipe(self, ctx, type):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            guild_t = await origin.get_region(ctx.guild.id)
            path = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
            target_keys = ['user_id', 'user_status']
            target_values = [ctx.author.id, c.USER_PERMISSIONS['dc_bank']]

            if await permissions.get_user_permission(path, target_keys, target_values) or ctx.author.id == ctx.guild.owner.id or ctx.author.id == c.CLIENT_ADMINISTRATION_ID:
                STRING = str(ctx.message.content).split(' ')
                if len(STRING) >= 2:
                    SUM_A = await origin.find_and_replace(STRING[1])
                    if str(SUM_A).isdigit():
                        path3 = c.GUILD_PATH['recipe.json'].format(ctx.guild.id)

                        await origin.get_locale()
                        guild_current = await server_timer.get_current_time(guild_t)

                        TEXT = ''
                        json_string = None

                        for data in STRING[2:]:
                            TEXT += '{} '.format(data)

                        if type == 0:
                            json_string = {'recipe': SUM_A, 'date': guild_current.strftime('%y.%m.%d | %H:%M'), 'reason': TEXT, 'type': 0}
                            await ctx.send(l.dc_bank[guild_l]['msg_success_3'].format(self.COINS2, locale.format_string('%d', SUM_A, grouping=True)))

                            client_message = 'Guild id: {} | Guild time: {} | Member id: {} | Sum: -{}'.format(ctx.guild.id, guild_current.strftime('%H:%M'), ctx.author.id, SUM_A)
                            await console_interface.console_message(c.CLIENT_MESSAGES['dc_bank_recipe_minus'], client_message)
                            await logger.log_event(ctx, 'dc_bank', c.CLIENT_MESSAGES['dc_bank_recipe_minus'], client_message)
                        elif type == 1:
                            json_string = {'recipe': SUM_A, 'date': guild_current.strftime('%y.%m.%d | %H:%M'), 'reason': TEXT, 'type': 1}
                            await ctx.send(l.dc_bank[guild_l]['msg_success_4'].format(self.COINS2, locale.format_string('%d', SUM_A, grouping=True)))

                            client_message = 'Guild id: {} | Guild time: {} | Member id: {} | Sum: +{}'.format(ctx.guild.id, guild_current.strftime('%H:%M'), ctx.author.id, SUM_A)
                            await console_interface.console_message(c.CLIENT_MESSAGES['dc_bank_recipe_plus'], client_message)
                            await logger.log_event(ctx, 'dc_bank', c.CLIENT_MESSAGES['dc_bank_recipe_plus'], client_message)
                        await json_manager.create(path3, json_string)
                    else:
                        if type == 0:
                            await ctx.send(l.dc_bank[guild_l]['msg_badformat_2'])
                        elif type == 1:
                            await ctx.send(l.dc_bank[guild_l]['msg_badformat_3'])
                else:
                    if type == 0:
                        await ctx.send(l.dc_bank[guild_l]['msg_info_2'])
                    elif type == 1:
                        await ctx.send(l.dc_bank[guild_l]['msg_info_3'])
            else:
                await ctx.author.send(l.user_permissions[guild_l]['msg_restricted_1'])
        except Exception as error:
            await exception.error(error)

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    @staticmethod
    async def fun_create(ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            guild_t = await origin.get_region(ctx.guild.id)
            path1 = c.GUILD_PATH['bank.json'].format(ctx.guild.id)

            if not await json_manager.get_status(path1, 'user_id', ctx.author.id):
                guild_current = await server_timer.get_current_time(guild_t)
                json_string = {'user_id': ctx.author.id, 'user_username': ctx.author.mention, 'donate': 0, 'bank': 0}
                await json_manager.create(path1, json_string)

                client_message = 'Guild id: {} | Guild time: {} | Member id: {}'.format(ctx.guild.id, guild_current.strftime('%H:%M'), ctx.author.id)
                await console_interface.console_message(c.CLIENT_MESSAGES['dc_bank_create'], client_message)
                await logger.log_event(ctx, 'dc_bank', c.CLIENT_MESSAGES['dc_bank_create'], client_message)

                await ctx.send(l.dc_bank[guild_l]['msg_success_1'])
            else:
                await ctx.send(l.dc_bank[guild_l]['msg_error_1'])
        except Exception as error:
            await exception.error(error)

    async def fun_bank(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            path1 = c.GUILD_PATH['bank.json'].format(ctx.guild.id)

            await origin.get_locale()

            DATA1 = await json_manager.get_data(path1)
            STATUS = False
            MEMBER = None

            for data in DATA1:
                if ctx.author.id == data['user_id']:
                    STATUS = True
                    MEMBER = data

            if STATUS:
                path3 = c.ORIGIN_PATH['embed.dc_bank.json']
                json_string = await json_manager.get_json(path3)
                new_json_string = {'data': []}

                for key, value in json_string[guild_l]['bank'].items():
                    if int(key) == 1:
                        new_json_string['data'].append({
                            'name{}'.format(key): value['name'].format(l.dc_bank[guild_l]['configuration']['extra_1']),
                            'value{}'.format(key): str(value['value']).format(
                                MEMBER['user_username'],
                                self.COINS1,
                                locale.format_string('%d', MEMBER['donate'], grouping=True),
                                self.COINS2, locale.format_string('%d', MEMBER['bank'], grouping=True)
                            )
                        })
                    else:
                        new_json_string['data'].append({
                            'name{}'.format(key): value['name'],
                            'value{}'.format(key): str(value['value'])
                        })

                await embed_creator.create_embed(ctx, discord.Color.gold(), False, ctx.guild.icon_url, self.BANK_ICON, l.dc_bank[guild_l]['embed_1'].format(ctx.guild.name), new_json_string['data'], False)
            else:
                await ctx.send(l.dc_bank[guild_l]['msg_error_2'])
        except Exception as error:
            await exception.error(error)

    async def fun_donate(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            STRING = str(ctx.message.content).split(' ')
            if len(STRING) == 2:
                SUM_A = await origin.find_and_replace(STRING[1])
                if str(SUM_A).isdigit():
                    path1 = c.CLIENT_PATH['guild'] + str(ctx.guild.id) + c.CLIENT_JSON['server']
                    path2 = c.GUILD_PATH['{}.ini'.format(self.name)].format(ctx.guild.id)
                    path3 = c.GUILD_PATH['bank.json'].format(ctx.guild.id)

                    server_config = await json_manager.get_json(path1)

                    ini = await ini_manager.get_ini(path2)
                    await origin.get_locale()

                    if await json_manager.get_status(path3, 'user_id', ctx.author.id):
                        channel = await discord_manager.get_channel(self.client, ctx.guild.id, server_config['dc_bank'])
                        if channel:
                            if ini['SECTION1']['ADMIN']:
                                await channel.send(l.dc_bank[guild_l]['msg_1'].format(ini['SECTION1']['ADMIN'], ctx.author.mention, self.COINS2, locale.format_string('%d', SUM_A, grouping=True), ctx.author.id, SUM_A))
                                await ctx.send(l.dc_bank[guild_l]['msg_2'].format(ctx.author.mention))
                            else:
                                await ctx.send(l.dc_bank[guild_l]['msg_no_config_1'].format(ctx.author.mention))
                        else:
                            await ctx.send(l.dc_bank[guild_l]['msg_no_config_2'].format(ctx.author.mention))
                    else:
                        await ctx.send(l.dc_bank[guild_l]['msg_error_2'])
                else:
                    await ctx.send(l.dc_bank[guild_l]['msg_badformat_1'].format(ctx.author.mention))
            else:
                await ctx.send(l.dc_bank[guild_l]['msg_info_1'])
        except Exception as error:
            await exception.error(error)

    async def fun_banktop(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            path2 = c.GUILD_PATH['bank.json'].format(ctx.guild.id)

            await origin.get_locale()

            DATA = await json_manager.get_data(path2)

            def get_id(INFO):
                return int(INFO.get('donate'))

            DATA.sort(key=get_id, reverse=True)

            path3 = c.ORIGIN_PATH['embed.dc_bank.json']
            json_string = await json_manager.get_json(path3)
            new_json_string = {'data': []}
            STRING = ''

            for key, value in json_string[guild_l]['banktop'].items():
                if DATA:
                    if int(key) == 1:
                        for index, data in enumerate(DATA):
                            index = index + 1
                            if index <= 4:
                                if index == 1:
                                    title = ':first_place: {}'.format(l.DISCORD_TOP[guild_l][index - 1])
                                elif index == 2:
                                    title = ':second_place: {}'.format(l.DISCORD_TOP[guild_l][index - 1])
                                elif index == 3:
                                    title = ':third_place: {}'.format(l.DISCORD_TOP[guild_l][index - 1])
                                else:
                                    title = '{}'.format(l.DISCORD_TOP[guild_l][index])

                                STRING += l.dc_bank[guild_l]['configuration']['top_gp_2'].format(title, data['user_username'], self.COINS2, locale.format_string('%d', data['donate'], grouping=True))

                        new_json_string['data'].append({
                            'name{}'.format(key): value['name'].format('\u200D'),
                            'value{}'.format(key): str(value['value']).format(STRING)
                        })
                    else:
                        new_json_string['data'].append({
                            'name{}'.format(key): value['name'],
                            'value{}'.format(key): str(value['value']).format(ctx.guild.name)
                        })
                else:
                    if int(key) == 1:
                        new_json_string['data'].append({
                            'name1': value['name'].format('Nėra'),
                            'value1': l.dc_bank[guild_l]['configuration']['extra_2']
                        })
                    else:
                        new_json_string['data'].append({
                            'name{}'.format(key): value['name'],
                            'value{}'.format(key): str(value['value']).format(ctx.guild.name)
                        })

            await embed_creator.create_embed(ctx, discord.Color.gold(), False, ctx.guild.icon_url, self.BANK_ICON, l.dc_bank[guild_l]['embed_1'].format(ctx.guild.name), new_json_string['data'], False)
        except Exception as error:
            await exception.error(error)

    async def fun_dcbank(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            path2 = c.GUILD_PATH['bank.json'].format(ctx.guild.id)
            path3 = c.GUILD_PATH['recipe.json'].format(ctx.guild.id)

            await origin.get_locale()

            sum = 0
            minus = 0
            plus = 0

            DATA1 = await json_manager.get_data(path2)

            for data1 in DATA1:
                sum += int(data1['donate'])

            DATA2 = await json_manager.get_data(path3)

            for data2 in DATA2:
                if int(data2['type']) == 0:
                    minus += int(data2['recipe'])
                else:
                    plus += int(data2['recipe'])

            SUM = (sum - minus) + plus

            path3 = c.ORIGIN_PATH['embed.dc_bank.json']
            json_string = await json_manager.get_json(path3)
            new_json_string = {'data': []}

            for key, value in json_string[guild_l]['dcbank'].items():
                if int(key) == 1:
                    new_json_string['data'].append({
                        'name{}'.format(key): value['name'].format(l.dc_bank[guild_l]['configuration']['extra_3'].format(ctx.guild.name)),
                        'value{}'.format(key): str(value['value']).format(self.COINS1, locale.format_string('%d', SUM, grouping=True))
                    })
                else:
                    new_json_string['data'].append({
                        'name{}'.format(key): value['name'],
                        'value{}'.format(key): str(value['value']).format(ctx.guild.name)
                    })

            await embed_creator.create_embed(ctx, discord.Color.gold(), False, ctx.guild.icon_url, self.BANK_ICON, l.dc_bank[guild_l]['embed_1'].format(ctx.guild.name), new_json_string['data'], False)
        except Exception as error:
            await exception.error(error)

    async def fun_recipe(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            path2 = c.GUILD_PATH['recipe.json'].format(ctx.guild.id)

            await origin.get_locale()

            DATA = await json_manager.get_data(path2)
            DATA.reverse()

            if DATA:
                count = 0
                STRING = ''

                path3 = c.ORIGIN_PATH['embed.dc_bank.json']
                json_string = await json_manager.get_json(path3)
                new_json_string = {'data': []}

                for key, value in json_string[guild_l]['recipe'].items():
                    for data in DATA:
                        if count <= 4:
                            if data['type'] == 1:
                                STRING += l.dc_bank[guild_l]['configuration']['extra_recipe_1'].format(
                                    self.COINS2, locale.format_string('%d', data['recipe'], grouping=True),
                                    l.dc_bank[guild_l]['configuration']['extra_recipe_2'].format(data['reason']) if data['reason'] != '' else l.dc_bank[guild_l]['configuration']['extra_recipe_3'],
                                    data['date']
                                )
                            else:
                                STRING += l.dc_bank[guild_l]['configuration']['extra_recipe_0'].format(
                                    self.COINS2, locale.format_string('%d', data['recipe'], grouping=True),
                                    l.dc_bank[guild_l]['configuration']['extra_recipe_2'].format(data['reason']) if data['reason'] != '' else l.dc_bank[guild_l]['configuration']['extra_recipe_3'],
                                    data['date']
                                )

                            count += 1

                    new_json_string['data'].append({
                        'name1': value['name'].format(l.dc_bank[guild_l]['configuration']['extra_recipe_4'].format(ctx.guild.name)),
                        'value1': str(value['value']).format(STRING)
                    })

                await embed_creator.create_embed(ctx, discord.Color.gold(), False, ctx.guild.icon_url, self.BANK_ICON, l.dc_bank[guild_l]['embed_1'].format(ctx.guild.name), new_json_string['data'], False)
            else:
                await ctx.send(l.dc_bank[guild_l]['msg_3'])
        except Exception as error:
            await exception.error(error)

    async def fun_pay(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            path = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
            target_keys1 = ['user_id', 'user_status']
            target_values1 = [ctx.author.id, c.USER_PERMISSIONS['dc_bank']]

            if await permissions.get_user_permission(path, target_keys1, target_values1) or ctx.author.id == ctx.guild.owner.id or ctx.author.id == c.CLIENT_ADMINISTRATION_ID:
                path1 = c.GUILD_PATH['{}.ini'.format(self.name)].format(ctx.guild.id)
                path3 = c.GUILD_PATH['bank.json'].format(ctx.guild.id)

                await origin.get_locale()
                ini = await ini_manager.get_ini(path1)

                STRING = str(ctx.message.content).split(' ')
                STATUS = False
                MEMBER = None
                DATA = await json_manager.get_json(path3)

                for data in DATA:
                    if data['user_id'] == int(STRING[1]):
                        STATUS = True
                        MEMBER = data

                if STATUS:
                    SUM = int(MEMBER['donate']) + int(STRING[2])
                    SUM2 = int(MEMBER['bank']) + int(STRING[2])

                    target_keys2 = ['donate', 'bank']
                    target_values2 = [SUM, SUM2]

                    await json_manager.update(path3, 'user_id', MEMBER['user_id'], target_keys2, target_values2)

                    user = self.client.get_user(MEMBER['user_id'])
                    await ctx.send(l.dc_bank[guild_l]['msg_success_2'].format(self.COINS2, (locale.format_string('%d', int(STRING[2]), grouping=True))))
                    await user.send(l.dc_bank[guild_l]['msg_4'].format(locale.format_string('%d', int(STRING[2]), grouping=True), locale.format_string('%d', int(SUM2), grouping=True)))

                    server = await discord_manager.get_server(self.client, ctx.guild.id)
                    user = await discord_manager.get_member(self.client, ctx.guild.id, MEMBER['user_id'])

                    if SUM >= int(ini['SECTION3']['DISCORD_TOP_1_COUNT']):  # DISCORD_TOP_1
                        role_set = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION2']['DISCORD_TOP_1'])) # DISCORD_TOP_1
                        role_del = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION2']['DISCORD_TOP_2'])) # DISCORD_TOP_2
                        await user.add_roles(role_set, reason='{}'.format(c.DISCORD_MESSAGES['dc_bank_role_add']), atomic=True)
                        await user.remove_roles(role_del, reason='{}'.format(c.DISCORD_MESSAGES['dc_bank_role_remove']), atomic=True)
                    elif SUM >= int(ini['SECTION3']['DISCORD_TOP_2_COUNT']):  # DISCORD_TOP_2
                        role_set = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION2']['DISCORD_TOP_2'])) # DISCORD_TOP_2
                        role_del = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION2']['DISCORD_TOP_3'])) # DISCORD_TOP_3
                        await user.add_roles(role_set, reason='{}'.format(c.DISCORD_MESSAGES['dc_bank_role_add']), atomic=True)
                        await user.remove_roles(role_del, reason='{}'.format(c.DISCORD_MESSAGES['dc_bank_role_remove']), atomic=True)
                    elif SUM >= int(ini['SECTION3']['DISCORD_TOP_3_COUNT']):  # DISCORD_TOP_3
                        role_set = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION2']['DISCORD_TOP_3'])) # DISCORD_TOP_3
                        role_del = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION2']['DISCORD_TOP_4'])) # DISCORD_TOP_4
                        await user.add_roles(role_set, reason='{}'.format(c.DISCORD_MESSAGES['dc_bank_role_add']), atomic=True)
                        await user.remove_roles(role_del, reason='{}'.format(c.DISCORD_MESSAGES['dc_bank_role_remove']), atomic=True)
                    elif SUM >= int(ini['SECTION3']['DISCORD_TOP_4_COUNT']):  # DISCORD_TOP_4
                        role_set = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION2']['DISCORD_TOP_4'])) # DISCORD_TOP_4
                        role_del = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION2']['DISCORD_TOP_5'])) # DISCORD_TOP_5
                        await user.add_roles(role_set, reason='{}'.format(c.DISCORD_MESSAGES['dc_bank_role_add']), atomic=True)
                        await user.remove_roles(role_del, reason='{}'.format(c.DISCORD_MESSAGES['dc_bank_role_remove']), atomic=True)
                    elif SUM >= int(ini['SECTION3']['DISCORD_TOP_5_COUNT']):  # DISCORD_TOP_5
                        role_set = await discord_manager.get_role(self.client, ctx.guild.id, int(ini['SECTION2']['DISCORD_TOP_5'])) # DISCORD_TOP_5
                        await user.add_roles(role_set, reason='{}'.format(c.DISCORD_MESSAGES['dc_bank_role_add']), atomic=True)

                    client_message = 'Guild id: {} | Seller id: {} | Sum: {} | Buyer id: {} | Sum: {}'.format(ctx.guild.id, ctx.author.id, STRING[2], STRING[1], SUM2)
                    await console_interface.console_message(c.CLIENT_MESSAGES['dc_bank_buy'], client_message)
                    await logger.log_event(ctx, 'dc_bank', c.CLIENT_MESSAGES['dc_bank_buy'], client_message)

                    path4 = c.CLIENT_PATH['guild'] + str(ctx.guild.id) + c.CLIENT_JSON['server']
                    server_config = await json_manager.get_json(path4)

                    if server_config['chat0']:
                        CHANNEL1 = server.get_channel(server_config['chat0'])
                        await CHANNEL1.send(l.dc_bank[guild_l]['msg_post_1'].format(user.mention, ctx.guild.name, l.dc_bank[guild_l]['msg_post_1_extra'].format(server_config['thanks']) if server_config['thanks'] else ''))

                    if server_config['chat1']:
                        CHANNEL2 = server.get_channel(server_config['chat1'])
                        await CHANNEL2.send(l.dc_bank[guild_l]['msg_post_1'].format(user.mention, ctx.guild.name, l.dc_bank[guild_l]['msg_post_1_extra'].format(server_config['thanks']) if server_config['thanks'] else ''))

                    if server_config['thanks']:
                        CHANNEL3 = server.get_channel(server_config['thanks'])
                        message = await CHANNEL3.send(l.dc_bank[guild_l]['msg_post_2'].format(user.mention, ctx.guild.name, locale.format_string('%d', int(STRING[2]), grouping=True)))
                        await message.add_reaction(l.DISCORD_EMOTE['thanks'])
                else:
                    await ctx.send(l.dc_bank[guild_l]['msg_error_3'].format(STRING[1]))
            else:
                await ctx.author.send(l.user_permissions[guild_l]['msg_restricted_1'])
        except Exception as error:
            await exception.error(error)

    async def fun_minus(self, ctx):
        try:
            await self.add_recipe(ctx, 0)
        except Exception as error:
            await exception.error(error)

    async def fun_plus(self, ctx):
        try:
            await self.add_recipe(ctx, 1)
        except Exception as error:
            await exception.error(error)

    async def fun_remote(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            path = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
            target_keys = ['user_id', 'user_status']
            target_values = [ctx.author.id, c.USER_PERMISSIONS['dc_bank']]

            if await permissions.get_user_permission(path, target_keys, target_values) or ctx.author.id == ctx.guild.owner.id or ctx.author.id == c.CLIENT_ADMINISTRATION_ID:
                STRING = str(ctx.message.content).split(' ')
                if len(STRING) == 2:
                    DCID = await origin.find_and_replace(STRING[1])
                    if str(DCID).isdigit():
                        path2 = c.GUILD_PATH['bank.json'].format(ctx.guild.id)
                        user = await discord_manager.get_member(self.client, ctx.guild.id, DCID)

                        if user:
                            if not await json_manager.get_status(path2, 'user_id', DCID):
                                json_string = {'user_id': user.id, 'user_username': user.mention, 'donate': 0, 'bank': 0}
                                await json_manager.create(path2, json_string)

                                client_message = 'Guild id: {} | Creator id: {} | Member id: {}'.format(ctx.guild.id, ctx.author.id, DCID)
                                await console_interface.console_message(c.CLIENT_MESSAGES['dc_bank_remote_create'], client_message)
                                await logger.log_event(ctx, 'dc_bank', c.CLIENT_MESSAGES['dc_bank_remote_create'], client_message)

                                await ctx.send(l.dc_bank[guild_l]['msg_success_5'].format(user.mention))
                            else:
                                await ctx.send(l.dc_bank[guild_l]['msg_error_4'].format(user.mention))
                        else:
                            await ctx.send(l.dc_bank[guild_l]['msg_error_5'].format(DCID, ctx.guild.name))
                    else:
                        await ctx.send(l.dc_bank[guild_l]['msg_badformat_4'].format(ctx.author.mention))
                else:
                    await ctx.send(l.dc_bank[guild_l]['msg_info_4'].format(ctx.author.mention))
            else:
                await ctx.author.send(l.user_permissions[guild_l]['msg_restricted_1'])
        except Exception as error:
            await exception.error(error)

    async def fun_bankdata(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            path = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
            target_keys = ['user_id', 'user_status']
            target_values = [ctx.author.id, c.USER_PERMISSIONS['dc_bank']]

            if await permissions.get_user_permission(path, target_keys, target_values) or ctx.author.id == ctx.guild.owner.id or ctx.author.id == c.CLIENT_ADMINISTRATION_ID:
                STRING = str(ctx.message.content).split(' ')
                if len(STRING) == 2:
                    DCID = await origin.find_and_replace(STRING[1])
                    if str(DCID).isdigit():
                        path3 = c.GUILD_PATH['bank.json'].format(ctx.guild.id)

                        await origin.get_locale()

                        STATUS = False
                        MEMBER = None

                        DATA = await json_manager.get_data(path3)

                        for data in DATA:
                            if DCID == data['user_id']:
                                STATUS = True
                                MEMBER = data

                        if STATUS:
                            path4 = c.ORIGIN_PATH['embed.dc_bank.json']
                            json_string = await json_manager.get_json(path4)
                            new_json_string = {'data': []}
                            for key, value in json_string[guild_l]['bankdata'].items():
                                new_json_string['data'].append({
                                    'name{}'.format(key): str(value['name']).format(l.dc_bank[guild_l]['configuration']['extra_1']),
                                    'value{}'.format(key): str(value['value']).format(
                                        MEMBER['user_username'], self.COINS2,
                                        locale.format_string('%d', int(MEMBER['donate']), grouping=True),
                                        self.COINS1, locale.format_string('%d', int(MEMBER['bank']), grouping=True)
                                    )
                                })

                            await embed_creator.create_embed(ctx, discord.Color.gold(), False, ctx.guild.icon_url, False, l.dc_bank[guild_l]['embed_1'].format(ctx.guild.name), new_json_string['data'], False)
                        else:
                            await ctx.send(l.dc_bank[guild_l]['msg_error_3'].format(STRING[1]))
                    else:
                        await ctx.send(l.dc_bank[guild_l]['msg_badformat_5'].format(ctx.author.mention))
                else:
                    await ctx.send(l.dc_bank[guild_l]['msg_info_5'].format(ctx.author.mention))
            else:
                await ctx.author.send(l.user_permissions[guild_l]['msg_restricted_1'])
        except Exception as error:
            await exception.error(error)

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    @tasks.loop(count=1)
    async def variable_init(self):
        try:
            path_global = c.GUILD_PATH['{}_g.ini'.format(self.name)]
            ini = await ini_manager.get_ini(path_global)

            self.BANK_ICON = ini['CONSTANT1']['BANK_ICON']
            self.RECIPE_ICON = ini['CONSTANT1']['RECIPE_ICON']
            self.COINS1 = ini['CONSTANT2']['COINS1']
            self.COINS2 = ini['CONSTANT2']['COINS2']

            await console_interface.console_message(c.CLIENT_MESSAGES['variable_init'].format(self.name))
        except Exception as error:
            await exception.error(error)

    def __init__(self, client):
        self.BANK_ICON = None
        self.RECIPE_ICON = None
        self.COINS1 = None
        self.COINS2 = None

        self.variable_init.start()
        self.client = client

    @commands.command()
    async def create(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_create, typef=True)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def bank(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_bank, typef=True)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def donate(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_donate, typef=True)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def banktop(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_banktop, typef=True)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def dcbank(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_dcbank, typef=True)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def recipe(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_recipe, typef=True)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def pay(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_pay, typef=True)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def minus(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_minus, typef=True)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def plus(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_plus, typef=True)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def remote(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_remote, typef=True)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def bankdata(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_bankdata, typef=True)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

def setup(client):
    client.add_cog(dc_bank(client))