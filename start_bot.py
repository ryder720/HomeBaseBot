from os import getenv
from dotenv import load_dotenv
import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

#Commands


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    





if __name__ == "__main__":
    load_dotenv()
    TOKEN = getenv('DISCORD_TOKEN')
    client.run(TOKEN)  # Token here