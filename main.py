
from dotenv import load_dotenv
# done
load_dotenv()

import os

import discord
from discord.ext import commands

import k
from src.cogs.utils.slash import Bot

bot = Bot("vv", intents=discord.Intents.all())


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")
    await bot.change_presence(activity=discord.Game(name="with verifications"))


for cog in os.listdir("src/cogs"):
    if cog.endswith(".py"):
        cog = f"src.cogs.{cog[:-3]}"
        bot.load_extension(cog)

k.k()
bot.run(os.environ["DISCORD_TOKEN"])
