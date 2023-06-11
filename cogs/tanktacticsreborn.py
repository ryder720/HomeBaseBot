from discord.ext import commands
import discord
from cogs.base import DISCORD_ROLES

DATA_DIR = './data/ttr/'

ttrchannels = []


class TTRCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot


# Manditory setup override function
async def setup(client):
    await client.add_cog(TTRCog(client))

    # Get all roles but admin
    ttrroles = []
    for role in DISCORD_ROLES:
        if not 'Admin':
            ttrroles += role

    # Create server channels
    for server in client.guilds:
        names = []
        categories = []

        for channel in server.channels:
            names.append(channel.name)
        for category in server.categories:
            categories.append(category.name)
        
        if 'GAMES' not in categories:
            gamescategory = await server.create_category('GAMES')
        else:
            gamescategory = discord.utils.get(server.categories, name='GAMES')

        if 'ttr' not in names:
            await server.create_text_channel('ttr', category = gamescategory)
            channel = discord.utils.get(server.channels, name='ttr')
            for role in ttrroles:
                await channel.set_permissions(role, send_messages=False)
            ttrchannels.append(channel.id)
        else:
            channel = discord.utils.get(server.channels, name='ttr')
            ttrchannels.append(channel.id) 