from discord.ext import commands


class MissingPermission(commands.CheckFailure):
    """Missing Permission"""
    message = None

    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = 'You should not see this...'


class InvalidArguments(commands.CommandError):
    """No or invalid arguments specified."""
    pass


class MissingChannel(commands.CommandError):
    """The user is not in a voice channel"""
    pass


class NotConnected(commands.CommandError):
    """The client is not connected to a voice channel in this server."""
    pass


class UserNotConnected(commands.CommandError):
    """The specified user is not connected to a voice channel in this server."""
    pass
