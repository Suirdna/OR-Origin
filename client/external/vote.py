from client import exception, discord_manager, ini_manager, json_manager, origin, permissions, server_timer
from client.config import config as c, language as l
from discord.ext import commands

class vote(commands.Cog):
    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    name = 'vote'

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    @staticmethod
    async def check_vote(payload, status):
        try:
            if payload.emoji.name == l.DISCORD_EMOTE['positive']:
                path = c.GUILD_PATH['voteban.json'].format(payload.guild_id)
                data = await json_manager.get_data(path)

                if data:
                    for value in data:
                        if value['message_id'] == payload.message_id:
                            if status:
                                SUM = value['vote'] + 1
                            else:
                                SUM = value['vote'] - 1
                            await json_manager.update(path, 'message_id', payload.message_id, 'vote', SUM)
        except Exception as error:
            await exception.error(error)

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    async def fun_votemute(self, ctx):
        try:
            guild_l = await origin.get_language(ctx.guild.id)
            guild_t = await origin.get_region(ctx.guild.id)
            path = c.GUILD_PATH['{}.ini'.format(self.name)].format(ctx.guild.id)
            ini = await ini_manager.get_ini(path)

            restriction = ini['SECTION1']['RESTRICTION']
            count = ini['SECTION2']['COUNT']

            organizer = await discord_manager.get_member(self.client, ctx.guild.id, ctx.author.id)
            restriction_role = await discord_manager.get_role(self.client, ctx.guild.id, int(restriction))
            organizer_roles = organizer.roles

            STATUS = None

            for role in organizer_roles:
                if role.id == restriction_role.id:
                    STATUS = True

            if STATUS:
                VALUE = str(ctx.message.content).split(' ')

                if len(VALUE) == 2:
                    VALUE = await origin.find_and_replace(VALUE[1])

                    user = await discord_manager.get_member(self.client, ctx.guild.id, VALUE)
                    path1 = c.GUILD_PATH['muted_member.json'].format(ctx.guild.id)
                    path2 = c.GUILD_PATH['voteban.json'].format(ctx.guild.id)

                    if not await json_manager.get_status(path1, 'user_id', user.id):
                        if not await json_manager.get_status(path2, 'user_id', user.id):
                            guild_current = await server_timer.get_timedelta(minutes=5, region=guild_t)
                            message = await ctx.send(l.vote[guild_l]['msg_pool_1'].format(user.mention, count, 5))
                            await message.add_reaction(l.DISCORD_EMOTE['positive'])

                            json_string = {'message_id': message.id, 'user_id': user.id, 'user_username': user.mention, 'year': guild_current.year, 'month': guild_current.month, 'day': guild_current.day, 'hour': guild_current.hour, 'minute': guild_current.minute, 'vote': 0}
                            await json_manager.create(path2, json_string)
                        else:
                            await ctx.send(l.vote[guild_l]['msg_1'].format(user.mention))
                    else:
                        await ctx.send(l.vote[guild_l]['msg_decline'].format(user.mention))
                else:
                    await ctx.send(l.vote[guild_l]['msg_badformat'].format(ctx.author.mention))
            else:
                await ctx.send(l.vote[guild_l]['msg_nopermissions'].format(restriction_role.name))
        except Exception as error:
            await exception.error(error)

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def votemute(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await permissions.module_status_check(ctx, self.name, c.GUILD_PATH['{}.ini'.format(self.name)], self.fun_votemute)
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

def setup(client):
    client.add_cog(vote(client))