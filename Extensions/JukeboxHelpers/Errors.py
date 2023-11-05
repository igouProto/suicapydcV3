from discord.ext import commands

"""
Collection of custom errors that the jukebox can throw
"""

class AlreadyConnected(commands.CommandError):
    """Raised when the bot is already connected to a voice channel"""
    pass

class NoVoiceChannel(commands.CommandError):
    """Raised when the user is not connected to a voice channel"""
    pass

class QueueIsEmpty(commands.CommandError):
    """Raised when the queue is empty"""
    pass