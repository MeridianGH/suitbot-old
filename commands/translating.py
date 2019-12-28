import discord
from discord.ext import commands
import sys
import os
from modules.utils import *
from modules.log.logging import get_log_path, get_time, send_log, log_traceback
from dotenv import load_dotenv
from yandex_translate import YandexTranslate
from urllib.parse import quote_plus


def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(relative_path)


load_dotenv(dotenv_path=resource_path('./venv/.env'))
yandex = os.getenv('YANDEX')
image = 'https://cdn.discordapp.com/app-icons/655725830252658688/4672f971d906465e219d6ae211798703.png'
translator = YandexTranslate(yandex)


class Translating(commands.Cog):
    """Commands for translating Discord messages using Yandex Translate.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='translate')
    async def translate(self, ctx):
        """Translates messages by ID or plain text.
        Syntax:      -translate [Message]
        Parameters:  [Message]: A ID of a message or just plain text.
        Permissions: None
        To get the ID of another message enable Developer Mode in
        Discord's appearance settings and click the three dots to
        the right of the message and copy its ID.
        """
        print(ctx.message.content)
        try:
            message_id = int(str(ctx.message.content).replace(f'-translate', ''))
            message = await ctx.message.channel.fetch_message(message_id)
            await message.channel.send(embed=translate_message(message))
        except ValueError:
            await ctx.send(embed=translate_message(ctx.message))


def translate_message(message):
    text = str(message.content).replace(f'-translate', '')

    message_link = f'https://discordapp.com/channels/{message.guild.id}/{message.channel.id}/{message.id}'

    translated = translator.translate(text, 'en')
    translated_text = str(translated['text'][0])
    lang = translated['lang']
    yandex_link = f'https://translate.yandex.com/?lang={lang}&text={quote_plus(text)}'
    embed = discord.Embed(title='TranslateBot', color=0xff0000,
                          description=f'[In case this translation is incorrect, try this link.]({yandex_link})')
    embed.add_field(name='Translation:', value=f'[{translated_text}]({yandex_link})')
    embed.add_field(name=f'Original message by {message.author.name}:', value=f'[{text}]({message_link})', inline=False)
    embed.set_thumbnail(url=image)
    return embed


def setup(bot):
    bot.add_cog(Translating(bot))
