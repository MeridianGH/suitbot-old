import traceback
import sys
from discord.ext import commands
import errors.errors as errors


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

        elif isinstance(error, errors.MoveMembers):
            print(f'[Error ] Invalid permission: \'{ctx.message.author}\' tried to use \'{ctx.command}\'')
            return await ctx.send('You are missing these permissions: Move Members')

        elif isinstance(error, errors.InvalidArguments):
            print(f'[Error ] No or invalid arguments in command \'{ctx.command}\' specified.')
            return await ctx.send('No or invalid arguments specified.')

        elif isinstance(error, commands.CommandError):
            owner = self.bot.get_user(360817252158930954)
            await ctx.send(
                f'Something has went wrong! Please contact the owner and specify your issue: {owner.mention}')
            print(error)

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
