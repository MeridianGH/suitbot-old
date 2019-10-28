from discord.ext import commands
from modules import errors as errors
import youtube_dl

players = {}


class Music(commands.Cog):
    """Music commands like play, join or leave.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='join')
    async def join(self, ctx):
        try:
            await ctx.message.author.voice.channel.connect()
        except AttributeError:
            raise errors.MissingChannel

    @commands.command(name='leave')
    async def leave(self, ctx):
        guild = ctx.message.guild
        voice_client = guild.voice_client
        if voice_client is not None:
            await voice_client.disconnect()
        else:
            raise errors.NotConnected

    @commands.command(name='play')
    async def play(self, ctx, url):
        guild = ctx.message.guild
        voice_client = guild.voice_client
        if voice_client is None:
            try:
                await ctx.message.author.voice.channel.connect()
            except AttributeError:
                raise errors.MissingChannel
            voice_client = guild.voice_client
        song =


def setup(bot):
    bot.add_cog(Music(bot))
