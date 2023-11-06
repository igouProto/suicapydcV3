# suicapydcV3
This is my second rewrite of SUICA, the Discord bot that I made years ago to learn Python and programming in general.

## What is SUICA?
SUICA or Sugoi Ultra Intelligent Chat Assistant is a Discord bot packed with music playback and some other features. Named after Ibuki Suika from the Touhou Project series (not to be confused with Suica, a prepaid rechargeable contactless smart card in Japan). It is currently designed for self-hosting. It currently speaks Traditional Chinese, but under the new structure it's possible to add multi language support.

## Why the rewrite?
A few reasons:
- I abandoned the old code for too long that it's becoming difficult understanding what I was doing, hence prevents me from extending it
- The old code was a hot mess:
    - No documentation
    - Extensions / Cogs are monolithic and scattered everywhere. Me back then did not know how to organize modules
    - Weird to no logic for grouping the commands
    - and so on. It was a mess anyway.
- The libraries I use had gone through many breaking changes and I'm afraid of older versions going obsolete
- I hadn't done Python for a while so I need a refresher
- ...etc

## Okay Cool, how do I run it?
### Prerequisites
- Python > 3.10
- Java
- A copy of Lavalink.jar (put it in the Lavalink dir)
- Your own Discord app and bot token

### Installation and execution
(Rough steps, to be updated with mode details soon)
1. Download the code by either cloning it or download the zip
2. In Suica's directory, place your copy of Lavalink.jar inside ./Lavalink
3. Create a Python virtual environment and activate it
4. Install required packages listed in requirements.txt
5. In a separate console, launch Lavalink.jar with `java -jar Lavalink.jar` (Lavalink must be running for the jukebox to work)
6. Launch Suica with `python Main.py`

### Initial Configuration
Suica has a sort of out-of-the-box set up experience when you first start it up. In the console, you'll be prompted to enter:
- The bot's token
- Default command prefix
- ID of the channel you want the backlog messages go to

The settings will be written to Assets/config.json. We recommend backing up this file.

## A quick list of function restoration status
### Restored
- Message echoing
- Keyword reply
- Omikuji function
- Ping (now with voice latency)
- User manual
- Most jukebox's features

### New Features
- Jukebox:
    - Moves a song in the queue to the top
    - New queue display that implements proper pagination
- Adding and managing custom keyword-reply pairs for guilds
- Messages and strings are sepatated in their own files (for potential multi-langugage support)

### Not yet (or may not be) restored / implemented
- Ship construction recipe generator for Kancolle (wow this is an old feature)
- Stocks function powered by YFinance
- Fake NKODICE minigame
- Jukebox features:
    - Reaction based panel buttons
    - Player seeking (seek, ff/rwd, replay)
    - Saving info of the current track to DM
    - Exporting / importing queue
    - Access to history queue
- Admin features:
    - Purge / bulk removing messages from chat
    - Update announcement
- Doodads:
    - Calculator powered by math.js

## Some future works
- More documentations! This is a crude readme at the moment without too many helpful stuff
- Study Docker to see how can I put Suica in a container
- Restore more function and implement new ones (of course)

# EOF
