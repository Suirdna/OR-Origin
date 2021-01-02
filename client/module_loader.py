from client.config import config as c
from discord.ext.commands.errors import ExtensionAlreadyLoaded

async def load_modules(client):
    try:
        for module in c.CLIENT_MODULES:
            client.load_extension(module)
    except ExtensionAlreadyLoaded:
        pass
