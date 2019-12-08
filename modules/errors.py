import traceback
import sys
from discord.http import Forbidden
from discord.ext import commands


class MoveMembers(commands.CheckFailure):
    """Missing Permission: Move Members"""
    pass


class InvalidArguments(commands.CommandError):
    """No or invalid arguments specified."""
    pass


class MissingChannel(commands.CommandError):
    """The user is not in a voice channel"""
    pass


class NotConnected(commands.CommandError):
    """The client is not connected to a voice channel in this server."""
    pass


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        ignored = (commands.CommandNotFound, commands.UserInputError)
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        elif isinstance(error, MoveMembers):
            print(f'[Error ] Invalid permission: \'{ctx.message.author}\' tried to use \'{ctx.command}\'')
            return await ctx.send('You are missing these permissions: Move Members')

        elif isinstance(error, InvalidArguments):
            print(f'[Error ] No or invalid arguments in command \'{ctx.command}\' specified.')
            return await ctx.send('No or invalid arguments specified.')

        elif isinstance(error, MissingChannel):
            print(f'[Error ] No channel to join specified. {ctx.message.author} is not connected to a channel.')
            return await ctx.send(f'No channel to join specified. {ctx.message.author} is not connected to a channel.')

        elif isinstance(error, NotConnected):
            print(f'[Error ] The client is not connected to a voice channel in this server.')
            return await ctx.send('The client is not connected to a voice channel in this server.')

        elif isinstance(error, Forbidden):
            print('[Error ] HTTP error: Can\'t make API call.')

        elif isinstance(error, commands.CommandError):
            owner = self.bot.get_user(360817252158930954)
            await ctx.send(
                f'Error executing command `{ctx.command.name}`: {str(error)}. \
                Please contact {owner.mention} for further assistance.")')
            print(error)

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
