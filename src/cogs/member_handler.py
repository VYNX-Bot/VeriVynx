import asyncio
import json
import random

import aiofiles
import discord
from discord.ext import commands


class Member_Handler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.current = {}

    async def verify_timeout(self, member, guild, data, msg):
        if data["guilds"][str(guild.id)]["verify_timeout"] is not None:
            await asyncio.sleep(data["guilds"][str(guild.id)]["verify_timeout"])
            await msg.delete()
            await member.send(
                "You don't react in {} seconds, so you are kicked from the server.".format(
                    data["guilds"][str(guild.id)]["verify_timeout"]
                )
            )
            await member.kick()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.bot.get_guild(member.guild.id)

        async with aiofiles.open("src/cogs/db/db.json") as f:
            data = json.loads(await f.read())

        if data["guilds"][str(guild.id)]["verify_channel"] != None:
            channel = guild.get_channel(data["guilds"][str(guild.id)]["verify_channel"])
            embed = discord.Embed(
                title="Welcome to {}!".format(guild.name),
                description=data["guilds"][str(guild.id)]["verify_message"],
                color=discord.Color.green(),
            )
            msg = await channel.send(embed=embed)
            await msg.add_reaction(self.bot.get_emoji(data["guilds"][str(guild.id)]["verify_emoji"]))
            self.current[str(member.id)] = self.bot.loop.create_task(self.verify_timeout(member, guild, data, msg))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        print("reacted")
        async with aiofiles.open("src/cogs/db/db.json") as f:
            data = json.loads(await f.read())

        if data["guilds"][str(guild.id)]["verify_channel"] != None:
            channel = guild.get_channel(data["guilds"][str(guild.id)]["verify_channel"])
            if payload.emoji.id == data["guilds"][str(guild.id)]["verify_emoji"]:
                if member.id == self.bot.user.id:
                    return
                if not data["guilds"][str(guild.id)]["verify_role"] in list(member.roles):
                    print("cancelled")
                    self.current[str(payload.user_id)].cancel()
                    del self.current[str(payload.user_id)]
                if data["guilds"][str(guild.id)]["doublesecurity"]:
                    equation1 = random.randint(2, 10)
                    equation2 = random.randint(2, 10)
                    operator = random.choice(["+", "-", "*"])
                    result = eval(str(equation1) + operator + str(equation2))
                    embed = discord.Embed(
                        title="Let's do some quick math.",
                        description="Since this server has double security, you need to solve the following equation:\n{} {} {} = ?".format(
                            equation1, operator, equation2
                        ),
                        color=discord.Color.green(),
                    )
                    await channel.send(embed=embed)

                    def check(msg):
                        return msg.author == member and msg.channel == channel

                    try:
                        msg = await self.bot.wait_for(
                            "message", check=check, timeout=60
                        )
                    except asyncio.TimeoutError:
                        await member.send(
                            "You took too long to solve the equation. You have been automatically removed from the verification process."
                        )
                        await member.kick()
                        return
                    if msg.content == str(result):
                        await member.add_roles(
                            guild.get_role(data["guilds"][str(guild.id)]["verify_role"])
                        )
                        await member.send(
                            "You have been verified and have been given the role {}!".format(
                                guild.get_role(
                                    data["guilds"][str(guild.id)]["verify_role"]
                                ).name
                            )
                        )
                        await msg.delete()
                        await channel.send(
                            "You have been verified and have been given the role {}!".format(
                                guild.get_role(
                                    data["guilds"][str(guild.id)]["verify_role"]
                                ).name
                            )
                        )
                    else:
                        await member.send("You answer the equation wrong")
                        await member.kick()
                        return
                await member.add_roles(
                    guild.get_role(data["guilds"][str(guild.id)]["verify_role"])
                )
                await channel.send(f"{member.mention} has been verified!")
                await member.send(f"You have been verified in {guild.name}!")
                a = await channel.history(limit=None).flatten()
                for m in a:
                    if m.author == member or m.author == self.bot.user:
                        await m.delete()
            else:
                return


def setup(bot):
    bot.add_cog(Member_Handler(bot))
