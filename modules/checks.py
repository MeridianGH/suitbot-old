from discord.ext import commands
import errors.errors as errors


class Checks:
    def __init__(self):
        self.move_members = commands.check(self.move_members_predicate)

    @staticmethod
    async def move_members_predicate(ctx):
        if ctx.message.author.guild_permissions.move_members:
            return True
        else:
            raise commands.CommandError(errors.MoveMembers(Exception))
