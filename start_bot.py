import os
from os import getenv
from dotenv import load_dotenv
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(intents=intents, command_prefix = "!",help_command=None)

# Get bot token and server id from .env
load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')
SERVER = int(getenv('SERVER_ID'))


@client.event
async def on_ready():
    # Load modules from ./cogs
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await client.load_extension("cogs." + file[:-3])
            print(f'DEBUG: Loaded {file} module')

    print(f'We have logged in as {client.user}, and Bot is ready to go!')

    for server in client.guilds:
            if server != client.get_guild(SERVER):
                await client.leave_guild(client.get_guild(SERVER))

@client.event
async def on_guild_join(server):
    # Leave server if not correct
    intendedserver = client.get_guild(SERVER)
    if intendedserver != server:
        await client.leave_guild(server)


if __name__ == "__main__":
    
    client.run(TOKEN)

    