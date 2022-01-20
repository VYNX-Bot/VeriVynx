import json

import aiofiles
import discord

from src.cogs.utils import slash


class SlashSettings(slash.ApplicationCog):

    @slash.slash_command()
    @slash.describe(channel="Verification channel")
    async def set_verify_channel(
        self, ctx: slash.Context, channel: discord.TextChannel
    ):
        """
        Set the verification channel.
        """
        if ctx.author.guild_permissions.administrator == False:
            return await ctx.send(
                "You do not have the required permissions to use this command."
            )
        async with aiofiles.open("src/cogs/db/db.json") as f:
            data = json.loads(await f.read())

        data["guilds"][str(ctx.guild.id)]["verify_channel"] = channel.id

        async with aiofiles.open("src/cogs/db/db.json", "w") as f:
            await f.write(json.dumps(data, indent=4))

        await ctx.send(f"Verification channel set to {channel.mention}")

    @slash.slash_command()
    @slash.describe(role="Verification role")
    async def set_verify_role(self, ctx: slash.Context, role: discord.Role):
        """
        Set the verification role.
        """
        if ctx.author.guild_permissions.administrator == False:
            return await ctx.send(
                "You do not have the required permissions to use this command."
            )
        async with aiofiles.open("src/cogs/db/db.json") as f:
            data = json.loads(await f.read())

        data["guilds"][str(ctx.guild.id)]["verify_role"] = role.id

        async with aiofiles.open("src/cogs/db/db.json", "w") as f:
            await f.write(json.dumps(data, indent=4))

        await ctx.send(f"Verification role set to {role.mention}")

    @slash.slash_command()
    @slash.describe(message="Verification message")
    async def set_verify_message(self, ctx: slash.Context, *, message: str):
        """
        Set the verification channel.
        """
        if ctx.author.guild_permissions.administrator == False:

            return await ctx.send(
                "You do not have the required permissions to use this command."
            )
        async with aiofiles.open("src/cogs/db/db.json") as f:
            data = json.loads(await f.read())

        data["guilds"][str(ctx.guild.id)]["verify_message"] = message

        async with aiofiles.open("src/cogs/db/db.json", "w") as f:
            await f.write(json.dumps(data, indent=4))

        await ctx.send(f"Verification message set to {message}")

    @slash.slash_command()
    @slash.describe(emoji="Verification channel")
    async def set_verify_emoji(self, ctx: slash.Context, emoji: str):
        if ctx.author.guild_permissions.administrator == False:
            return await ctx.send(
                "You do not have the required permissions to use this command."
            )

        async with aiofiles.open("src/cogs/db/db.json") as f:
            data = json.loads(await f.read())

        data["guilds"][str(ctx.guild.id)]["verify_emoji"] = emoji.id

        async with aiofiles.open("src/cogs/db/db.json", "w") as f:
            await f.write(json.dumps(data, indent=4))

        await ctx.send(f"Verification emoji set to {str(emoji)}")

    @slash.slash_command()
    @slash.describe(timeout="Amount of seconds to wait for verification")
    async def set_verify_timeout(self, ctx: slash.Context, timeout: int):
        """
        Set the verification timeout.
        """
        if ctx.author.guild_permissions.administrator == False:
            return await ctx.send(
                "You do not have the required permissions to use this command."
            )
        async with aiofiles.open("src/cogs/db/db.json") as f:
            data = json.loads(await f.read())

        data["guilds"][str(ctx.guild.id)]["verify_timeout"] = timeout

        async with aiofiles.open("src/cogs/db/db.json", "w") as f:
            await f.write(json.dumps(data, indent=4))

        await ctx.send(f"Verification timeout set to {timeout} seconds")

    @slash.slash_command()
    @slash.describe(message="Message after kicked the user")
    async def set_verify_timeout_message(self, ctx: slash.Context, *, message: str):
        """
        Set the verification timeout message.
        """
        if ctx.author.guild_permissions.administrator == False:
            return await ctx.send(
                "You do not have the required permissions to use this command."
            )
        async with aiofiles.open("src/cogs/db/db.json") as f:
            data = json.loads(await f.read())

        data["guilds"][str(ctx.guild.id)]["verify_timeout_message"] = message

        async with aiofiles.open("src/cogs/db/db.json", "w") as f:
            await f.write(json.dumps(data, indent=4))

        await ctx.send(f"Verification timeout message set to {message}")
    
    @slash.slash_command()
    @slash.describe(yes_or_no="Response: Yes or no")
    async def set_double_verify(self, ctx: slash.Context, yes_or_no: str):
        """
        Set the double verification.
        """
        if ctx.author.guild_permissions.administrator == False:
            return await ctx.send(
                "You do not have the required permissions to use this command."
            )
        async with aiofiles.open("src/cogs/db/db.json") as f:
            data = json.loads(await f.read())

        data["guilds"][str(ctx.guild.id)]["double_verify"] = yes_or_no

        async with aiofiles.open("src/cogs/db/db.json", "w") as f:
            await f.write(json.dumps(data, indent=4))

        await ctx.send(f"Double verification set to {yes_or_no}")

    @slash.slash_command()
    @slash.describe(command="The command you want to get help")
    async def help(self, ctx: slash.Context, command: str = None):
        """
        Get help for a command.
        """
        if command is None:
            embed = discord.Embed(
                title="Help", description="", color=discord.Color.blue()
            )
            for command in self.bot.commands:
                if command.hidden:
                    continue
                if command.aliases:
                    aliases = " | ".join(command.aliases)
                    embed.add_field(
                        name=f"{command.name} | {aliases}",
                        value=command.help,
                        inline=True,
                    )
                else:
                    embed.add_field(name=command.name, value=command.help, inline=True)
            await ctx.send(embed=embed)

        else:
            command = self.bot.get_command(command)
            if command is None:
                await ctx.send("That command does not exist.")
                return
            embed = discord.Embed(
                title=f"Help: {command.name}",
                description=command.help,
                color=discord.Color.blue(),
            )
            embed.add_field(name="Usage", value=command.usage)
            embed.add_field(
                name="Aliases",
                value=", ".join(command.aliases) if command.aliases else "None",
            )
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(SlashSettings(bot))
