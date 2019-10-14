import os
import sys
import time
from dotenv import load_dotenv
import discord
from discord.ext import commands
from modules.utils import *
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


class General(commands.Cog):
    """All general commands.
    """
    def __init__(self):
        bot.help_command.cog = self

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Sends the current response time in ms.
        Parameters:  None
        Permissions: None
        This will display the elapsed time between a heartbeat and an acknowledged heartbeat.
        """
        await ctx.send(str(round(bot.latency * 1000)) + 'ms')

    @commands.command(name='clear')
    async def clear(self, ctx):
        """Deletes a given amount of messages in the current channel.
        Parameters:  [Amount]: The number of messages to delete.
        Permissions: None
        """
        args = arg_parse(ctx)
        if len(args) == 0:
            args[0] = 10
        deleted = await ctx.message.channel.purge(limit=int(args[0]+1))
        await ctx.message.channel.send('Deleted {} message(s)'.format(len(deleted)))


bot.add_cog(General())


class Users(commands.Cog):
    """All user related commands.
    """
    @commands.command(name='move')
    async def move(self, ctx):
        """Moves all mentioned users to the specified channel.
        Parameters:  [Users]: Mention all users like this: @User
                     [Channel] (optional): Exact channel name. The user(s) will be moved to this channel.
                                          If no channel name has been specified, all users will be disconnected.
        Permissions: Move Members
        """
        if ctx.message.author.guild_permissions.move_members:
            args = arg_parse(ctx)
            channel_text = args[-1]
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
        else:
            response = 'You do not have the permissions to do this.'

        await ctx.send(response)
        print(response)

    @commands.command(name='move_all')
    async def move_all(self, ctx):
        """Moves all users in a channel to another channel.
        Parameters:  [Channel1]: Exact channel name. The channel the users are currently connected to.
                     [Channel2] (optional): Exact channel name. The user(s) will be moved to this channel.
                                           If no channel name has been specified, all users will be disconnected.
        Permissions: Move Members
        """
        if ctx.message.author.guild_permissions.move_members:
            args = arg_parse(ctx)
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
        else:
            response = 'You do not have the permissions to do this.'

        await ctx.send(response)
        print(response)

    @commands.command(name='move_all_guild')
    async def move_all_guild(self, ctx):
        args = arg_parse(ctx)
        channel = discord.utils.find(lambda x: x.name == args[0], ctx.message.channel.guild.channels)

        for ch in ctx.message.channel.guild.voice_channels:
            for user in ch.members:
                await user.move_to(channel)

    @commands.command(name='shame_on_you')
    async def shame_on_you(self, ctx):
        """Moves the mentioned user out of the channel for five seconds.
        Parameters:  [Users]: Mention all users like this: @User
        Permissions: Move Members

        The user will be moved to a different channel and moved back after five seconds.
        He should contemplate his life choices.
        """
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

    @commands.command(name='say_sike')
    async def say_sike(self, ctx):
        """Sends an embed with the famous piranha plant.
        Parameters:  [User] (optional): Will send the image in a private conversation. If not specified, will send
                                       it to the channel where the command has been invoked.
        Permissions: None
        """
        embed = discord.Embed()
        embed.set_image(url='https://i.kym-cdn.com/entries/icons/original/000/030/414/plant.jpg')
        embed.set_footer(text='say sike right now')
        if len(ctx.message.mentions) == 0:
            await ctx.send(embed=embed)
        else:
            user = ctx.message.mentions[0]
            dm = await user.create_dm()
            await dm.send(embed=embed)


bot.add_cog(Users())

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(e)
    # Invite: https://discordapp.com/api/oauth2/authorize?client_id=610495026002133003&permissions=62915584&scope=bot
    bot.run(token)
