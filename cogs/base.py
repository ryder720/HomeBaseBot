import os
from discord.ext import commands
import time, datetime, discord
from start_bot import SERVER

# Constants
DISCORD_ROLES = ['Admin', 'Member']



# Bot extention class
class BaseCog(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot
        # Start uptime timer
        self.startTime = time.time()
        
        


    ##DEBUG COMMANDS##
    @commands.has_role(DISCORD_ROLES[0])
    @commands.command()
    async def debug(self, ctx, arg=None):  
        match arg:
            # !debug time
            case 'time': 
                now = datetime.datetime.now()
                current_time = now.strftime('%H:%M:%S')
                await ctx.author.send(f'Current time = {current_time}')
            # !debug embed
            case 'embed':
                embed = discord.Embed(title='Test')
                embed.add_field(name='', value=':black_large_square:')
                await ctx.author.send(embed=embed)
            # !debug uptime
            case 'uptime':
                uptime = str(datetime.timedelta(seconds=int(round(time.time()-self.startTime))))
                await ctx.author.send(f'The bot has been up for {uptime}')
            # !debug
            case _:
                await ctx.author.send("Test successful.")
    ##END DEBUG COMMANDS##

    @commands.command()
    async def help(self, ctx, arg=None):
        match arg:
            # !help commands
            case 'commands':
                await ctx.send(f'Commands:\n'
                               '!help | Information on the use of this bot\n'
                               '!help cogs | Addons or "cogs" installed in bot')
            case 'cogs':
                # Will always work unless base cog gets moved during use
                cogsstring = 'Current cogs installed:\n'
                for file in os.listdir("./cogs"):
                    if file.endswith(".py"):
                        cogsstring += (f'{file[:-3]}\n')
                await ctx.send(cogsstring)
            # !help debug
            case 'debug':
                # Check if user has admin role
                if not commands.has_role('admin'):
                    pass
                await ctx.author.send(f'Debug Commands: \n'
                               '!debug | Send message back to chat as test \n'
                               '!debug time | Get current time in bots timezone \n'
                               '!debug uptime | Get current bot uptime')
            # !help
            case _:
                await ctx.send('For a list of commands type "!help commands"')

# Manditory setup override function
async def setup(client):
    await client.add_cog(BaseCog(client))
    
    server = client.get_guild(SERVER)
    
    for role in DISCORD_ROLES:
            if not discord.utils.get(server.roles, name=role):
                await server.create_role(name=role)


   
    
    