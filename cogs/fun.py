import random
import discord

from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def slots(self, ctx):
        """Азино три топора"""
        author_id = str(ctx.author.id)

        symbols = ['🍒', '🔔', '7️⃣', '👑', '☠️']

        slot = [0, 1, 2]

        for i in range(3):
            slot[i] = symbols[random.randint(0, 3)]

        is_same = True if slot[0] == slot[1] == slot[2] else False

        if is_same and symbols[4] in slot:
            footer = 'Лузер! Ваш баланс обнулён'
        elif is_same and symbols[3] in slot:
            footer = '+ 5 000 баксов на ваш счёт'
        elif is_same and symbols[2] in slot:
            footer = '+ 10 000 баксов на ваш счёт'
        elif is_same and symbols[1] in slot:
            footer = '+ 15 000 баксов на ваш счёт'
        elif is_same and symbols[0] in slot:
            footer = 'ДЖЕКПОТ!!! + 1 000 000 баксов на ваш счёт'
        elif symbols[0] == slot[0] == slot[1] or slot[0] == slot[2] == symbols[0] or slot[1] == slot[2] == symbols[0]:
            footer = '+ 3 500 баксов на ваш счёт'
        elif symbols[0] in slot:
            footer = '+ 1 500 баксов на ваш счёт'
        else:
            footer = 'Ничего('
        embed = discord.Embed(color=0x36c600, title='🎰 Slots Azino777',
                              description=str(slot[0]) + str(slot[1]) + str(slot[2]))
        embed.set_footer(text=footer, icon_url="https://i.imgur.com/uZIlRnK.png")
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Fun(bot))
