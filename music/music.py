import discord
from discord.ext import commands
import wavelink
import time


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'wavelink'):
            self.bot.wavelink = wavelink.Client(self.bot)

        self.bot.loop.create_task(self.start_nodes())

    @staticmethod
    def convert_to_monospace(chars):
        monospace_nums = {'0': '０', '1': '１', '2': '２', '3': '３', '4': '４',
                          '5': '５', '6': '６', '7': '７', '8': '８', '9': '９', ':': '：'}
        for char in chars:
            if char in monospace_nums:
                chars = chars.replace(char, monospace_nums[char])
        return chars

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        # Initiate our nodes. For this example we will use one server.
        # Region should be a discord.py guild.region e.g sydney or us_central (Though this is not technically required)
        await self.bot.wavelink.initiate_node(host='127.0.0.1',
                                              port=2333,
                                              rest_uri='http://127.0.0.1:2333',
                                              password='youshallnotpass',
                                              identifier='main',
                                              region='europe')

    @commands.command(name='connect')
    async def connect(self, ctx, *, channel: discord.VoiceChannel = None):
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise discord.DiscordException('No channel to join. Please either specify a valid channel or join one.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        await ctx.send(f'Connecting to **`{channel.name}`**')
        await player.connect(channel.id)

    @commands.command(name='play')
    async def play(self, ctx, *, query: str):
        tracks = await self.bot.wavelink.get_tracks(f'ytsearch:{query}')

        if not tracks:
            return await ctx.send('Could not find any songs with that query.')

        player = self.bot.wavelink.get_player(ctx.guild.id)
        if not player.is_connected:
            await ctx.invoke(self.connect)

        await ctx.send(f'Added **`{str(tracks[0])}`** to the queue.')
        await player.play(tracks[0])

    @commands.command(name='leave', aliases=['stop'])
    async def leave(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        await player.destroy()

    @commands.command(name='seek')
    async def seek(self, ctx, pos):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        pos = int(pos)
        await player.seek(position=pos * 1000)
        format_time = time.strftime('%M:%S', time.gmtime(pos))
        await ctx.send(f'Skipped to {format_time}.')

    @commands.command(name='pause', aliases=['resume', 'p'])
    async def pause(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if player.paused:
            await player.set_pause(False)
            await ctx.send('Resuming! ⏯')
        elif not player.paused:
            await player.set_pause(True)
            await ctx.send('Pausing! ⏯')

    @commands.command(name='volume', aliases=['vol', 'v'])
    async def volume(self, ctx, vol):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        vol = int(vol)
        if not 0 <= vol <= 100:
            await ctx.send('Please specify a valid value between 0 and 100!')
        else:
            await player.set_volume(vol=vol)
            await ctx.send(f'Volume set to {vol}%!')

    @commands.command(name='now_playing', aliases=['np', 'now'])
    async def now_playing(self, ctx):
        player = self.bot.wavelink.get_player(ctx.guild.id)
        if player.is_playing:
            track = player.current

            percentage = (player.position / track.duration) * 100
            percentage = int(percentage / 4)
            length_dash = percentage - 1
            if length_dash < 1:
                length_empty = 24
            else:
                length_empty = 25 - percentage
            progress_bar = '｜' + (length_dash * '－') + 'Ｏ' + (length_empty * '　') + '｜'

            start = self.convert_to_monospace('00:00')
            current = self.convert_to_monospace(time.strftime('%M:%S', time.gmtime(player.position/1000)))
            end = self.convert_to_monospace(time.strftime('%M:%S', time.gmtime(track.duration/1000)))
            times = start+'　　　　　　'+current+'　　　　　　'+end

            embed = discord.Embed(title='Now playing:', description=f'[{track.author} - {track.title}]({track.uri})',
                                  color=0xff0000)
            embed.add_field(name=progress_bar, value=times)
            embed.set_image(url=track.thumb)
        else:
            embed = discord.Embed(title='Now playing:', color=0xff0000,
                                  description='I\'m not playing anything! Type \'-play\' to add a song!')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Music(bot))
