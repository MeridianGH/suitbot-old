# import discord
from discord.ext import commands
from discord.voice_client import VoiceClient

startup_extensions = ['Music']
bot = commands.Bot('-')


class MainCommands:
    def __init__(self, bot):
        self.bot = bot


@bot.event
async def on_ready():
    print('Bot Online!')


@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send('Pong :ping_pong:')


if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc =


bot.run('NjEwNDk1MDI2MDAyMTMzMDAz.XVGH6g.l0GSh1hOCzYMnXAuM6F_u3iRMlM')
