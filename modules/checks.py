from discord.ext import commands
import modules.errors as errors


class Checks:
    @staticmethod
    def move_members():
        def predicate(ctx):
            if ctx.message.author.guild_permissions.move_members:
                return True
            else:
                raise errors.MoveMembers()
        return commands.check(predicate)
