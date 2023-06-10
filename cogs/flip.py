from discord.ext import commands
import random, os, json


# Flip cog is an addon remake of a bot I made a while back
# Every season the leaderboards reset 
# You use !flip to flip a coin
# Heads = 2 points / Tails = 1
# I use: int((1 + math.sqrt(1 + 8 * points / 5)) / 2) to calc level

# Constants
DATA_DIR = './data/flip/'

class FlipCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        # Create json file if it doesn't exist
        

    def updateleaderboard(self, usr, coin):
            score = coin + 1
            if not os.path.isfile(f'{DATA_DIR}flip.json'):
                with open(f'{DATA_DIR}flip.json', 'w+') as file: 
                    newdata = {str(usr): {'score': score}}
                    json.dump(newdata, file)
            else:
                with open(f'{DATA_DIR}flip.json', 'r') as file:
                    data = json.load(file)
                    
                    data[str(usr)]['score'] += score

                with open(f'{DATA_DIR}flip.json', 'w') as file:
                    json.dump(data, file)

            

    # !flip
    @commands.command()
    async def flip(self, ctx):
        # Flip coin
        coin = random.randint(0,1)
        if coin:
            await ctx.send(f'{ctx.author}\'s flip landed HEADS!')
        else:
            await ctx.send(f'{ctx.author}\'s flip landed TAILS!')

        self.updateleaderboard(ctx.author.id, coin)

    

# Manditory setup override function
async def setup(client):
    await client.add_cog(FlipCog(client))