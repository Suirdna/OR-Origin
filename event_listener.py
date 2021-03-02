from client import exception, listener, logger
from client.config import config as c
from discord.ext import commands, tasks
import discord

class event_listener(commands.Cog):
    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    name = 'event_listener'
    STATUS = 0

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    @tasks.loop(minutes=1)
    async def status_update(self):
        try:
            status = discord.Game('{}'.format((c.CLIENT_STATUS[self.STATUS])))
            await self.client.change_presence(status=discord.Status.do_not_disturb, activity=status)

            self.STATUS += 1
            if self.STATUS == len(c.CLIENT_STATUS):
                self.STATUS = 0
        except Exception as error:
            await exception.error(error)

    # ▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬

    def __init__(self, client):
        self.client = client
        self.status_update.start()
        
    @commands.Cog.listener()
    async def on_message(self, payload):
        try:
            await listener.message(message, self.client)
        except Exception as error:
            await exception.error(error)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        try:
            await listener.raw_reaction_add(payload, self.client, True)
        except Exception as error:
            await exception.error(error)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        try:
            await listener.raw_reaction_remove(payload, self.client, False)
        except Exception as error:
            await exception.error(error)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        try:
            await listener.guild_join(self.client, guild)
        except Exception as error:
            await exception.error(error)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, discord.ext.commands.CommandError):
            await exception.error('{} - {}'.format(error, ctx))
        await exception.error(error)

def setup(client):
    client.add_cog(event_listener(client))
