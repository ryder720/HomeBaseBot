from discord.ext import commands
import time, datetime

# Bot extention class
class BaseCog(commands.Cog):  
    def __init__(self, bot) -> None:
        self.bot = bot
        self.startTime = time.time()


    ##DEBUG COMMANDS##
    # !test - Test command
    @commands.has_role('admin')
    @commands.command()
    async def debugTest(self, ctx):  
        await ctx.send("Test successful.")
    
    @commands.has_role('admin')
    @commands.command()
    async def debugTime(self, ctx):
        now = datetime.datetime.now()
        current_time = now.strftime('%H:%M:%S')
        await ctx.send(f'Current time = {current_time}')
    
    @commands.has_role('admin')
    @commands.command()
    async def debugUpTime(self, ctx):
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-self.startTime))))
        await ctx.send(f'The bot has been up for {uptime}')
    ##END DEBUG COMMANDS##

    @commands.command()
    async def help(self, ctx, arg=None):
        match arg:
            case 'commands':
                # Might want to add a parser to pretty this up
                commands = {'help':'Information on the use of this bot'}
                await ctx.send(f'list of commands: {repr(commands)}')
            case _:
                await ctx.send('For a list of commands type "!help commands"')

# Manditory setup override function
async def setup(client):
    await client.add_cog(BaseCog(client))