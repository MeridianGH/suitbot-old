import os
import sys
from dotenv import load_dotenv
from discord.ext import commands


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(relative_path)


load_dotenv(dotenv_path=resource_path('./venv/.env'))
token = os.getenv('DISCORD_TOKEN')

startup_extensions = ['commands.general', 'commands.users', 'commands.stuff', 'errors.error_handling']
bot = commands.Bot(command_prefix='-')


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print('Close this window to stop the bot.')


@bot.event
async def on_command_error(ctx, error):
    owner = bot.get_user(360817252158930954)
    await ctx.send(f'Something has went wrong! Please contact the owner and specify your issue: {owner.mention}')
    print(error)


if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
            print('Successfully loaded extension \'{}\''.format(extension))
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(extension, exc))
    # Invite: https://discordapp.com/api/oauth2/authorize?client_id=610495026002133003&permissions=62915584&scope=bot
    bot.run(token)
