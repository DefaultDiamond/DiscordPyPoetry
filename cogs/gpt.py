import g4f
import discord
from discord.ext import commands


class Gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def gpt(self, ctx, *, message):
        """Отправка вопроса chat GPT"""
        try:
            print(f'prompt is {message}')
            response = await g4f.ChatCompletion.create_async(
                model=g4f.models.gpt_35_turbo,
                messages=[{"role": "user", "content": message}],
            )
            embed = discord.Embed(color=0x191F46, title='GPT Response', description=response)
        except RuntimeWarning as error:
            print(error)
        except RuntimeError as error:
            print(error)
        except discord.ext.commands.errors.CommandInvokeError as error:
            print(error)
            await ctx.send(f'Ошибка: {error}')
        finally:
            print(response)
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Gpt(bot))
