from discord.ext import commands


class MoveMembers(commands.CheckFailure):
    """Missing Permission: Move Members"""
    pass


class InvalidArguments(commands.CommandError):
    """No or invalid arguments specified."""
    pass
