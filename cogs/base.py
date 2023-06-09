from discord.ext import commands

# Bot extention class
class MainCog(commands.Cog):  
    def __init__(self, bot) -> None:
        self.bot = bot

    # !test - Test command
    @commands.command()
    async def test(self, ctx):  
        await ctx.send("Test successful.")

async def setup(client):
    await client.add_cog(MainCog(client))