from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
load_dotenv()

bot = commands.Bot('vv',intents=discord.Intents.all())

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name='with verifications'))

for cog in os.listdir('src/cogs'):
    if cog.endswith('.py'):
        cog = f'src.cogs.{cog[:-3]}'
        bot.load_extension(cog)

bot.run(os.environ['DISCORD_TOKEN'])