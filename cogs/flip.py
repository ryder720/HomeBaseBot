from discord.ext import commands
import random

# Flip cog is an addon remake of a bot I made a while back
# Every season the leaderboards reset 
# You use !flip to flip a coin
# Heads = 2 points / Tails = 1
# I use: int((1 + math.sqrt(1 + 8 * points / 5)) / 2) to calc level

class FlipCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    # !flip
    @commands.command()
    async def flip(self, ctx):
        # Flip coin
        num = random.randint(0,1)
        if num:
            await ctx.send(f'{ctx.author}\'s flip landed HEADS!')
        else:
            await ctx.send(f'{ctx.author}\'s flip landed TAILS!')

# Manditory setup override function
async def setup(client):
    await client.add_cog(FlipCog(client))