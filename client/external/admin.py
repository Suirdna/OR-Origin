from client import exception, embed_creator, discord_manager, ini_manager, json_manager, origin, permissions, server_timer, console_interface
from client.config import config as c, language as l
from discord.ext import commands
import discord

class admin(commands.Cog):
    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    name = 'admin'

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    @staticmethod
    async def remove_message(message):
        try:
            path = c.GUILD_PATH['muted_member.json'].format(message.guild.id)
            if await json_manager.get_status(path, 'user_id', message.author.id):
                await message.delete()
        except Exception as error:
            await exception.error(error)

    async def add_permissions(self, ctx, permission):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            
            path = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
            if ctx.author.id == ctx.guild.owner.id or ctx.author.id == c.CLIENT_ADMINISTRATION_ID or await json_manager.get_status(path, 'user_status', 3):
                STRING = str(ctx.message.content).split(' ')
                if len(STRING) == 2:
                    DCID = await origin.find_and_replace(STRING[1])
                    if str(DCID).isdigit():
                        member = await discord_manager.get_member(self.client, ctx.guild.id, DCID)
                        if member:
                            user_permissions = [c.USER_PERMISSIONS['organizer'], c.USER_PERMISSIONS['admin'], c.USER_PERMISSIONS['dc_bank']]
                            path2 = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
                            if not await json_manager.get_status(path2, 'user_id', DCID):
                                json_string = None
                                for index in range(1, 4):
                                    if permission == index:
                                        json_string = {'user_id': DCID, 'user_status': user_permissions[index-1]}
                                        await ctx.author.send(l.admin[guild_l]['msg_success_{}'.format(index)].format(STRING[1]))
                                await json_manager.create(path2, json_string)
                            else:
                                for index in range(1, 4):
                                    if permission == index:
                                        await json_manager.update(path2, 'user_id', DCID, 'user_status', c.USER_PERMISSIONS['organizer'])
                                        await ctx.author.send(l.admin[guild_l]['msg_success_{}'.format(index)].format(STRING[1]))
                        else:
                            await ctx.author.send(l.admin[guild_l]['msg_error_1'].format(STRING[1]))
                    else:
                        for index in range(1, 4):
                            if permission == index:
                                await ctx.send(l.admin[guild_l]['msg_badformat_{}'.format(index)].format(ctx.author.mention))
                else:
                    for index in range(1, 4):
                        print(index)
                        if permission == index:
                            await ctx.send(l.admin[guild_l]['msg_info_{}'.format(index)].format(ctx.author.mention))
            else:
                await ctx.author.send(l.user_permissions[guild_l]['msg_restricted_1'])
        except Exception as error:
            await exception.error(error)

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    async def fun_addorganizer(self, ctx):
        try:
            await self.add_permissions(ctx, 1)
        except Exception as error:
            await exception.error(error)

    async def fun_addadmin(self, ctx):
        try:
            await self.add_permissions(ctx, 2)
        except Exception as error:
            await exception.error(error)

    async def fun_addaccountant(self, ctx):
        try:
            await self.add_permissions(ctx, 3)
        except Exception as error:
            await exception.error(error)

    @staticmethod
    async def fun_remuser(ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            if ctx.author.id == ctx.guild.owner.id or ctx.author.id == c.CLIENT_ADMINISTRATION_ID:
                STRING = str(ctx.message.content).split(' ')
                if len(STRING) == 2:
                    DCID = await origin.find_and_replace(STRING[1])
                    if str(DCID).isdigit():
                        path2 = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
                        await json_manager.delete(path2, 'user_id', DCID)
                        await ctx.author.send(l.admin[guild_l]['msg_success_4'].format(STRING[1]))
                    else:
                        await ctx.send(l.admin[guild_l]['msg_badformat_4'].format(ctx.author.mention))
                else:
                    await ctx.send(l.admin[guild_l]['msg_info_4'].format(ctx.author.mention))
            else:
                await ctx.author.send(l.user_permissions[guild_l]['msg_restricted_1'])
        except Exception as error:
            await exception.error(error)

    async def fun_mute(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            guild_t = await origin.get_region(ctx.guild.id)
            path = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
            target_keys = ['user_id', 'user_status']
            target_values = [ctx.author.id, c.USER_PERMISSIONS['admin']]
            STATUS = False

            if await permissions.get_user_permission(path, target_keys, target_values):
                STRING = str(ctx.message.content).split(' ')
                if len(STRING) >= 2:
                    DCID = await origin.find_and_replace(STRING[1])
                    if str(DCID).isdigit():
                        path1 = c.GUILD_PATH['{}.ini'.format(self.name)].format(ctx.guild.id)
                        ini = await ini_manager.get_ini(path1)
                        role_name = ini['SECTION1']['BAN']

                        path3 = c.GUILD_PATH['muted_member.json'].format(ctx.guild.id)
                        user = await discord_manager.get_member(self.client, ctx.guild.id, DCID)

                        if not await json_manager.get_status(path3, 'user_id', user.id):
                            path4 = c.CLIENT_PATH['guild'] + str(ctx.guild.id) + c.CLIENT_JSON['server']

                            if len(STRING) == 2:
                                guild_current = await server_timer.get_timedelta(weeks=52, region=guild_t)
                                STATUS = True

                            if len(STRING) == 3:
                                if STRING[2].isdigit():
                                    guild_current = await server_timer.get_timedelta(hours=int(STRING[2]), region=guild_t)
                                    STATUS = True

                            if STATUS:
                                json_string = {'user_id': user.id, 'user_username': user.mention, 'year': guild_current.year, 'month': guild_current.month, 'day': guild_current.day, 'hour': guild_current.hour, 'minute': guild_current.minute}

                                role = await discord_manager.get_role(self.client, ctx.guild.id, int(role_name))
                                await user.add_roles(role, reason=c.DISCORD_MESSAGES['mute_reason'], atomic=True)
                                await json_manager.create(path3, json_string)
                                server_config = await json_manager.get_json(path4)
                                await ctx.send(l.admin[guild_l]['msg_post_1'].format(user.mention, guild_current.year, guild_current.month, guild_current.day, guild_current.hour, guild_current.minute, l.admin[guild_l]['configuration']['extra_2'].format(server_config['chat1']) if server_config['chat1'] else ''))
                            else:
                                await ctx.send(l.admin[guild_l]['msg_info_9'].format(ctx.author.mention))
                        else:
                            await ctx.send(l.admin[guild_l]['msg_post_2'].format(user.mention))
                    else:
                        await ctx.send(l.admin[guild_l]['msg_badformat_5'].format(ctx.author.mention))
                else:
                    await ctx.send(l.admin[guild_l]['msg_info_5'].format(ctx.author.mention))
            else:
                await ctx.author.send(l.user_permissions[guild_l]['msg_restricted_1'])
        except Exception as error:
            await exception.error(error)

    async def fun_unmute(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            path = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
            target_keys = ['user_id', 'user_status']
            target_values = [ctx.author.id, c.USER_PERMISSIONS['admin']]

            if await permissions.get_user_permission(path, target_keys, target_values):
                STRING = str(ctx.message.content).split(' ')
                if len(STRING) == 2:
                    DCID = await origin.find_and_replace(STRING[1])
                    if str(DCID).isdigit():
                        path1 = c.GUILD_PATH['{}.ini'.format(self.name)].format(ctx.guild.id)
                        ini = await ini_manager.get_ini(path1)
                        role_name = ini['SECTION1']['BAN']

                        path3 = c.GUILD_PATH['muted_member.json'].format(ctx.guild.id)
                        user = await discord_manager.get_member(self.client, ctx.guild.id, DCID)

                        if await json_manager.get_status(path3, 'user_id', user.id):
                            role = await discord_manager.get_role(self.client, ctx.guild.id, int(role_name))
                            await user.remove_roles(role, reason=c.DISCORD_MESSAGES['unmute_reason'], atomic=True)
                            await json_manager.delete(path3, 'user_id', user.id)

                            await ctx.send(l.admin[guild_l]['msg_post_3'].format(user.mention))
                        else:
                            await ctx.send(l.admin[guild_l]['msg_post_4'].format(user.mention))
                    else:
                        await ctx.send(l.admin[guild_l]['msg_badformat_6'].format(ctx.author.mention))
                else:
                    await ctx.send(l.admin[guild_l]['msg_info_6'].format(ctx.author.mention))
            else:
                await ctx.author.send(l.user_permissions[guild_l]['msg_restricted_1'])
        except Exception as error:
            await exception.error(error)

    async def fun_post(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            path = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
            target_keys = ['user_id', 'user_status']
            target_values = [ctx.author.id, c.USER_PERMISSIONS['admin']]

            if await permissions.get_user_permission(path, target_keys, target_values):
                STRING = str(ctx.message.content).split(' ')
                if len(STRING) >= 2:
                    CID = await origin.find_and_replace(STRING[1])
                    if str(CID).isdigit():
                        SERVER = await discord_manager.get_server(self.client, ctx.guild.id)
                        CHANNEL = SERVER.get_channel(CID)

                        TEXT = ''
                        for data in STRING[2:]:
                            TEXT += '{} '.format(str(data))

                        if TEXT:
                            await CHANNEL.send(TEXT)
                        else:
                            await ctx.send(l.admin[guild_l]['msg_badformat_7'])
                    else:
                        await ctx.send(l.admin[guild_l]['msg_badformat_7'])
                else:
                    await ctx.send(l.admin[guild_l]['msg_info_7'])
            else:
                await ctx.author.send(l.user_permissions[guild_l]['msg_restricted_1'])
        except Exception as error:
            await exception.error(error)

    async def fun_showmember(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            path = c.GUILD_PATH['special_member.json'].format(ctx.guild.id)
            target_keys = ['user_id', 'user_status']
            target_values = [ctx.author.id, c.USER_PERMISSIONS['admin']]

            if await permissions.get_user_permission(path, target_keys, target_values):
                STRING = str(ctx.message.content).split(' ')
                if len(STRING) >= 1:
                    user = None

                    if len(STRING) == 1:
                        user = ctx.author

                    if len(STRING) == 2:
                        DCID = await origin.find_and_replace(STRING[1])
                        if str(DCID).isdigit():
                            SERVER = await discord_manager.get_server(self.client, ctx.guild.id)
                            user = SERVER.get_member(DCID)
                        else:
                            await ctx.send(l.admin[guild_l]['msg_badformat_8'].format(ctx.author.mention))

                    if user:
                        path2 = c.ORIGIN_PATH['embed.admin.json']
                        json_string = await json_manager.get_json(path2)
                        new_json_string = {'data': []}

                        for key, value in json_string[guild_l]['showmember'].items():
                            new_json_string['data'].append({
                                'name{}'.format(key): value['name'],
                                'value{}'.format(key): str(value['value']).format(
                                    user.mention, user.top_role.mention,
                                    user.premium_since.strftime('%y.%m.%d | %H:%M') if user.premium_since else l.admin[guild_l]['configuration']['extra_1'],
                                    user.joined_at.strftime('%y.%m.%d | %H:%M'),
                                    user.created_at.strftime('%y.%m.%d | %H:%M')
                                )
                            })

                        await embed_creator.create_embed(ctx, discord.Color.dark_orange(), None, ctx.guild.icon_url, user.avatar_url, l.admin[guild_l]['embed_1'].format(ctx.guild.name), new_json_string['data'], False)
                    else:
                        await ctx.send(l.admin[guild_l]['msg_error_1'].format(STRING[1]))
                else:
                    await ctx.send(l.admin[guild_l]['msg_info_8'].format(ctx.author.mention))
            else:
                await ctx.author.send(l.user_permissions[guild_l]['msg_restricted_1'])
        except Exception as error:
            await exception.error(error)


    async def fun_get_server_list(self, ctx):
        try:
            if ctx.author.id == c.CLIENT_ADMINISTRATION_ID:
                for guild in self.client.guilds:
                    await console_interface.console_message('{}, {}'.format(guild.name, guild.id))
            else:
                await ctx.author.send(l.user_permissions['EN']['msg_restricted_1'])
        except Exception as error:
            await exception.error(error)

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def addorganizer(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_addorganizer)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def addadmin(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_addadmin)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def addaccountant(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_addaccountant)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def remu(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_remuser)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def mute(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_mute)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def unmute(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_unmute)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def post(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_post)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def showmember(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_showmember)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def get_server_list(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await self.fun_get_server_list(ctx)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

def setup(client):
    client.add_cog(admin(client))