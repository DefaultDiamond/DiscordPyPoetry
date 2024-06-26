import discord
from discord.ext import commands


class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx, *, message):
        await ctx.send(message)


async def setup(bot):
    await bot.add_cog(Test(bot))