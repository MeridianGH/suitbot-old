import asyncio
import random
import re
import typing as t
from enum import Enum
import time

import discord
import wavelink
from discord.ext import commands

import modules.error_classes
from modules.utils import *
from modules.log.logging import send_log

URL_REGEX = r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:"\".,<>?«»“”‘’]))'
OPTIONS = {
    '1️⃣': 0,
    '2⃣': 1,
    '3⃣': 2,
    '4⃣': 3,
    '5⃣': 4,
}


class AlreadyConnectedToChannel(commands.CommandError):
    pass


class NoVoiceChannel(commands.CommandError):
    pass


class QueueIsEmpty(commands.CommandError):
    pass


class NoTracksFound(commands.CommandError):
    pass


class PlayerIsAlreadyPaused(commands.CommandError):
    pass


class NoMoreTracks(commands.CommandError):
    pass


class NoPreviousTracks(commands.CommandError):
    pass


class InvalidRepeatMode(commands.CommandError):
    pass


class RepeatMode(Enum):
    NONE = 0
    ONE = 1
    ALL = 2


class Queue:
    def __init__(self):
        self._queue = []
        self.position = 0
        self.repeat_mode = RepeatMode.NONE

    @property
    def is_empty(self):
        return not self._queue

    @property
    def current_track(self):
        if not self._queue:
            raise QueueIsEmpty

        if self.position <= len(self._queue) - 1:
            return self._queue[self.position]

    @property
    def upcoming(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            raise QueueIsEmpty

        return self._queue[:self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args):
        self._queue.extend(args)

    def remove(self, index):
        self._queue.pop(index)

    def get_next_track(self):
        if not self._queue:
            raise QueueIsEmpty

        self.position += 1

        if self.position < 0:
            return None
        elif self.position > len(self._queue) - 1:
            if self.repeat_mode == RepeatMode.ALL:
                self.position = 0
            else:
                return None

        return self._queue[self.position]

    def shuffle(self):
        if not self._queue:
            raise QueueIsEmpty

        upcoming = self.upcoming
        random.shuffle(upcoming)
        self._queue = self._queue[:self.position + 1]
        self._queue.extend(upcoming)

    def set_repeat_mode(self, mode):
        if mode == 'none':
            self.repeat_mode = RepeatMode.NONE
        elif mode == '1':
            self.repeat_mode = RepeatMode.ONE
        elif mode == 'all':
            self.repeat_mode = RepeatMode.ALL

    def empty(self):
        self._queue.clear()
        self.position = 0


class Player(wavelink.Player):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = Queue()

    async def connect(self, ctx, channel=None):
        if self.is_connected:
            raise AlreadyConnectedToChannel

        if (channel := getattr(ctx.author.voice, 'channel', channel)) is None:
            raise NoVoiceChannel

        await super().connect(channel.id)
        return channel

    async def teardown(self):
        try:
            await self.destroy()
        except KeyError:
            pass

    async def add_tracks(self, ctx, tracks):
        if not tracks:
            raise NoTracksFound

        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
            await ctx.send(f'Added a playlist to the queue.', delete_after=10)
            send_log(f'[ Info ] Added a playlist to the queue in guild \'{ctx.guild.name}\'.')
        else:
            self.queue.add(tracks[0])
            await ctx.send(f'Added `{tracks[0].title}` to the queue.', delete_after=10)
            send_log(f'[ Info ] Added track {tracks[0].title} to the queue in guild \'{ctx.guild.name}\'.')

        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()

    async def add_choose_tracks(self, ctx, tracks):
        if not tracks:
            raise NoTracksFound

        if isinstance(tracks, wavelink.TrackPlaylist):
            self.queue.add(*tracks.tracks)
            await ctx.send(f'Added a playlist to the queue.', delete_after=10)
            send_log(f'[ Info ] Added a playlist to the queue in guild \'{ctx.guild.name}\'.')
        elif len(tracks) == 1:
            self.queue.add(tracks[0])
            await ctx.send(f'Added `{tracks[0].title}` to the queue.', delete_after=10)
            send_log(f'[ Info ] Added track {tracks[0].title} to the queue in guild \'{ctx.guild.name}\'.')
        else:
            if (track := await self.choose_track(ctx, tracks)) is not None:
                self.queue.add(track)
                await ctx.send(f'Added `{track.title}` to the queue.', delete_after=10)
                send_log(f'[ Info ] Added track {track.title} to the queue in guild \'{ctx.guild.name}\'.')

        if not self.is_playing and not self.queue.is_empty:
            await self.start_playback()

    async def choose_track(self, ctx, tracks):
        def _check(r, u):
            return (
                r.emoji in OPTIONS.keys()
                and u == ctx.author
                and r.message.id == msg.id
            )

        embed = discord.Embed(
            title='Choose a song:',
            description=(
                '\n'.join(
                    f'**{i+1}.** {t.title} ({t.length//60000}:{str(t.length%60).zfill(2)})'
                    for i, t in enumerate(tracks[:5])
                )
            ),
            colour=ctx.author.colour
        )
        embed.set_author(name='Query Results:')
        embed.set_footer(text=f'Invoked by {ctx.author.display_name}', icon_url=ctx.author.avatar_url)

        msg = await ctx.send(embed=embed, delete_after=10)
        for emoji in list(OPTIONS.keys())[:min(len(tracks), len(OPTIONS))]:
            await msg.add_reaction(emoji)

        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=60.0, check=_check)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.message.delete()
        else:
            await msg.delete()
            return tracks[OPTIONS[reaction.emoji]]

    async def start_playback(self):
        await self.play(self.queue.current_track)

    async def advance(self):
        try:
            if (track := self.queue.get_next_track()) is not None:
                await self.play(track)
        except QueueIsEmpty:
            pass

    async def repeat_track(self):
        await self.play(self.queue.current_track)


