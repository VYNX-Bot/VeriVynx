import json

import aiofiles
import discord
from discord.ext import commands


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def set_verify_channel(self, ctx, channel: discord.TextChannel = None):
        if channel == None:
            await ctx.send(
                f"Please specify a channel to set as the verification channel."
            )
            return
        async with aiofiles.open("src/cogs/db/db.json") as f:
            data = json.loads(await f.read())

        data["guilds"][str(ctx.guild.id)]["verify_channel"] = channel.id

        async with aiofiles.open("src/cogs/db/db.json", "w") as f:
            await f.write(json.dumps(data, indent=4))

        await ctx.send(f"Verification channel set to {channel.mention}")

    @commands.command()
    async def set_verify_role(self, ctx, role: discord.Role = None):
        if role == None:
            await ctx.send(f"Please specify a role to set as the verification role.")
            return
        async with aiofiles.open("src/cogs/db/db.json") as f:
            data = json.loads(await f.read())

        data["guilds"][str(ctx.guild.id)]["verify_role"] = role.id

        async with aiofiles.open("src/cogs/db/db.json", "w") as f:
            await f.write(json.dumps(data, indent=4))

        await ctx.send(f"Verification role set to {role.mention}")

    @commands.command()
    async def set_verify_message(self, ctx, *, message=None):
        if message == None:
            await ctx.send(
                f"Please specify a message to set as the verification message."
            )
            return
        async with aiofiles.open("src/cogs/db/db.json") as f:
            data = json.loads(await f.read())

        data["guilds"][str(ctx.guild.id)]["verify_message"] = message

        async with aiofiles.open("src/cogs/db/db.json", "w") as f:
            await f.write(json.dumps(data, indent=4))

        await ctx.send(f"Verification message set to {message}")

    @commands.command()
    async def set_verify_emoji(self, ctx, emoji: discord.Emoji = None):
        if emoji == None:
            await ctx.send(f"Please specify an emoji to set as the verification emoji.")
            return

        async with aiofiles.open("src/cogs/db/db.json") as f:
            data = json.loads(await f.read())

        data["guilds"][str(ctx.guild.id)]["verify_emoji"] = emoji.id

        async with aiofiles.open("src/cogs/db/db.json", "w") as f:
            await f.write(json.dumps(data, indent=4))

        await ctx.send(f"Verification emoji set to {str(emoji)}")

    @commands.command()
    async def set_verify_timeout(self, ctx, timeout: int = 0):
        if timeout <= 0:
            await ctx.send(f"Please specify a timeout greater than 0.")
            return
        async with aiofiles.open("src/cogs/db/db.json") as f:
            data = json.loads(await f.read())

        data["guilds"][str(ctx.guild.id)]["verify_timeout"] = timeout

        async with aiofiles.open("src/cogs/db/db.json", "w") as f:
            await f.write(json.dumps(data, indent=4))

        await ctx.send(f"Verification timeout set to {timeout} seconds")

    @commands.command()
    async def set_verify_timeout_message(self, ctx, *, message=None):
        if message == None:
            await ctx.send(
                f"Please specify a message to set as the verification timeout message."
            )
            return
        async with aiofiles.open("src/cogs/db/db.json") as f:
            data = json.loads(await f.read())

        data["guilds"][str(ctx.guild.id)]["verify_timeout_message"] = message

        async with aiofiles.open("src/cogs/db/db.json", "w") as f:
            await f.write(json.dumps(data, indent=4))

        await ctx.send(f"Verification timeout message set to {message}")

    @commands.command()
    async def set_doublesecurity(self, ctx, *, yes_or_no=None):
        if yes_or_no == None:
            await ctx.send(f"Please specify yes or no.")
            return
        async with aiofiles.open("src/cogs/db/db.json") as f:
            data = json.loads(await f.read())

        if yes_or_no.lower() == "yes":
            data["guilds"][str(ctx.guild.id)]["doublesecurity"] = True
            await ctx.send("Double security enabled")
        elif yes_or_no.lower() == "no":
            data["guilds"][str(ctx.guild.id)]["doublesecurity"] = False
            await ctx.send("Double security disabled")
        else:
            await ctx.send("Please specify yes or no")

        async with aiofiles.open("src/cogs/db/db.json", "w") as f:
            await f.write(json.dumps(data, indent=4))


def setup(bot):
    bot.add_cog(Settings(bot))
