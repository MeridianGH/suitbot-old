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


@bot.command(name='move')
# @commands.has_permissions(move_members=True)
async def move(ctx):
    args = ctx.message.content.split()[1:]
    for index, arg in enumerate(args):
        if len(arg) < 2:
            args[index-1:index+1] = [' '.join(args[index-1:index+1])]
    channel_text = args[1]
    channel = discord.utils.find(lambda x: x.name == channel_text, ctx.message.channel.guild.channels)

    user_list = []
    for user in ctx.message.mentions:
        await user.move_to(channel)
        user_list.append(user.name)
    user_list_string = ', '.join(user_list)

    if channel is None:
        if len(user_list) == 1:
            response = f'{user_list_string} has been sent to oblivion.'
        else:
            response = f'({user_list_string}) have been sent to oblivion.'
    else:
        if len(user_list) == 1:
            response = f'Moved {user_list_string} to {channel}.'
        else:
            response = f'Moved ({user_list_string}) to {channel}.'
    await ctx.send(response)
    print(response)


@bot.command(name='move_all')
# @commands.has_permissions(move_members=True)
async def move_all(ctx):
    args = ctx.message.content.split()[1:]
    for index, arg in enumerate(args):
        if len(arg) < 2:
            args[index-1:index+1] = [' '.join(args[index-1:index+1])]
    channel1 = discord.utils.find(lambda x: x.name == args[0], ctx.message.channel.guild.channels)
    channel2 = discord.utils.find(lambda x: x.name == args[1], ctx.message.channel.guild.channels)

    user_list = []
    for user in channel1.members:
        await user.move_to(channel2)
        user_list.append(user.name)
    user_list_string = ', '.join(user_list)

    if channel2 is None:
        if len(user_list) == 1:
            response = f'{user_list_string} has been sent to oblivion.'
        else:
            response = f'({user_list_string}) have been sent to oblivion.'
    else:
        if len(user_list) == 1:
            response = f'Moved {user_list_string} from {channel1} to {channel2}.'
        else:
            response = f'Moved ({user_list_string}) from {channel1} to {channel2}.'
    await ctx.send(response)
    print(response)


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

        await user.move_to(new_channel)
        await ctx.send(response)
        await dm.send(content=response)
        time.sleep(5.0)
        await user.move_to(old_channel)
        print(f'Used \'shame_on_you\' successfully on {user}.')


@bot.command(name='say_sike')
async def say_sike(ctx):
    embed = discord.Embed()
    embed.set_image(url='https://i.kym-cdn.com/entries/icons/original/000/030/414/plant.jpg')
    embed.set_footer(text='say sike right now')
    await ctx.send(embed=embed)

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)
    # Invite: https://discordapp.com/api/oauth2/authorize?client_id=610495026002133003&permissions=62915584&scope=bot
    bot.run(token)
