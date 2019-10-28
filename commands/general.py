from discord.ext import commands
from modules.utils import *
from datetime import datetime


class General(commands.Cog):
    """All general commands.
    """
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()
        self.bot.help_command.cog = self

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Sends the current response time in ms.
        Syntax:      -ping
        Parameters:  None
        Permissions: None
        This will display the elapsed time between a heartbeat and an acknowledged heartbeat.
        """
        ping = str(round(self.bot.latency * 1000)) + 'ms'
        print(f'[ Info ] Ping: {ping}')
        message = await ctx.send(ping)
        await ctx.message.delete(delay=5)
        await message.delete(delay=5)

    @commands.command()
    async def uptime(self, ctx):
        """Tells how long the bot has been running.
        Syntax:      -uptime
        Parameters:  None
        Permissions: None
        """
        uptime_seconds = round((datetime.now() - self.start_time).total_seconds())
        await ctx.send(f"Current Uptime: {format_seconds(uptime_seconds)}")

    @commands.command(name='clear')
    async def clear(self, ctx):
        """Deletes a given amount of messages in the current channel.
        Syntax:      -clear [Amount]
        Parameters:  [Amount]: The number of messages to delete.
        Permissions: None
        """
        await ctx.message.delete()
        args = arg_parse(ctx)
        deleted = await ctx.message.channel.purge(limit=int(args[0]))
        print(f'[ Info ] Deleted {len(deleted)} messages in #{ctx.message.channel}')
        message = await ctx.send('Deleted {} message(s)'.format(len(deleted)))
        await message.delete(delay=5)


def setup(bot):
    bot.add_cog(General(bot))
