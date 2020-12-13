from discord.ext import commands
from discord.http import Forbidden
import modules.error_classes
import traceback
from modules.log.logging import send_log, log_traceback
from yandex_translate import YandexTranslateException


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

        elif isinstance(error, modules.error_classes.MissingPermission):
            permission = modules.error_classes.MissingPermission.message
            send_log(f'[Error ] Invalid permission: \'{ctx.author}\' tried to use \'{ctx.command}\' without permission '
                     f'{permission}')
            return await ctx.send(f'You are missing these permissions: {permission}')

        elif isinstance(error, modules.error_classes.InvalidArguments):
            send_log(f'[Error ] No or invalid arguments in command \'{ctx.command}\' specified.')
            return await ctx.send('No or invalid arguments specified.')

        elif isinstance(error, modules.error_classes.MissingChannel):
            send_log(f'[Error ] No channel to join specified. \'{ctx.author}\' is not connected to a channel.')
            return await ctx.send(f'No channel to join specified. {ctx.author.mention} is not connected to a channel.')

        elif isinstance(error, modules.error_classes.NotConnected):
            send_log(f'[Error ] The client is not connected to a voice channel in \'{ctx.guild.name}\'.')
            return await ctx.send('The client is not connected to a voice channel in this server.')

        elif isinstance(error, modules.error_classes.UserNotConnected):
            send_log(f'[Error ] The specified user is not connected to a voice channel in \'{ctx.guild.name}\'.')
            return await ctx.send('The specified user is not connected to a voice channel in this server.')

        elif isinstance(error, YandexTranslateException):
            send_log(f'[Error ] Failed to get response from YandexTranslate.')
            return await ctx.send('Failed to get response from https://translate.yandex.com.')

        elif isinstance(error, Forbidden):
            send_log(f'[Error ] HTTP error: Can\'t make API call for command {ctx.command}.')

        elif isinstance(error, commands.CommandError):
            owner = self.bot.get_user(360817252158930954)
            await ctx.send(f'Error executing command `{ctx.command.name}`: '
                           f'{traceback.format_exception(type(error), error, error.__traceback__)[-1]}'
                           f'Please contact {owner.mention} for further assistance.")')
        else:
            owner = self.bot.get_user(360817252158930954)
            log_traceback(traceback.format_exception(type(error), error, error.__traceback__), ctx.command)
            await ctx.send(f'An unexpected error has occured. '
                           f'The error has been logged and {owner.mention} has been notified.')


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
