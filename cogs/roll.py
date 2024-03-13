from discord.ext import commands
import discord
import random


class Rolls(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx, *, roll: str):
        """
        Кидает кубик | пример использования команды: !roll 2d6+4
        """
        dice = (roll.lower()).split('d')
        # print(dice)
        plus = None
        dice_sum = 0
        suma = 0
        number_of_cubes = dice[0]
        if '+' in roll:
            plus = roll.split('+')
            if plus[1] == '':
                plus[1] = '0'
            suma += int(plus[1])
            dice = dice[1].split('+')
            dice[0] = dice[1]
        if number_of_cubes == '' or number_of_cubes == '1' or number_of_cubes == '0':
            result = ''
            add = random.randint(1, int(dice[1]))
            result += f'🎲 {add} 🎲'
            suma += add
            dice_sum += add
        else:
            result = '🎲 ('
            for i in range(int(number_of_cubes)):
                if i != int(number_of_cubes) - 1:
                    add = random.randint(1, int(dice[1]))
                    result += f'{add}, '
                    suma += add
                    dice_sum += add
                else:
                    add = random.randint(1, int(dice[1]))
                    result += f'{add}'
                    suma += add
                    dice_sum += add
            result += ') 🎲'
        if plus is not None:
            embed = discord.Embed(color=0x991F46, title=f'Roll: {roll}',
                                  description=f'{result}\nsum of the dices = {dice_sum}\nplus = {plus[1]}\nresult = {suma}')
        else:
            embed = discord.Embed(color=0x991F46, title=f'Roll: {roll}',
                                  description=f'{result}\nresult = {suma}')
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Rolls(bot))
