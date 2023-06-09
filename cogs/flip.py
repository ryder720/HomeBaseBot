from discord.ext import commands
import random


class FlipCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def flip(self, ctx):
        num = random.randint(0,1)
        if num:
            await ctx.send(f'{ctx.author}\'s flip landed HEADS!')
        else:
            await ctx.send(f'{ctx.author}\'s flip landed TAILS!')

# Manditory setup override function
async def setup(client):
    await client.add_cog(FlipCog(client))