from discord.ext import commands
from start_bot import SERVER
from base import DISCORD_ROLES
import os, pathlib, json

DATA_DIR = './data/moderation/'

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.server = bot.get_guild(SERVER)

    async def kick(self, id, reason:str):
        with open(f'{DATA_DIR}kicked' , 'a') as file:
            kick = {id: {'reason':reason}}
            json.dump(kick, file)
        await self.server.kick(self.server.fetch_member(id), reason)

    @commands.has_role(DISCORD_ROLES[0])
    @commands.command()
    async def mod(self, ctx, arg=None):
        match arg[0]:
            case 'kick':
                await ctx.message.delete()
                await self.kick(arg[1])
            case '_':
                await ctx.message.delete()
                await ctx.author.send('Test success')



async def setup(client):
    await client.add_cog(Moderation(client))

    if not os.path.isfile(f'{DATA_DIR}kicked'):
        pathlib.Path(f'{DATA_DIR}').mkdir(parents=True, exist_ok=True)
    
        with open(f'{DATA_DIR}kicked' , 'w') as file:
            blankkick = {0: {'reason':'The reason provided'}}
            json.dump(blankkick, file)
        
        with open(f'{DATA_DIR}banned' , 'w') as file:
            blankban = {0: {'reason':'The reason provided', 'time': 0}}
            json.dump(blankban, file)

    
    


   
    