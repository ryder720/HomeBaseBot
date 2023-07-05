from discord.ext import commands
import os, pathlib, json

DATA_DIR = './data/moderation/'

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


async def setup(client):
    await client.add_cog(Moderation(client))

    if not os.path.isfile(f'{DATA_DIR}kicked'):
        pathlib.Path(f'{DATA_DIR}').mkdir(parents=True, exist_ok=True)
    
        with open(f'{DATA_DIR}kicked' , 'w') as file:
            blankkick = {0: {'reason':'The reason provided'}}
            json.dump(blankkick, file)
        
        with open(f'{DATA_DIR}banned' , 'w') as file:
            blankban = {0: {'reason':'The reason provided', 'time': 0}}
            json.dump(blankban, file)

    
    


   
    