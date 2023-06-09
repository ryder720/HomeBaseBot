from discord.ext import commands
import time, datetime

# Constants
ADMIN_ROLE = "Admin"

# Bot extention class
class BaseCog(commands.Cog):  
    def __init__(self, bot) -> None:
        self.bot = bot
        self.startTime = time.time()


    ##DEBUG COMMANDS##
    @commands.has_role(ADMIN_ROLE)
    @commands.command()
    async def debug(self, ctx, arg=None):  
        match arg:
            # !debug time
            case 'time': 
                now = datetime.datetime.now()
                current_time = now.strftime('%H:%M:%S')
                await ctx.send(f'Current time = {current_time}')
            # !debug uptime
            case 'uptime':
                uptime = str(datetime.timedelta(seconds=int(round(time.time()-self.startTime))))
                await ctx.send(f'The bot has been up for {uptime}')
            # !debug
            case _:
                await ctx.send("Test successful.")
    ##END DEBUG COMMANDS##

    @commands.command()
    async def help(self, ctx, arg=None):
        match arg:
            case 'commands':
                # Might want to add a parser to pretty this up
                hcoms = {'help':'Information on the use of this bot'}
                await ctx.send(f'list of commands: {repr(hcoms)}')
            case 'debug':
                if not commands.has_role('admin'):
                    pass
                dcoms = {'': 'sends message to channel as test',
                         'time': 'get current time in bots timezone',
                         'uptime': 'get current bot uptime'}
                await ctx.send(f'!debug "command": {repr(dcoms)}')
            case _:
                await ctx.send('For a list of commands type "!help commands"')

# Manditory setup override function
async def setup(client):
    await client.add_cog(BaseCog(client))