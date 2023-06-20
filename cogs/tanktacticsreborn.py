from discord.ext import commands
import discord
from cogs.base import DISCORD_ROLES
from start_bot import SERVER
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
ROUND_TIMER = 86400  # Seconds in a day

class GameState(Enum):
    Stopped = 1
    Setup = 2
    Play = 3


class TTRCog(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.ttrchannel = discord.utils.get(bot.get_guild(SERVER).channels, name='ttr')
        self.gamestate = GameState.Stopped
        self.nextroundtime = 0
        self.roundtimer = 86400
        self.round = 0
        self.gameover = True
        # Max 9x9 with current solution
        self.boardheight = 9
        self.boardwidth = 9
        self.baseboardemoji = ':black_large_square:'
        self.boardmessageid = 0
        
    
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
        # Set to true to limit recursion error
        self.gameover = False
        self.round = 0

        # Make list of each column based on board height and width
        board = []
        for _ in range(0, self.boardwidth):
            boardcolumn = []
            for _ in range(0, self.boardheight):
                boardcolumn.append(self.baseboardemoji)
            boardcolumn.append('\n')
            board.append(boardcolumn)
        

        self.nextround(board)

    async def createboard(self, boardlist):
        boardstring = ''
        for row in boardlist:
            for collumn in row:
                boardstring += collumn[:]
        
        message = await self.ttrchannel.send(boardstring)
        self.boardmessageid = message.id
        
    
    def updateboard(self, boardlist):
        boardstring = ''
        for row in boardlist:
            for collumn in row:
                boardstring += collumn[:]
        
            
    
    def calculatenextround(self):
        currentday=datetime.today()
        delta_t=self.nextroundtime-currentday

        return delta_t
        
    def nextround(self, gameboard):
        # Game Logic


        self.updateboard(gameboard)
        if not self.gameover:
            self.nextroundtime = datetime.now() + timedelta(days=1)
            roundthread = Timer(ROUND_TIMER, self.nextround, (gameboard,))
            roundthread.daemon = True
            roundthread.start()
            print(f'DEBUG: Timer started for {ROUND_TIMER} seconds')
            self.round += 1
            print(f'DEBUG: Current round {self.round}')
            


# Manditory setup override function
async def setup(client):
    await client.add_cog(TTRCog(client))

    # Get all roles but admin
    ttrroles = []
    for role in DISCORD_ROLES:
        if not 'Admin':
            ttrroles += role
    bot_server = client.get_guild(SERVER)
    # Create server channels    
    if 'GAMES' not in bot_server.categories:
        gamescategory = await bot_server.create_category('GAMES')
    else:
        gamescategory = discord.utils.get(bot_server.categories, name='GAMES')

    if 'ttr' not in bot_server.channels:
        overwrites = {bot_server.default_role: discord.PermissionOverwrite(send_messages=False, add_reactions=False)}
        await bot_server.create_text_channel('ttr', category = gamescategory, overwrites=overwrites)
        ttrchannel = discord.utils.get(bot_server.channels, name='ttr')
        for role in ttrroles:
            await ttrchannel.set_permissions(role, send_messages=False)
        
    else:
        ttrchannel = discord.utils.get(bot_server.channels, name='ttr')
        