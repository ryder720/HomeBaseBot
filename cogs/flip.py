from discord.ext import commands
import random, os, json, math, discord


# Flip cog is an addon remake of a bot I made a while back
# Every season the leaderboards reset 
# You use !flip to flip a coin
# Heads = 2 points / Tails = 1
# I use: int((1 + math.sqrt(1 + 8 * points / 5)) / 2) to calc level

# Constants
DATA_DIR = './data/flip/'

flipchannels = []

class FlipCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    def updateleaderboard(self, usr, coin):
            score = coin + 1
            # Check if file exists
            if not os.path.isfile(f'{DATA_DIR}flip.json'):
                with open(f'{DATA_DIR}flip.json', 'w+') as file: 
                    newdata = {str(usr): {'score': score, 'level': 0}}
                    json.dump(newdata, file)
            else:
                with open(f'{DATA_DIR}flip.json', 'r') as file:
                    data = json.load(file)
                    data[str(usr)]['score'] += score

                    # Update player level
                    total = data[str(usr)]['score']
                    data[str(usr)]['level'] = int((1 + math.sqrt(1 + 8 * total / 5)) / 2)

                with open(f'{DATA_DIR}flip.json', 'w') as file:
                    json.dump(data, file)

    def viewplayeronboard(self, ctx):
            if not os.path.isfile(f'{DATA_DIR}flip.json'):
                with open(f'{DATA_DIR}flip.json', 'w+') as file:
                    key = str(ctx.author.id)
                    newdata = {key: {'score': 0, 'level': 0}}
                    json.dump(newdata, file)
                    return newdata[key]
            
            with open(f'{DATA_DIR}flip.json', 'r') as file:
                    data = json.load(file)
                    key = str(ctx.author.id)
                    if key in data.keys():
                        # Pretty up later
                        return data[key]
                    return None

    # !flip
    @commands.command()
    async def flip(self, ctx, arg=None):
        if ctx.channel.id in flipchannels:
            match arg:
                # !flip leaderboard
                case 'leaderboard':
                    player = self.viewplayeronboard(ctx)
                    if player:
                        # Pretty up later
                        await ctx.send(f"{ctx.author} is currently level {player['level']} with a score of {player['score']}")
                    else:
                        await ctx.send(f'Sorry {ctx.author} I couldn\'t find your id on the leaderboard')
                        print(f'Failed to find {ctx.author.id} in {DATA_DIR}flip.json')

                # !flip
                case _:
                    # Flip coin
                    coin = random.randint(0,1)
                    message = ''
                    player = self.viewplayeronboard(ctx)
                    if coin:
                        message += f"LVL[{player['level']}] {ctx.author}\'s flip landed HEADS!"
                    else:
                        message += f"LVL[{player['level']}] {ctx.author}\'s flip landed TAILS!"
                    # Update score
                    self.updateleaderboard(ctx.author.id, coin)
                    player = self.viewplayeronboard(ctx)
                    message += f"\nYour new score is {player['score']}"
                    await ctx.send(message)
        else:
            await ctx.message.delete()
            await ctx.author.send(f'Hey {ctx.author} I know how fun flipping is but please keep it contained in the relegated flip channel')


    @commands.command()
    async def fliphelp(self, ctx):
        await ctx.send('Commands: \n'
                 '!flip | Flip a coin \n'
                 '!flip leaderboard | See how you rank on the leaderboard\n'
                 'ONLY USABLE IN FLIP CHAT')
    

# Manditory setup override function
async def setup(client):
    await client.add_cog(FlipCog(client))

    for server in client.guilds:
        names = []
        categories = []
        for channel in server.channels:
            names.append(channel.name)
        for category in server.categories:
            categories.append(category.name)
        
        if 'GAMES' not in categories:
            gamescategory = await server.create_category('GAMES')
        else:
            gamescategory = discord.utils.get(server.categories, name='GAMES')

        if 'flip' not in names:
            await server.create_text_channel('flip', category = gamescategory)
            channel = discord.utils.get(server.channels, name='flip')
            flipchannels.append(channel.id) 
        else:
            channel = discord.utils.get(server.channels, name='flip')
            flipchannels.append(channel.id) 

              