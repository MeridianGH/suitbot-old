import os
import sys
from dotenv import load_dotenv
from discord.ext import commands
import discord


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(relative_path)


load_dotenv(dotenv_path=resource_path('./venv/.env'))
token = os.getenv('DISCORD_TOKEN')

startup_extensions = ['commands.general', 'commands.users', 'commands.stuff', 'modules.errors', 'music.advanced']
bot = commands.Bot(command_prefix='-')

maintenance = [discord.Activity(type=discord.ActivityType.playing, name='Maintenance'), discord.Status.dnd]
normal = [discord.Activity(type=discord.ActivityType.playing, name='\'-help\' for info.'), discord.Status.online]
processing = [discord.Activity(type=discord.ActivityType.playing, name='Processing...'), discord.Status.idle]
mode = normal


@bot.event
async def on_ready():
    print(f'\n{bot.user} connected to Discord!')
    print('Close this window to stop the bot.')
    print('__________________________________\n')
    await bot.change_presence(activity=mode[0], status=mode[1])


if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
            print(f'[Status] Successfully loaded extension \'{extension}\'')
        except Exception as e:
            exception = '{}: {}'.format(type(e).__name__, e)
            print(f'[Error ] Failed to load extension {extension}')
            print(f'[Error ] {exception}')
    # Invite: https://discordapp.com/api/oauth2/authorize?client_id=610495026002133003&permissions=62915584&scope=bot
    bot.run(token)
