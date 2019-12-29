import discord
from discord.ext import commands
from modules.utils import *
from modules.log.logging import get_log_path, get_time, send_log, log_traceback
from datetime import datetime


class MyHelpCommand(commands.DefaultHelpCommand):
    def __init__(self):
        super().__init__()
        self.paginator.prefix = ''
        self.paginator.suffix = ''

    def get_command_signature(self, command):
        if len(command.aliases) > 0:
            aliases = ', '.join(str(self.clean_prefix)+str(alias) for alias in command.aliases)
            title = f'{self.clean_prefix}{command.name}, {aliases}'
        else:
            title = command.name
        return f'{title}{command.signature}'


class General(commands.Cog):
    """All general commands.
    """
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()
        self.bot.help_command.cog = self
        # self._original_help_command = bot.help_command
        # bot.help_command = MyHelpCommand()
        # bot.help_command.cog = self

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Sends the current response time in ms.
        Syntax:      -ping
        Parameters:  None
        Permissions: None
        This will display the elapsed time between a heartbeat and an acknowledged heartbeat.
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass
        ping = str(round(self.bot.latency * 1000)) + 'ms'
        send_log(f'[ Info ] Ping: {ping}')
        await ctx.send(f'Ping: {ping}', delete_after=10)

    @commands.command()
    async def uptime(self, ctx):
        """Tells how long the bot has been running.
        Syntax:      -uptime
        Parameters:  None
        Permissions: None
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        uptime_seconds = round((datetime.now() - self.start_time).total_seconds())
        send_log(f'Current Uptime: {format_seconds(uptime_seconds)}')
        await ctx.send(f'Current Uptime: {format_seconds(uptime_seconds)}', delete_after=10)

    @commands.command(name='clear')
    async def clear(self, ctx):
        """Deletes a given amount of messages in the current channel.
        Syntax:      -clear [Amount]
        Parameters:  [Amount]: The number of messages to delete.
        Permissions: None
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass
        args = str(ctx.message.content).split(' ')
        try:
            deleted = await ctx.message.channel.purge(limit=int(args[1]))
        except discord.HTTPException:
            deleted = 0
        except IndexError:
            raise modules.errors.InvalidArguments
        if len(deleted) == 0:
            return
        elif len(deleted) == 1:
            msg_text = 'message'
        else:
            msg_text = 'messages'
        send_log(f'[ Info ] Deleted {len(deleted)} {msg_text} in #{ctx.message.channel}')
        await ctx.send(f'Deleted {len(deleted)} {msg_text}', delete_after=10)


def setup(bot):
    bot.add_cog(General(bot))
