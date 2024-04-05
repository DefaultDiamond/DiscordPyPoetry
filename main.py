import asyncio
import os.path
import sys

from config import settings

from cogs import gpt, fun, listeners, music, misc, roll, test

from rich import print

from discord.ext import commands
from discord import Intents

import tarfile


ffmpeg_file = 'ffmpeg.tar.gz'

if not os.path.isfile('ffmpeg'):
    with tarfile.open(ffmpeg_file, 'r:gz') as tar:
        print('[b yellow]Разархивируем ffmpeg')
        tar.extractall()


print(f'[bold yellow]Python {sys.version}')

intents = Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=settings['prefix'], intents=intents)

# import cogs here
asyncio.run(fun.setup(bot))
asyncio.run(gpt.setup(bot))
asyncio.run(listeners.setup(bot))
asyncio.run(music.setup(bot))
asyncio.run(misc.setup(bot))
asyncio.run(roll.setup(bot))
# asyncio.run(test.setup(bot))


print(f'[b green]Starting a bot.')

try:
    bot.run(token=settings['token'])
except RuntimeError as error:
    print(error)
    bot.run(token=settings['token'])
finally:
    pass
