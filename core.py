from client import exception, console_interface, module_loader
from client.config import config as c
from discord.ext import commands
import discord

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix=c.CLIENT_PREFIX, help_command=None, intents=intents)

@client.event
async def on_ready():
    try:
        await console_interface.console()
        await module_loader.load_modules(client)
    except Exception as error:
        await exception.error(error)

client.run(c.CLIENT_TOKEN)
