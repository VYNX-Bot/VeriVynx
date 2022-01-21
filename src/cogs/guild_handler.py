import json

import aiofiles
import discord
from discord.ext import commands


class Guild_Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        async with aiofiles.open("src/cogs/db/db.json") as f:
            data = json.loads(await f.read())

        data["guilds"][str(guild.id)] = {
            "verify_channel": None,
            "verify_role": None,
            "verify_message": None,
            "verify_emoji": None,
            "verify_timeout": None,
            "verify_timeout_message": None,
            "doublesecurity": False,
        }

        async with aiofiles.open("src/cogs/db/db.json", "w") as f:
            await f.write(json.dumps(data, indent=4))

        embed = discord.Embed(
            title="Hello there!",
            description="I am your verification bot!\n\nBefore you can use me, you need to set up some settings.\n\nTo do so, use the command `!help` for list all settings commands.",
            color=0x00FF00,
        )

        await guild.text_channels[0].send(embed=embed)


def setup(bot):
    bot.add_cog(Guild_Handler(bot))
