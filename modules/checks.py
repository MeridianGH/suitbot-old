from discord.ext import commands
import modules.error_classes as errors


class Checks:
    @staticmethod
    def move_members():
        def predicate(ctx):
            if ctx.message.author.guild_permissions.move_members:
                return True
            else:
                raise errors.MissingPermission('Move Members')
        return commands.check(predicate)

    @staticmethod
    def manage_messages():
        def predicate(ctx):
            if ctx.message.author.guild_permissions.manage_messages:
                return True
            else:
                raise errors.MissingPermission('Manage Messages')
        return commands.check(predicate)
