from client import exception, embed_creator, json_manager, origin
from client.config import config as c, language as l
from discord.ext import commands

class command_listener(commands.Cog):
    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    name = 'command_listener'

    #▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    def __init__(self, client):
        self.client = client

    async def send_embed(self, ctx, prefix):
        guild_l = await origin.get_language(ctx.guild.id)
        author_name = l.command_listener[guild_l][prefix].format(c.CLIENT_NAME)
        embed_data = await json_manager.get_json(c.ORIGIN_PATH['embed.{}.json'.format(self.name)])
        await embed_creator.create_embed_command_listener(self, ctx, self.client, embed_data[guild_l][prefix], author_name, prefix)

    @commands.command()
    async def help(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await self.send_embed(ctx, 'help')
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def admin(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await self.send_embed(ctx, 'admin')
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

    @commands.command()
    async def about(self, ctx):
        try:
            if str(ctx.message.channel.type) == 'text':
                await self.send_embed(ctx, 'about')
            else:
                await ctx.send(l.module_permissions['EN']['msg_restricted_pm'])
        except Exception as error:
            await exception.error(error)

def setup(client):
    client.add_cog(command_listener(client))