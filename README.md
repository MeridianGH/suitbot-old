# SuitBot

![Last commit](https://img.shields.io/github/last-commit/meridianpy/suitbot.svg?color=green&label=Last%20commit) &nbsp;
![Pull Requests](https://img.shields.io/github/issues-pr-raw/meridianpy/suitbot.svg?color=yellow&label=Pull%20requests)  &nbsp;
![Issues](https://img.shields.io/github/issues-raw/meridianpy/suitbot.svg?color=red&label=Issues)

![Stars](https://img.shields.io/github/stars/meridianpy/suitbot.svg?style=social) &nbsp;
![Watchers](https://img.shields.io/github/watchers/meridianpy/suitbot.svg?label=Watchers&style=social) &nbsp;
![Followers](https://img.shields.io/github/followers/meridianpy.svg?label=Followers&style=social)

This is my own Discord bot. I use it for some various unusual commands.
I used [discord.py](https://github.com/Rapptz/discord.py) to create the bot
and [WaveLink](https://github.com/PythonistaGuild/Wavelink) to play music.

## How to use

Currently this bot is not available for public use.
I plan to host it on a server running 24/7 and make it public, but that will take a while.

## Commands

These are the current commands. I plan to implement even more functionality.
- General:
  ```
  clear        Deletes a given amount of messages in the current channel.
  help         Shows this message
  ping         Sends the current response time in ms.
  uptime       Tells how long the bot has been running.
- Music:
  ```
  connect      Connect to voice.
  info         Retrieve various Music / WaveLink information.
  now_playing  Invoke the player controller.
  pause        Pause the currently playing song.
  play         Queue a song or playlist for playback.
  queue        Retrieve a list of currently queued songs.
  repeat       Repeat the currently playing song.
  resume       Resume a currently paused song.
  shuffle      Shuffle the current queue.
  skip         Skip the current song.
  stop         Stop the player, disconnect and clear the queue.
  volume       Change the player volume.
- Stuff:
  ```
  d2_ffs       Sends an embed with the D2 Forsaken parody.
  say_sike     Sends an embed with the famous piranha plant.
  shame_on_you Moves the mentioned user out of the channel for five seconds.
- Users:
  ```
  move         Moves all mentioned users to the specified channel.
  move_all     Moves all users in a channel to another channel.