class Music(commands.Cog, wavelink.WavelinkMixin):
    """All commands for the music player.
    """
    def __init__(self, bot):
        self.bot = bot
        self.wavelink = wavelink.Client(bot=bot)
        self.bot.loop.create_task(self.start_nodes())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if not member.bot and after.channel is None:
            if not [m for m in before.channel.members if not m.bot]:
                await self.get_player(member.guild).teardown()

    @wavelink.WavelinkMixin.listener('on_track_stuck')
    @wavelink.WavelinkMixin.listener('on_track_end')
    @wavelink.WavelinkMixin.listener('on_track_exception')
    async def on_player_stop(self, node, payload):
        if payload.player.queue.repeat_mode == RepeatMode.ONE:
            await payload.player.repeat_track()
        else:
            await payload.player.advance()
        if not payload.player.is_playing and not payload.player.queue.upcoming:
            await payload.player.teardown()

    async def cog_check(self, ctx):
        if isinstance(ctx.channel, discord.DMChannel):
            await ctx.send('Music commands are not available in DMs.', delete_after=10)
            return False

        return True

    async def start_nodes(self):
        await self.bot.wait_until_ready()

        nodes = {
            'MAIN': {
                'host': '127.0.0.1',
                'port': 2333,
                'rest_uri': 'http://127.0.0.1:2333',
                'password': 'youshallnotpass',
                'identifier': 'MAIN',
                'region': 'europe',
            }
        }

        for node in nodes.values():
            await self.wavelink.initiate_node(**node)

    def get_player(self, obj):
        if isinstance(obj, commands.Context):
            return self.wavelink.get_player(obj.guild.id, cls=Player, context=obj)
        elif isinstance(obj, discord.Guild):
            return self.wavelink.get_player(obj.id, cls=Player)

    @commands.command(name='join', aliases=['connect'])
    async def join(self, ctx, *, channel: t.Optional[discord.VoiceChannel]):
        """Joins your current voice channel.
        Syntax:      -join, -connect
        Parameters:  None
        Permissions: None
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        player = self.get_player(ctx)
        channel = await player.connect(ctx, channel)
        await ctx.send(f'Connected to `{channel.name}`.', delete_after=10)
        send_log(f'[ Info ] Connected to channel {channel.name} in guild \'{ctx.guild.name}\'.')

    @join.error
    async def join_error(self, ctx, exc):
        if isinstance(exc, AlreadyConnectedToChannel):
            await ctx.send('Already connected to a voice channel.', delete_after=10)
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send('No suitable voice channel was provided.', delete_after=10)

    @commands.command(name='leave', aliases=['disconnect'])
    async def leave(self, ctx):
        """Leaves the current voice channel.
        Syntax:      -leave, -disconnect
        Parameters:  None
        Permissions: None
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        player = self.get_player(ctx)
        await player.teardown()
        await ctx.send('Disconnected.', delete_after=10)
        send_log(f'[ Info ] Disconnected from channel in guild \'{ctx.guild.name}\'.')

    @commands.command(name='play', aliases=['p'])
    async def play(self, ctx, *, query: t.Optional[str]):
        """Searches for a song and takes the best match.
        Syntax:      -play [query], -p [query]
        Parameters:  [query]: String to search for.
        Permissions: None
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        player = self.get_player(ctx)

        if not player.is_connected:
            await player.connect(ctx)

        if query is None:
            if player.queue.is_empty:
                raise QueueIsEmpty

            await player.set_pause(False)
            await ctx.send('Playback resumed.', delete_after=10)

        else:
            query = query.strip('<>')
            if not re.match(URL_REGEX, query):
                query = f'ytsearch:{query}'

            await player.add_tracks(ctx, await self.wavelink.get_tracks(query))

    @play.error
    async def play_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send('No songs to play as the queue is empty.', delete_after=10)
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send('No suitable voice channel was provided.', delete_after=10)

    @commands.command(name='search', aliases=['s'])
    async def search(self, ctx, *, query: t.Optional[str]):
        """Searches for a song and gives five options to choose.
        Syntax:      -search [query], -s [query]
        Parameters:  [query]: String to search for.
        Permissions: None
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        player = self.get_player(ctx)

        if not player.is_connected:
            await player.connect(ctx)

        if query is None:
            if player.queue.is_empty:
                raise QueueIsEmpty

            await player.set_pause(False)
            await ctx.send('Playback resumed.', delete_after=10)

        else:
            query = query.strip('<>')
            if not re.match(URL_REGEX, query):
                query = f'ytsearch:{query}'

            await player.add_choose_tracks(ctx, await self.wavelink.get_tracks(query))

    @search.error
    async def search_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send('No songs to play as the queue is empty.', delete_after=10)
        elif isinstance(exc, NoVoiceChannel):
            await ctx.send('No suitable voice channel was provided.', delete_after=10)

    @commands.command(name='pause')
    async def pause(self, ctx):
        """Pauses the player.
        Syntax:      -pause
        Parameters:  None
        Permissions: None
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        player = self.get_player(ctx)

        if player.is_paused:
            raise PlayerIsAlreadyPaused

        await player.set_pause(True)
        await ctx.send('Playback paused.', delete_after=10)
        send_log(f'[ Info ] Paused playback in guild \'{ctx.guild.name}\'.')

    @pause.error
    async def pause_error(self, ctx, exc):
        if isinstance(exc, PlayerIsAlreadyPaused):
            await ctx.send('Already paused.', delete_after=10)

    @commands.command(name='stop')
    async def stop(self, ctx):
        """Stops the player.
        Syntax:      -stop
        Parameters:  None
        Permissions: None
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        player = self.get_player(ctx)
        player.queue.empty()
        await player.stop()

        await ctx.send('Playback stopped.', delete_after=10)
        send_log(f'[ Info ] Stopped playback in guild \'{ctx.guild.name}\'.')

    @commands.command(name='skip', aliases=['next'])
    async def skip(self, ctx):
        """Skips to the next track in the queue.
        Syntax:      -skip, -next
        Parameters:  None
        Permissions: None
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        player = self.get_player(ctx)

        if not player.queue.upcoming:
            raise NoMoreTracks

        await player.stop()
        await ctx.send('Playing next track in queue.', delete_after=10)
        send_log(f'[ Info ] Skipped track in guild \'{ctx.guild.name}\'.')

    @skip.error
    async def skip_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send('The queue is currently empty.', delete_after=10)
        elif isinstance(exc, NoMoreTracks):
            await ctx.send('There are no more tracks in the queue.', delete_after=10)

    @commands.command(name='previous', aliases=['prev'])
    async def previous(self, ctx):
        """Plays the previously played track again.
        Syntax:      -previous, -prev
        Parameters:  None
        Permissions: None
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        player = self.get_player(ctx)

        if not player.queue.history:
            raise NoPreviousTracks

        player.queue.position -= 2
        await player.stop()

        await ctx.send('Playing previous track in queue.', delete_after=10)
        send_log(f'[ Info ] Skipped to previous in guild \'{ctx.guild.name}\'.')

    @previous.error
    async def previous_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send('The queue is currently empty.', delete_after=10)
        elif isinstance(exc, NoPreviousTracks):
            await ctx.send('There are no previous tracks in the queue.', delete_after=10)

    @commands.command(name='shuffle')
    async def shuffle(self, ctx):
        """Shuffles the queue.
        Syntax:      -shuffle
        Parameters:  None
        Permissions: None
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        player = self.get_player(ctx)
        player.queue.shuffle()

        await ctx.send('Queue shuffled.', delete_after=10)
        send_log(f'[ Info ] Shuffled queue in guild \'{ctx.guild.name}\'.')

    @shuffle.error
    async def shuffle_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send('The queue could not be shuffled as it is currently empty.', delete_after=10)

    @commands.command(name='repeat', aliases=['loop'])
    async def repeat(self, ctx, mode: str):
        """Sets the repeat mode of the player.
        Syntax:      -repeat [mode], -loop [mode]
        Parameters:  [mode]: Can be either none, 1 or all. Sets the mode respectively.
        Permissions: None
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        if mode not in ('none', '1', 'all'):
            raise InvalidRepeatMode

        player = self.get_player(ctx)
        player.queue.set_repeat_mode(mode)

        await ctx.send(f'The repeat mode has been set to {mode}.', delete_after=10)
        send_log(f'[ Info ] Set repeat mode ({mode}) in guild \'{ctx.guild.name}\'.')

    @commands.command(name='queue', aliases=['list', 'q'])
    async def queue(self, ctx, show: t.Optional[int] = 10):
        """Displays the current queue.
        Syntax:      -queue, -list, -q
        Parameters:  None
        Permissions: None
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        embed = discord.Embed(
            title='Queue:',
            description=f'Showing up to next {show} tracks',
            colour=ctx.author.colour
        )
        embed.set_author(name='Query Results:')
        embed.set_footer(text=f'Requested by {ctx.author.display_name}', icon_url=ctx.author.avatar_url)
        embed.add_field(
            name='Currently playing:',
            value=getattr(player.queue.current_track, 'title', 'No tracks currently playing.'),
            inline=False
        )

        if player.queue.upcoming:
            queue = '\n'.join(f'{player.queue._queue.index(t)}: ' + t.title for t in player.queue.upcoming[:show])

            if len(queue) >= 5500:
                embed = discord.Embed(title='Can\'t show this many entries, please use a limit:',
                                      description='-queue [limit]')
            else:
                entries = iter(queue.split('\n'))
                fields, current = [], next(entries)
                for entry in entries:
                    if len(current) + 1 + len(entry) > 1024:
                        fields.append(current)
                        current = entry
                    else:
                        current += '\n' + entry
                fields.append(current)
                for i in range(len(fields)):
                    embed.add_field(
                        name=f'Queue ({i + 1}):',
                        value=fields[i],
                        inline=False
                    )

        await ctx.send(embed=embed, delete_after=10)
        send_log(f'[ Info ] Sent queue in guild \'{ctx.guild.name}\'.')

    @queue.error
    async def queue_error(self, ctx, exc):
        if isinstance(exc, QueueIsEmpty):
            await ctx.send('The queue is currently empty.', delete_after=10)

    @commands.command(name='now_playing', aliases=['np', 'now'])
    async def now_playing(self, ctx):
        """Show a prompt that displays the currently playing song.
        Syntax:      -now_playing, -np, -now
        Parameters:  None
        Permissions: None
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        player = self.get_player(ctx)

        if player.queue.is_empty:
            raise QueueIsEmpty

        embed = discord.Embed(
            title='Now playing:',
            colour=ctx.author.colour
        )
        embed.set_footer(text=f'Requested by {ctx.author.display_name}', icon_url=ctx.author.avatar_url)
        embed.add_field(name='Now playing:',
                        value=getattr(player.queue.current_track, 'title', 'No tracks currently playing.'),
                        inline=False)
        if player.queue.current_track.is_stream:
            embed.add_field(name='Streaming:', value='🔴 Live')
        else:
            embed.add_field(
                name='Time:',
                value=time.strftime('%H:%M:%S', time.gmtime(player.position / 1000)) + ' / ' +
                      time.strftime('%H:%M:%S', time.gmtime(player.queue.current_track.length / 1000))
            )

        await ctx.send(embed=embed, delete_after=10)
        send_log(f'[ Info ] Sent now_playing in guild \'{ctx.guild.name}\'.')

    @commands.command(name='seek')
    async def seek(self, ctx, *, position: str):
        """Seek to a specific position in the currently playing song.
        Syntax:      -seek [position]
        Parameters:  [position]: Can be in hh:mm:ss, mm:ss or ss format.
        Permissions: None
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        player = self.get_player(ctx)

        if not player.is_connected:
            raise modules.error_classes.NotConnected

        try:
            h, m, s = position.split(':')
        except ValueError:
            try:
                h = 0
                m, s = position.split(':')
            except ValueError:
                h, m = 0, 0
                s = position

        sec = (int(h) * 3600 + int(m) * 60 + int(s)) * 1000

        await player.seek(sec)
        await ctx.send(f'Set the position to `{h}:{m}:{s}`.', delete_after=10)
        send_log(f'[ Info ] Set the position to {h}:{m}:{s} in guild \'{ctx.guild.name}\'.')

    @commands.command(name='volume', aliases=['vol', 'v'])
    async def volume(self, ctx, *, volume: int):
        """Change the player volume.
        Syntax:      -volume [volume], -vol [volume], -v [volume]
        Parameters:  [volume]: The percent to set the volume to.
        Permissions: None
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        player = self.get_player(ctx)

        if not player.is_connected:
            raise modules.error_classes.NotConnected

        if not 0 <= volume <= 100:
            return await ctx.send('Please enter a value between 0 and 100.', delete_after=10)

        await player.set_volume(volume)
        await ctx.send(f'Volume set to **{volume}**%!', delete_after=10)
        send_log(f'[ Info ] Set the volume to `{volume}%` in guild \'{ctx.guild.name}\'.')

    @commands.command(name='remove')
    async def remove(self, ctx, *, position: int):
        """Remove a specified track from the queue. Check with -queue which track number to remove.
        Syntax:      -remove [position]
        Parameters:  [position]: The index of the track to remove.
        Permissions: None
        """
        try:
            await ctx.message.delete()
        except discord.HTTPException:
            pass

        player = self.get_player(ctx)

        if not player.is_connected:
            raise modules.error_classes.NotConnected
        if player.queue.is_empty:
            raise QueueIsEmpty
        if position <= 0:
            await ctx.send(f'Please specify a valid position. Type `-queue` and look at the positions of the tracks.')
            return

        track = player.queue._queue[position].title
        player.queue.remove(position)

        await ctx.send(f'Removed track `{track}` from the queue.')
        send_log(f'[ Info ] Removed track \'{track}\' from the queue in guild \'{ctx.guild.name}\'.')


def setup(bot):
    bot.add_cog(Music(bot))
