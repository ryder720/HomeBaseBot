import os
from os import getenv
from dotenv import load_dotenv
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(intents=intents, command_prefix = "!",help_command=None)


@client.event
async def on_ready():
    # Load modules from ./cogs
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            await client.load_extension("cogs." + file[:-3])
            print(f'DEBUG: Loaded {file} module')

    print(f'We have logged in as {client.user}, and Bot is ready to go!')


if __name__ == "__main__":
    # Get bot token from .env
    load_dotenv()
    TOKEN = getenv('DISCORD_TOKEN')

    client.run(TOKEN)