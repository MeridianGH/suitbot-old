from modules.utils import *


class General(commands.Cog):
    """All general commands.
    """
    def __init__(self, bot):
        self.bot = bot
        self.bot.help_command.cog = self

    @commands.command(name='ping')
    async def ping(self, ctx):
        """Sends the current response time in ms.
        Parameters:  None
        Permissions: None
        This will display the elapsed time between a heartbeat and an acknowledged heartbeat.
        """
        message = await ctx.send(str(round(self.bot.latency * 1000)) + 'ms')
        await ctx.message.delete(delay=5)
        await message.delete(delay=5)

    @commands.command(name='clear')
    async def clear(self, ctx):
        """Deletes a given amount of messages in the current channel.
        Parameters:  [Amount]: The number of messages to delete.
        Permissions: None
        """
        await ctx.message.delete()
        args = arg_parse(ctx)
        if len(args) == 0:
            args = [10]
        deleted = await ctx.message.channel.purge(limit=int(args[0]))
        message = await ctx.send('Deleted {} message(s)'.format(len(deleted)))
        await message.delete(delay=5)


def setup(bot):
    bot.add_cog(General(bot))
