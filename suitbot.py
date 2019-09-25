import discord
from discord.ext import commands
import time
# from discord.voice_client import VoiceClient

startup_extensions = ['Music']
bot = commands.Bot(command_prefix='-')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command(name='ping', pass_context=True)
async def ping(ctx):
    await ctx.send(str(round(bot.latency * 1000)) + 'ms')


@bot.command(name='schäm_dich')
# @commands.has_permissions(move_members=True)
async def schaem_dich(ctx):
    old_channel = ctx.message.author.voice.channel
    new_channel = discord.utils.find(lambda x: x.name == 'Schäm-Dich-Ecke', ctx.message.channel.guild.channels)
    user = ctx.message.mentions[0]
    response = f'Schäm dich, {user.mention}!'
    dm = await user.create_dm()
    await dm.send(content=response)
    await user.move_to(new_channel, reason=f'Schäm dich, {user}!')
    await ctx.send(response)
    time.sleep(5.0)
    await user.move_to(old_channel, reason=f'Schäm dich, {user}!')
    print(f'Used \'schaem_dich\' successfully on {user}.')


@bot.command(name='move')
# @commands.has_permissions(move_members=True)
async def move(ctx):
    print(ctx.message.content)
    channel_text = ctx.message.content[ctx.message.content.find('>')+2:]
    print(channel_text)
    channel = discord.utils.find(lambda x: x.name == channel_text, ctx.message.channel.guild.channels)
    user = ctx.message.mentions[0]
    response = f'Moved {user} to {channel}.'
    await user.move_to(channel)
    await ctx.send(response)
    print(f'Moved {user} to {channel}.')


if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)
    # Invite: https://discordapp.com/api/oauth2/authorize?client_id=610495026002133003&permissions=62915584&scope=bot
    bot.run('NjEwNDk1MDI2MDAyMTMzMDAz.XVGH6g.l0GSh1hOCzYMnXAuM6F_u3iRMlM')
