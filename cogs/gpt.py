import g4f
import discord
from discord.ext import commands
import asyncio


class Gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# TODO | Сделать функцию РАБОЧЕЙ БЛЕЯТЬ
    @commands.command()
    async def gpt(self, ctx, *, message: str):
        """
        Отправка вопроса chat GPT. В данный момент провайдеры поумнели, а я нет, поэтому функция не работает
        """
        try:
            print(f'prompt is {message}')
            response = g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_35_turbo,
                messages=[{"role": "user", "content": message}],
            )
            embed = discord.Embed(color=0x191F46, title='GPT Response', description=response)
        except RuntimeWarning as error:
            print(error)
        except TimeoutError as error:
            print(error)
            await ctx.send(f'Ошибка: {error}')
        finally:
            await asyncio.wait_for(response, timeout=120)
            if response:
                print(response)
                await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Gpt(bot))
