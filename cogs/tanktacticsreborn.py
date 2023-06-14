from discord.ext import commands
import discord
from cogs.base import DISCORD_ROLES
from enum import Enum
from datetime import datetime,timedelta
from threading import Timer

# Tank Tactics is a friendship ruining game made by Halfbrick Studios
# You can watch an amazing talk on it here: https://www.youtube.com/watch?v=t9WMNuyjm4w&pp=ygUNZ2RjIGhhbGZicmljaw%3D%3D
# In this game you control a square that gets one action point a day
# You can use this action point to move, shoot, trade, or upgrade range
# The goal in the prototype is to be the last person standing
# I'm going to recreate it here and add a few tweaks that might make it less life ruining.... or more idk

# Constants
DATA_DIR = './data/ttr/'
ROUND_TIMER = 24  # Hours need to convert depending on how it's used

ttrchannels = []

class GameState(Enum):
    Stopped = 1
    Setup = 2
    Play = 3


class TTRCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.gamestate = GameState.Stopped
        self.nextroundtime = 0
        self.roundtimer = 86400
        self.round = 0
        self.gameover = True
        self.boardheight = 8
        self.boardwidth = 8
        self.baseboardemoji = ':black_large_square:'
        
    
    @commands.command()
    async def ttr(self, ctx, arg=None):
        match arg:
            case 'round':
                if self.gamestate == GameState.Play:
                    await ctx.send(f'Round:{self.round} will end in {self.calculatenextround()}')
            # !ttr play | Start game if available
            case 'play':
                # Start game
                if self.gamestate == GameState.Stopped:
                    await ctx.send('DEBUG: START GAME NOT IMPLEMENTED YET CHANGING GAME STATE')
                    await self.startgame()
                    self.gamestate = GameState.Setup

                else:
                    await ctx.send('TTR is already setting up or underway. Checkout the game page to find out!')
            # !ttr | sends status of current game
            case _:
                match self.gamestate:
                    case GameState.Stopped:
                        await ctx.send('The game is currently not running. If you would like to start a game please type !ttr play.')
                    case GameState.Setup:
                        await ctx.send('The game is currently looking for memebers please visit the game page and react to play.')
                    case GameState.Play:
                        await ctx.send('The game is currently underway! Go to the game page to watch the action!')
                    case _:
                        print('ERROR: TTR GAMESTATE NOT FOUND')
    
    async def startgame(self):
        self.gameover = False
        self.round = 0

        # Set up board
        embed = discord.Embed(title='Tank Tactics!')

        # Make list of each column based on board height and width
        baseboard = []
        for _ in range(0, self.boardheight):
            boardcolumn = []
            for _ in range(0, self.boardwidth):
                boardcolumn += self.baseboardemoji
            baseboard += boardcolumn

        # ERROR BOARD TOO LARGE
        embed.add_field(name='', value=self.displayboard(baseboard))
        for channel in ttrchannels:
            ttrchannel = self.bot.get_channel(channel)
            await ttrchannel.send(embed=embed)

        await self.nextround()

    def displayboard(self, boardlist):
        liststring = ''
        for list in boardlist:
            liststring += ' '.join(list) + '\n'
        return liststring
    
    def calculatenextround(self):
        currentday=datetime.today()
        delta_t=self.nextroundtime-currentday

        return delta_t
        
    async def nextround(self):
        # Game Logic
        

        if not self.gameover:
            self.nextroundtime = datetime.now() + timedelta(days=1)
            roundthread = Timer(self.roundtimer, self.nextround())
            roundthread.daemon = True
            roundthread.start()
            self.round += 1
            


# Manditory setup override function
async def setup(client):
    await client.add_cog(TTRCog(client))

    # Get all roles but admin
    ttrroles = []
    for role in DISCORD_ROLES:
        if not 'Admin':
            ttrroles += role

    # Create server channels
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

        if 'ttr' not in names:
            await server.create_text_channel('ttr', category = gamescategory)
            channel = discord.utils.get(server.channels, name='ttr')
            for role in ttrroles:
                await channel.set_permissions(role, send_messages=False)
            ttrchannels.append(channel.id)
        else:
            channel = discord.utils.get(server.channels, name='ttr')
            ttrchannels.append(channel.id) 