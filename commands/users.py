from modules.utils import *
import modules.checks as checks
import discord

checks = checks.Checks()


class Users(commands.Cog):
    """All user related commands.
    """
    @checks.move_members
    @commands.command(name='move')
    async def move(self, ctx):
        """Moves all mentioned users to the specified channel.
        Parameters:  [Users]: Mention all users like this: @User
                     [Channel] (optional): Exact channel name. The user(s) will be moved to this channel.
                                          If no channel name has been specified, all users will be disconnected.
        Permissions: Move Members
        """
        await ctx.message.delete()
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

        await ctx.send(response)
        print(response)

    @checks.move_members
    @commands.command(name='move_all')
    async def move_all(self, ctx):
        """Moves all users in a channel to another channel.
        Parameters:  [Channel1]: Exact channel name. The channel the users are currently connected to.
                     [Channel2] (optional): Exact channel name. The user(s) will be moved to this channel.
                                           If no channel name has been specified, all users will be disconnected.
        Permissions: Move Members
        """
        await ctx.message.delete()

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

        await ctx.send(response)
        print(response)

    @checks.move_members
    @commands.command(name='move_all_guild')
    async def move_all_guild(self, ctx):
        """Moves every user in the entire server to one channel.
        """
        await ctx.message.delete()
        args = arg_parse(ctx)
        channel = discord.utils.find(lambda x: x.name == args[0], ctx.message.channel.guild.channels)

        for ch in ctx.message.channel.guild.voice_channels:
            for user in ch.members:
                await user.move_to(channel)


def setup(bot):
    bot.add_cog(Users(bot))
