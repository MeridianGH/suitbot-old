from modules.utils import *
import modules.checks as checks
from modules.log.logging import send_log
import discord
from discord.ext import commands

checks = checks.Checks()


class Users(commands.Cog):
    """All user related commands.
    """
    def __init__(self, bot):
        self.bot = bot

    @checks.move_members()
    @commands.command(name='move')
    async def move(self, ctx):
        """Moves all mentioned users to the specified channel.
        Syntax:      -move [Users] [Channel]
        Parameters:  [Users]: Mention all users like this: @User
                     [Channel] (optional): Exact channel name. The user(s) will be moved to this channel.
                                          If no channel name has been specified, all users will be disconnected.
        Permissions: Move Members
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass
        args = str(ctx.message.content).split(' ')
        try:
            channel = self.bot.get_channel(int(args[-1]))
        except TypeError or ValueError:
            channel = discord.utils.find(lambda x: x.name == args[-1], ctx.message.guild.channels)
        except IndexError:
            raise modules.error_classes.InvalidArguments
        user_list = []
        for user in ctx.message.mentions:
            await user.move_to(channel)
            user_list.append(user.name)
        user_list_string = ', '.join(user_list)

        if channel is None:
            if len(user_list) == 1:
                response = f'[ Info ] {user_list_string} has been sent to oblivion.'
            else:
                response = f'[ Info ] ({user_list_string}) have been sent to oblivion.'
        else:
            if len(user_list) == 1:
                response = f'Moved \'{user_list_string}\' to \'{channel}\''
            else:
                response = f'Moved ({user_list_string}) to \'{channel}\''

        await ctx.send(response + '.', delete_after=10)
        send_log(f'[ Info ] {response} in guild \'{ctx.message.guild}\'.')

    @checks.move_members()
    @commands.command(name='move_all')
    async def move_all(self, ctx):
        """Moves all users in a channel to another channel.
        Syntax:      -move_all [Channel1] [Channel2]
        Parameters:  [Channel1]: Exact channel name. The channel the users are currently connected to.
                     [Channel2] (optional): Exact channel name. The user(s) will be moved to this channel.
                                           If no channel name has been specified, all users will be disconnected.
                     If a channel name contains spaces, you have to use the channel ID. To get the ID,
                     enable Discord's Developer Mode in the appearance settings and right click the channel.
        Permissions: Move Members
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass
        args = str(ctx.message.content).split(' ')
        try:
            channel1 = self.bot.get_channel(int(args[1]))
            channel2 = self.bot.get_channel(int(args[2]))
        except TypeError:
            channel1 = discord.utils.find(lambda x: x.name == args[1], ctx.message.guild.channels)
            channel2 = discord.utils.find(lambda x: x.name == args[2], ctx.message.guild.channels)
        except IndexError:
            raise modules.error_classes.InvalidArguments

        user_list = []
        for user in channel1.members:
            await user.move_to(channel2)
            user_list.append(user.name)
        user_list_string = ', '.join(user_list)

        if channel2 is None:
            if len(user_list) == 1:
                response = f'\'{user_list_string}\' has been sent to oblivion.'
            else:
                response = f'({user_list_string}) have been sent to oblivion.'
        else:
            if len(user_list) == 1:
                response = f'Moved \'{user_list_string}\' from \'{channel1}\' to \'{channel2}\''
            else:
                response = f'Moved ({user_list_string}) from \'{channel1}\' to \'{channel2}\''

        await ctx.send(response + '.', delete_after=10)
        send_log(f'[ Info ] {response} in guild \'{ctx.message.guild}\'.')

    @checks.move_members()
    @checks.manage_channels()
    @commands.command(name='move_all_guild')
    async def move_all_guild(self, ctx):
        """Moves every user in the entire server to one channel.
        Syntax:      -move_all_guild [Channel]
        Parameters:  [Channel]: Exact channel name or ID. The user(s) will be moved to this channel.
        Permissions: Move Members, Manage Channels
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        args = str(ctx.message.content).split(' ')
        try:
            channel = self.bot.get_channel(int(args[1]))
        except TypeError:
            channel = discord.utils.find(lambda x: x.name == args[1], ctx.message.guild.channels)
        except IndexError:
            raise modules.error_classes.InvalidArguments

        if channel is None:
            raise modules.error_classes.InvalidArguments

        user_list = []
        for ch in ctx.message.guild.voice_channels:
            for user in ch.members:
                await user.move_to(channel)
                user_list.append(user.name)
        user_list_string = ', '.join(user_list)

        if len(user_list) == 1:
            response = f'Moved \'{user_list_string}\' from the entire server to \'{channel}\''
        else:
            response = f'Moved ({user_list_string}) from the entire server to \'{channel}\''

        await ctx.send(response + '.', delete_after=10)
        send_log(f'[ Info ] {response} in guild \'{ctx.message.guild}\'.')


def setup(bot):
    bot.add_cog(Users(bot))
