from client import exception, embed_creator, discord_manager, ini_manager, json_manager, permissions, server_timer, origin
from client.external.hiscores import hiscores_xp
from client.config import config as c, language as l
from discord.ext import commands
import discord

class rsn_register(commands.Cog):
    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    name = 'rsn_register'

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    @staticmethod
    async def rsn_registration(client, message):
        try:
            guild_l = await origin.get_language(message.guild.id)
            guild_t = await origin.get_region(message.guild.id)
            path1 = c.GUILD_PATH['rsn_register.ini'].format(message.guild.id)
            ini = await ini_manager.get_ini(path1)

            CHECK = True
            SAFE_CHECK = 0
            userName = message.content
            userName = userName.lstrip()
            userName = userName.rstrip()

            time = await server_timer.get_current_time(guild_t)
            time = time.strftime('%y.%m.%d %H:%M:%S')

            if int(ini['STATUS']['STATUS']) == 2:
                role_id = int(ini['SECTION1']['ROLE'])
                if role_id:
                    role = await discord_manager.get_role(client, message.guild.id, role_id)
                    if role:
                        path2 = c.GUILD_PATH['rsn.json'].format(message.guild.id)
                        user = await discord_manager.get_member(client, message.guild.id, message.author.id)
                        while CHECK:
                            USERNAME = userName.replace(' ', '%20')
                            USER = hiscores_xp.Hiscores(USERNAME, 'N')
                            if USER.status != 404:
                                if hasattr(USER, 'stats'):
                                    CHECK = False
                                    if not await json_manager.get_status(path2, 'user_id', message.author.id):
                                        json_string = {'user_id': message.author.id, 'rsn': [message.content], 'time': ['{}'.format(time)]}
                                        await json_manager.create(path2, json_string)
                                        await user.add_roles(role, reason='{}'.format(c.DISCORD_MESSAGES['role_added']), atomic=True)
                                        await user.edit(nick='{}'.format(message.content), reason='{}'.format(c.DISCORD_MESSAGES['role_added']))

                                        await user.send(l.rsn_register[guild_l]['msg_success_1'].format(userName))
                                    else:
                                        DATA = await json_manager.get_json(path2)
                                        MASSIVE = []
                                        TIME_MASSIVE = []
                                        for data in DATA:
                                            if data['user_id'] == message.author.id:
                                                MASSIVE = data['rsn']
                                                MASSIVE.append(message.content)
                                                TIME_MASSIVE = data['time']
                                                TIME_MASSIVE.append(time)

                                        target_keys = ['rsn', 'time']
                                        target_values = [MASSIVE, TIME_MASSIVE]
                                        await json_manager.update(path2, 'user_id', message.author.id, target_keys, target_values)
                                        await user.add_roles(role, reason='{}'.format(c.DISCORD_MESSAGES['role_added']), atomic=True)
                                        await user.edit(nick='{}'.format(message.content), reason='{}'.format(c.DISCORD_MESSAGES['role_added']))

                                        await user.send(l.rsn_register[guild_l]['msg_success_2'].format(userName))
                                else:
                                    SAFE_CHECK += 1
                                    if SAFE_CHECK >= 10:
                                        CHECK = False
                                        await user.send(l.rsn_register[guild_l]['msg_error_1'].format(userName))
                            else:
                                CHECK = False
                                await user.send(l.rsn_register[guild_l]['msg_error_1'].format(userName))
            await message.delete()
        except Exception as error:
            await exception.error(error)

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    @staticmethod
    async def fun_checkrsn(ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            path = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
            target_keys = ['user_id', 'user_status']
            target_values = [ctx.author.id, c.USER_PERMISSIONS['admin']]

            if await permissions.get_user_permission(path, target_keys, target_values) or ctx.author.id == ctx.guild.owner.id or ctx.author.id == c.CLIENT_ADMINISTRATION_ID:
                STRING = str(ctx.message.content).split(' ')
                if len(STRING) >= 2:
                    path2 = c.GUILD_PATH['rsn.json'].format(ctx.guild.id)
                    DATA = await json_manager.get_json(path2)
                    DCID = await origin.find_and_replace(STRING[1])
                    NEW_LIST = []
                    TIME_LIST = []

                    for data in DATA:
                        if data['user_id'] == DCID:
                            NEW_LIST = data['rsn']
                            TIME_LIST = data['time']

                    if NEW_LIST:
                        NEW_LIST.reverse()
                        TIME_LIST.reverse()
                        path4 = c.ORIGIN_PATH['embed.rsn.json']
                        json_string = await json_manager.get_json(path4)
                        new_json_string = {'data': []}
                        string = ''
                        for index, rsn_id in enumerate(NEW_LIST):
                            if index <= 4:
                                string += l.rsn_register[guild_l]['configuration']['rsn_list'].format(index+1, rsn_id, TIME_LIST[index] if TIME_LIST[index] else l.rsn_register[guild_l]['configuration']['rsn_false'])
                        for key, value in json_string[guild_l]['checkrsn'].items():
                            if int(key) == 1:
                                new_json_string['data'].append({
                                    'name{}'.format(key): value['name'],
                                    'value{}'.format(key): str(value['value']).format(STRING[1])
                                })
                            else:
                                new_json_string['data'].append({
                                    'name{}'.format(key): str(value['name']).format(l.rsn_register[guild_l]['configuration']['module_name']),
                                    'value{}'.format(key): str(value['value']).format(string)
                                })

                        await embed_creator.create_embed(ctx, discord.Color.gold(), False, ctx.guild.icon_url, ctx.guild.icon_url, l.rsn_register[guild_l]['embed_1'].format(ctx.guild.name), new_json_string['data'], False)
                    else:
                        await ctx.send(l.rsn_register[guild_l]['msg_error_2'].format(STRING[1], ctx.guild.name))
                else:
                    await ctx.send(l.rsn_register[guild_l]['msg_info_1'].format(ctx.author.mention))
            else:
                await ctx.author.send(l.user_permissions[guild_l]['msg_restricted_1'])
        except Exception as error:
            await exception.error(error)

    async def fun_rsn(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            guild_t = await origin.get_region(ctx.guild.id)
            STRING = str(ctx.message.content).split(' ')
            if len(STRING) >= 2:
                time = await server_timer.get_current_time(guild_t)
                time = time.strftime('%y.%m.%d %H:%M:%S')
                path1 = c.GUILD_PATH['{}.ini'.format(self.name)].format(ctx.guild.id)
                ini = await ini_manager.get_ini(path1)
                role_id = int(ini['SECTION1']['ROLE'])
                CHECK = True
                if role_id:
                    role = await discord_manager.get_role(self.client, ctx.guild.id, role_id)
                    if role:
                        path2 = c.GUILD_PATH['rsn.json'].format(ctx.guild.id)
                        user = await discord_manager.get_member(self.client, ctx.guild.id, ctx.author.id)
                        SAFE_CHECK = 0
                        userName = ''

                        for string in STRING[1:]:
                            userName += '{} '.format(string)

                        userName = userName.lstrip()
                        userName = userName.rstrip()

                        while CHECK:
                            USERNAME = userName.replace(' ', '%20')
                            USER = hiscores_xp.Hiscores(USERNAME, 'N')
                            if USER.status != 404:
                                if hasattr(USER, 'stats'):
                                    CHECK = False
                                    if not await json_manager.get_status(path2, 'user_id', ctx.author.id):
                                        json_string = {'user_id': ctx.author.id, 'rsn': [userName], 'time': ['{}'.format(time)]}
                                        await json_manager.create(path2, json_string)
                                        await user.add_roles(role, reason='{}'.format(c.DISCORD_MESSAGES['role_added']), atomic=True)
                                        await user.edit(nick='{}'.format(userName), reason='{}'.format(c.DISCORD_MESSAGES['role_added']))

                                        await user.send(l.rsn_register[guild_l]['msg_success_1'].format(userName))
                                    else:
                                        DATA = await json_manager.get_json(path2)
                                        MASSIVE = []
                                        TIME_MASSIVE = []
                                        for data in DATA:
                                            if data['user_id'] == ctx.author.id:
                                                MASSIVE = data['rsn']
                                                MASSIVE.append(userName)
                                                TIME_MASSIVE = data['time']
                                                TIME_MASSIVE.append(time)

                                        target_keys = ['rsn', 'time']
                                        target_values = [MASSIVE, TIME_MASSIVE]

                                        await json_manager.update(path2, 'user_id', ctx.author.id, target_keys, target_values)
                                        await user.add_roles(role, reason='{}'.format(c.DISCORD_MESSAGES['role_added']), atomic=True)
                                        await user.edit(nick='{}'.format(userName), reason='{}'.format(c.DISCORD_MESSAGES['role_added']))

                                        await user.send(l.rsn_register[guild_l]['msg_success_2'].format(userName))
                                else:
                                    SAFE_CHECK += 1
                                    if SAFE_CHECK >= 10:
                                        CHECK = False
                                        await user.send(l.rsn_register[guild_l]['msg_error_1'])
                            else:
                                CHECK = False
                                await user.send(l.rsn_register[guild_l]['msg_error_1'].format(userName))
            else:
                await ctx.send(l.rsn_register[guild_l]['msg_info_2'])
        except Exception as error:
            await exception.error(error)

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def rsn(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)].format(ctx.guild.id), self.fun_rsn)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def checkrsn(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)].format(ctx.guild.id), self.fun_checkrsn)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

def setup(client):
    client.add_cog(rsn_register(client))