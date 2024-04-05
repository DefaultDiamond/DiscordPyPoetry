import discord
from discord.ext import commands
import yt_dlp as youtube_dl
from pprint import pprint


ffmpeg_options = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 1 -http_persistent 0',
                  'options': '''\
                  -vaf "firequalizer=gain_entry='entry(32, 42); entry(64, 50); entry(125, 45); entry(250, 30)'\
                  :delay=0.5:fixed=on:zero_phase=on:text=text test:gain=gain_interpolate(32); gain_interpolate(64);\
                  gain_interpolate(125); gain_interpolate(250)"\
                  '''
                  }
                    # equalizer=f=32:width_type=h:width=20:g=400,\
                    # equalizer=f=64:width_type=h:width=20:g=2000,\
                    # equalizer=f=125:width_type=h:width=30:g=45,\
                    # equalizer=f=250:width_type=h:width=30:g=30,\
                    # equalizer=f=500:width_type=h:width=30:g=38,\
                    # equalizer=f=1000:width_type=h:width=30:g=20,\
                    # equalizer=f=2000:width_type=h:width=20:g=10,\
                    # equalizer=f=4000:width_type=h:width=20:g=15\
                    # "'''}
ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '256'
                }],
            }


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def _youtube_extract_n_play(self, url: str, voice_client: discord.VoiceClient) -> None:
        global ffmpeg_option, ydl
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            format_dict = info.get('formats')
            # pprint(format_dict)     # <---- сладко бабахает словарь
            url2 = format_dict[4].get('url')
            voice_client.play(discord.FFmpegPCMAudio(executable='./ffmpeg',
                                                     source=url2, options=ffmpeg_options)
                              )
            voice_client.is_playing()
        return None

    @commands.command()
    async def play(self, ctx, *, url):
        """Нереально наваливает басов с отправленного URL YouTube"""
        try:
            if ctx.author.voice.channel is not None:
                voice_client = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
                if voice_client and voice_client.is_connected():
                    try:
                        self._youtube_extract_n_play(url=url, voice_client=voice_client)
                    except discord.errors.ClientException as Error:
                        await ctx.send(f'{Error}')


                else:
                    voice_client = await ctx.author.voice.channel.connect(reconnect=True)

                    self._youtube_extract_n_play(url=url, voice_client=voice_client)
            else:
                voice_channel = ctx.author.voice.channel
                voice_client = await voice_channel.connect(reconnect=True)

                self._youtube_extract_n_play(url=url, voice_client=voice_client)

        except youtube_dl.utils.ExtractorError as error:
            print('EXCEPTION')
            print(error)
        except youtube_dl.utils.DownloadError:
            print('EXCEPTION DOWNLOADERROR')
        except discord.ext.commands.MissingRequiredArgument:
            print(ctx)
            await ctx.send('Необходимо указать URL адрес после команды')

    @commands.command()
    async def leave(self, ctx):
        """Заставить бота выйти из канала"""
        voice_client = await discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice_channel = voice_client.voice_channel()
        if voice_client and voice_client.is_connected():
            await voice_client.disconnect()
            await ctx.send(f'Бот покинул голосовой канал {voice_channel}')
        else:
            await ctx.send('Бот не находится в голосовом канале')

    @commands.command()
    async def pause(self, ctx):
        """Ставит на паузу проигрываемый трек"""
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
        else:
            await ctx.send('Бот не находится в голосовом канале автора сообщения')
            return 0
        voice_client = await discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client:
            voice_client.pause()

    @commands.command()
    async def resume(self, ctx):
        """Продолжает проигрывать трек"""
        if ctx.author.voice:
            voice_channel = ctx.author.voice.channel
        else:
            await ctx.send('Бот не находится в голосовом канале автора сообщения')
            return 0
        voice_client = await discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice_client:
            if voice_client.is_paused() is True:
                voice_client.resume()
        else:
            await ctx.send('В данный момент ничего не проигрывается')


async def setup(bot):
    await bot.add_cog(Music(bot))
