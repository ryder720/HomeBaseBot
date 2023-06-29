from discord.ext import commands
import random, os, json, math, discord, pathlib
from start_bot import SERVER


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
        # Needs reboot after creation to work correctly
        self.flipchannel = discord.utils.get(bot.get_guild(SERVER).channels, name='flip')

        if not self.flipchannel:
            print('ERROR: Cant find flipchannel')
    ## File Work ##
    def loadfileasdict(self):
        dict = {}
        with open(f'{DATA_DIR}flip.json', 'r') as file:
            dict = json.load(file)
        return dict
    def writefilefromdict(self, dict):
        with open(f'{DATA_DIR}flip.json', 'w') as file:
            json.dump(dict, file)
    ## End File Work ##

    ## Leaderboard ##
    def updateleaderboard(self, usr, coin):
        score = coin + 1
        # Check if file exists
        self.createleaderboard(usr)
        
        data = self.loadfileasdict()
        data[str(usr)]['score'] += score

        # Update player level
        total = data[str(usr)]['score']
        data[str(usr)]['level'] = int((1 + math.sqrt(1 + 8 * total / 5)) / 2)

        self.writefilefromdict(data)

    def viewplayeronboard(self, ctx):
        
        self.createleaderboard(ctx.author.id)
        
        data = self.loadfileasdict()
        key = str(ctx.author.id)
        if key in data.keys():
            # Pretty up later
            return data[key]
        else:
            # Create new player adds data instead of overwriting
            data.update({key: {'score': 0, 'level': 0}})
            self.writefilefromdict(data)
            return data[key]
            
    async def viewleaderboard(self, ctx):
        self.createleaderboard(ctx.author.id)
        leaderboard = {}

        data = self.loadfileasdict()
        datadict = dict(data)  # Make copy
        for ind in datadict.keys():
            # Replace id with name no way this can't be maliciously exploited lol
            # Maybe just add servername to database as well when I update discord.py
            usr = await ctx.bot.fetch_user(int(ind))
            newind = usr.name
            leaderboard.update({newind: datadict[ind]})
        leaderboard = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
        return leaderboard
    
    # Checks if leaderbord needs to be created, if so, it creates it
    def createleaderboard(self, userid):
        if not os.path.isfile(f'{DATA_DIR}flip.json'):
            pathlib.Path(f'{DATA_DIR}').mkdir(parents=True, exist_ok=True)
            with open(f'{DATA_DIR}flip.json', 'w+') as file:
                key = str(userid)
                newdata = {key:{'score': 0, 'level': 0}}
                json.dump(newdata, file)
                print(newdata)
        
    ## End Leaderboard ##

    # !flip
    @commands.command()
    async def flip(self, ctx, arg=None):
        if ctx.channel.id == self.flipchannel.id:
            match arg:
                # !flip score
                case 'score':
                    player = self.viewplayeronboard(ctx)
                    if player:
                        # immushmush is currently level 6 with a score of 98
                        await ctx.send(f"{ctx.author.name} is currently level {player['level']} with a score of {player['score']}")
                    else:
                        await ctx.send(f'Sorry {ctx.author.name} I couldn\'t find your id on the leaderboard')
                        print(f'Failed to find {ctx.author.id} in {DATA_DIR}flip.json')

                case 'leaderboard':
                    board = await self.viewleaderboard(ctx)
                    # Pretty up here
                    await ctx.send(board)
                
                case 'help':
                    await ctx.send('Commands: \n'
                        '!flip | Flip a coin \n'
                        '!flip leaderboard | Check the leaderboard\n'
                        '!flip score | View your stats\n'
                        'ONLY USABLE IN FLIP CHAT')

                # !flip
                case _:
                    # Flip coin
                    coin = random.randint(0,1)
                    message = ''
                    player = self.viewplayeronboard(ctx)
                    if coin:
                        message += f"LVL[{player['level']}] {ctx.author.name}\'s flip landed HEADS!"
                    else:
                        message += f"LVL[{player['level']}] {ctx.author.name}\'s flip landed TAILS!"
                    # Update score
                    self.updateleaderboard(ctx.author.id, coin)
                    player = self.viewplayeronboard(ctx)
                    message += f"\nYour new score is {player['score']}"
                    await ctx.send(message)
        else:
            await ctx.message.delete()
            await ctx.author.send(f'Hey {ctx.author.name} I know how fun flipping is but please keep it contained in the relegated flip channel')
         

# Manditory setup override function
async def setup(client):
    await client.add_cog(FlipCog(client))

    # Check for server channels
    bot_server = client.get_guild(SERVER)
    gamescategory = discord.utils.get(bot_server.categories, name='GAMES')
    flipchannel = discord.utils.get(bot_server.channels, name='flip')

    # Create server channels    
    if not gamescategory:
        gamescategory = await bot_server.create_category('GAMES')

    if not flipchannel:
        await bot_server.create_text_channel('flip', category = gamescategory)
