import os
import sys
import time
from dotenv import load_dotenv
import discord
from discord.ext import commands
# from discord.voice_client import VoiceClient


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(relative_path)


load_dotenv(dotenv_path=resource_path('./venv/.env'))
token = os.getenv('DISCORD_TOKEN')

startup_extensions = []
bot = commands.Bot(command_prefix='-')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print('Close this window to stop the bot.')


@bot.command(name='ping')
async def ping(ctx):
    await ctx.send(str(round(bot.latency * 1000)) + 'ms')


@bot.command(name='shame_on_you')
# @commands.has_permissions(move_members=True)
async def shame_on_you(ctx):
    user = ctx.message.mentions[0]
    owner_id = ctx.message.channel.guild.owner_id
    if user.id == owner_id and not ctx.message.author.id == owner_id:
        embed = discord.Embed()
        embed.set_image(url='https://i.kym-cdn.com/entries/icons/original/000/030/414/plant.jpg')
        embed.set_footer(text='say sike right now')
        await ctx.send(embed=embed)
    else:
        old_channel = user.voice.channel
        new_channel = discord.utils.find(lambda x: x.name == 'Schäm-Dich-Ecke', ctx.message.channel.guild.channels)
        response = f'Schäm dich, {user.mention}!'
        dm = await user.create_dm()
        await user.move_to(new_channel, reason=f'Schäm dich, {user}!')
        await ctx.send(response)
        await dm.send(content=response)
        time.sleep(5.0)
        await user.move_to(old_channel, reason=f'Schäm dich, {user}!')
        print(f'Used \'schaem_dich\' successfully on {user}.')


@bot.command(name='move')
# @commands.has_permissions(move_members=True)
async def move(ctx):
    channel_text = ctx.message.content[ctx.message.content.find('{')+1:]
    channel = discord.utils.find(lambda x: x.name == channel_text, ctx.message.channel.guild.channels)
    user_list = []
    for user in ctx.message.mentions:
        await user.move_to(channel)
        user_list.append(user.name)
    user_list_string = ', '.join(user_list)
    response = f'Moved ({user_list_string}) to {channel}.'
    await ctx.send(response)
    print(response)


@bot.command(name='move_all')
# @commands.has_permissions(move_members=True)
async def move_all(ctx):
    index1 = ctx.message.content.find('{', 1)
    index2 = ctx.message.content.find('{', index1 + 1)
    channel_text1 = ctx.message.content[index1+1:index2-1]
    channel_text2 = ctx.message.content[index2+1:]
    channel1 = discord.utils.find(lambda x: x.name == channel_text1, ctx.message.channel.guild.channels)
    channel2 = discord.utils.find(lambda x: x.name == channel_text2, ctx.message.channel.guild.channels)
    user_list = []
    for user in channel1.members:
        await user.move_to(channel2)
        user_list.append(user.name)
    user_list_string = ', '.join(user_list)
    response = f'Moved ({user_list_string}) to {channel2}.'
    await ctx.send(response)
    print(response)


if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)
    # Invite: https://discordapp.com/api/oauth2/authorize?client_id=610495026002133003&permissions=62915584&scope=bot
    bot.run(token)
