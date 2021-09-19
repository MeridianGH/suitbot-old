# ARCHIVED
This repository hasn't been developed in a really long while and is heavily deprecated.\
A newer, alternative JavaScript version of this bot is available [here](https://github.com/MeridianGH/suitbot).

# SuitBot

![Last commit](https://img.shields.io/github/last-commit/meridianpy/suitbot.svg?color=green&label=Last%20commit) &nbsp;
![Pull Requests](https://img.shields.io/github/issues-pr-raw/meridianpy/suitbot.svg?color=yellow&label=Pull%20requests)  &nbsp;
![Issues](https://img.shields.io/github/issues-raw/meridianpy/suitbot.svg?color=red&label=Issues)

![Stars](https://img.shields.io/github/stars/meridianpy/suitbot.svg?style=social) &nbsp;
![Watchers](https://img.shields.io/github/watchers/meridianpy/suitbot.svg?label=Watchers&style=social) &nbsp;
![Followers](https://img.shields.io/github/followers/meridianpy.svg?label=Followers&style=social)

This is SuitBot. 

SuitBot is a Discord bot with various functions such as as music player or easier user moving.
It is currently only used on my own Discord server and still in development.

I used [discord.py](https://github.com/Rapptz/discord.py) to create the bot
and [WaveLink](https://github.com/PythonistaGuild/Wavelink) to play music.

## How to use

Currently this bot is not available for public use.
I am hosting it 24/7 on a Raspberry Pi, but the bot itself is not in a state that it can be used publicly.

## Commands

These are the current commands. I plan to implement even more as time goes on.
- General:
  ```
  clear          Deletes a given amount of messages in the current channel.
  github         Sends the GitHub link to the source code of the bot.
  help           Shows this message
  ping           Sends the current response time in ms.
  uptime         Tells how long the bot has been running.
- Music:
  ```
  join           Joins your current voice channel.
  leave          Leaves the current voice channel.
  now_playing    Show a prompt that displays the currently playing song.
  pause          Pauses the player.
  play           Searches for a song, takes the best match and starts playback.
  previous       Plays the previously played track again.
  queue          Displays the current queue.
  repeat         Sets the repeat mode of the player.
  search         Searches for a song, gives five options to choose and starts...
  seek           Seek to a specific position in the currently playing song.
  shuffle        Shuffles the queue.
  skip           Skips to the next track in the queue.
  stop           Stops the player.
  volume         Change the player volume.
- Stuff:
  ```
  d2_ffs         Sends an embed with the Destiny 2 Forsaken parody.
  dice_roll      Sends a random number between the two parameters given.
  say_sike       Sends an embed with the famous piranha plant.
  shame_on_you   Moves the mentioned user out of the channel for five seconds.
- Translating:
  ```
  translate    Translates messages by ID or plain text.
- Users:
  ```
  move           Moves all mentioned users to the specified channel.
  move_all       Moves all users in a channel to another channel.
  move_all_guild Moves every user in the entire server to one channel.
