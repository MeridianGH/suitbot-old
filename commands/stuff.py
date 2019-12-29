from discord.ext import commands
import discord
import time
import modules.errors
from modules.log.logging import get_log_path, get_time, send_log, log_traceback
import random


class Stuff(commands.Cog):
    """All fun commands
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='shame_on_you')
    async def shame_on_you(self, ctx):
        """Moves the mentioned user out of the channel for five seconds.
        Syntax:      -shame_on_you [User]
        Parameters:  [User]: Mention the user like this: @User
        Permissions: Move Members

        The user will be moved to a different channel and moved back after five seconds.
        He should contemplate his life choices.
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass
        try:
            user = ctx.message.mentions[0]
        except IndexError:
            raise modules.errors.InvalidArguments
        owner_id = ctx.message.channel.guild.owner_id

        if user.id == owner_id and not ctx.message.author.id == owner_id:
            embed = discord.Embed()
            embed.set_image(url='https://i.kym-cdn.com/entries/icons/original/000/030/414/plant.jpg')
            embed.set_footer(text='say sike right now')
            await ctx.send(embed=embed)
        else:
            old_channel = user.voice.channel
            new_channel = discord.utils.find(lambda x: x.name == 'Schäm-Dich-Ecke', ctx.message.channel.guild.channels)
            response = f'Schäm dich, {user.mention}!'
            dm = await user.create_dm()

            await user.move_to(new_channel)
            await ctx.send(response)
            await dm.send(content=response)
            time.sleep(5.0)
            await user.move_to(old_channel)
            send_log(f'[ Info ] Used \'shame_on_you\' on {user}.')

    @commands.command(name='say_sike')
    async def say_sike(self, ctx):
        """Sends an embed with the famous piranha plant.
        Syntax:      -say_sike [User]
        Parameters:  [User] (optional): Will send the image in a private conversation. If not specified, will send
                                       it to the channel where the command has been invoked.
        Permissions: None
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        embed = discord.Embed()
        embed.set_image(url='https://i.kym-cdn.com/entries/icons/original/000/030/414/plant.jpg')
        embed.set_footer(text='say sike right now')

        if len(ctx.message.mentions) == 0:
            await ctx.send(embed=embed, delete_after=10)
            receiver = f'\'{ctx.message.channel}\' in guild \'{ctx.guild}\''
        else:
            user = ctx.message.mentions[0]
            dm = await user.create_dm()
            await dm.send(embed=embed)
            receiver = f'\'{user}\''
        send_log(f'[ Info ] Sent embed \'say_sike\' to {receiver}')

    @commands.command(name='d2_ffs')
    async def d2_ffs(self, ctx):
        """Sends an embed with the Destiny 2 Forsaken parody.
        Syntax:      -d2_ffs [User]
        Parameters:  [User] (optional): Will send the image in a private conversation. If not specified, will send
                                       it to the channel where the command has been invoked.
        Permissions: None
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        embed = discord.Embed()
        embed.set_image(url='https://pbs.twimg.com/media/EG70xsgXYAAw4Ne?format=jpg&name=medium')
        embed.set_footer(text='bungo plz')

        if len(ctx.message.mentions) == 0:
            await ctx.send(embed=embed)
            receiver = f'\'{ctx.message.channel}\' in guild \'{ctx.guild}\''
        else:
            user = ctx.message.mentions[0]
            dm = await user.create_dm()
            await dm.send(embed=embed)
            receiver = f'\'{user}\''
        send_log(f'[ Info ] Sent embed \'d2_ffs\' to {receiver}')

    @commands.command(name='dice_roll', aliases=['random', 'dice'])
    async def dice_roll(self, ctx):
        """Sends a random number between the two parameters given.
        Syntax:      -dice_roll [Min] [Max], -random [Min] [Max], -dice [Min] [Max]
        Parameters:  [Min] (optional): The lowest number that can be rolled. Defaults to 1.
                     [Max] (optional): The highest number that can be rolled. Defaults to 6.
        Permissions: None
        """
        emojis = {'1': '1\u20e3', '2': '2\u20e3', '3': '3\u20e3', '4': '4\u20e3', '5': '5\u20e3',
                  '6': '6\u20e3', '7': '7\u20e3', '8': '8\u20e3', '9': '9\u20e3', '0': '0\u20e3'}
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass
        args = str(ctx.message.content).split(' ')
        try:
            minimum = int(args[1])
        except IndexError:
            minimum = 1
        try:
            maximum = int(args[2])
        except IndexError:
            maximum = 6
        roll = str(random.randint(minimum, maximum))
        message = []
        for num in roll:
            print(num)
            message.append(emojis[num])
        message = ''.join(message)
        await ctx.send(message)


def setup(bot):
    bot.add_cog(Stuff(bot))
