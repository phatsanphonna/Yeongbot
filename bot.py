import discord
from discord.ext import commands, tasks

import datetime
from datetime import datetime, timedelta
from itertools import cycle

import json
import requests
import os

# * Import assets/client_playing.json file
with open('assets/client_playing.json') as f:
    client_playing = json.load(f)

# * Intents Settings
intents = discord.Intents.all()

# * Bot's Infomations
TOKEN = os.environ['client_token']
PASSWORD = os.environ['admin_password']
client = commands.Bot(
    command_prefix='.',
    intents=intents,
    case_insensitive=True
)

# * Client critical rate
CRIT_RATE = 33
CRIT2X_RATE = 35
CRIT_MULTIPLY_RATE1, CRIT_MULTIPLY_RATE2 = 1, 2

# * Remove Commands
client.remove_command('help')

# * Author's Informations
AUTHOR_ICON = 'https://i.ibb.co/tMbrntz/jang-wonyoung-nationality-cover2.jpg'

# * Server's Infomations
GUILD_ID = int(os.environ['GUILD_ID'])
CHANNEL_ID = int(os.environ['CHANNEL_ID'])

# * Timezone Settings
tz_bangkok = timedelta(hours=7)  # Bangkok's Timezone (GMT +7)
on_ready_time = datetime.now() + tz_bangkok


# ? Load Cogs
@client.command()
async def load(ctx, extension):
    if ctx.author is ctx.guild.owner:
        client.load_extension(f'cogs.{extension}')
        print(f'cogs.{filename} loaded!')
    else:
        await ctx.send('You need to be a server owner to use this command!')


# ? Unload Cogs
@client.command()
async def unload(ctx, extension):
    if ctx.author is ctx.guild.owner:
        client.unload_extension(f'cogs.{extension}')
        print(f'cogs.{filename} unloaded!')
    else:
        await ctx.send('You need to be a server owner to use this command!')


# ? Reload Cogs
@client.command()
async def reload(ctx, all_cogs=None):
    if ctx.author is ctx.guild.owner:
        if all_cogs is None:
            for filename in os.listdir('./cogs'):
                if filename.endswith('.py'):
                    client.unload_extension(f'cogs.{filename[:-3]}')
                    client.load_extension(f'cogs.{filename[:-3]}')
                    print(f'cogs.{filename[:-3]} reloaded!')
        else:
            client.unload_extension(f'cogs.{extension}')
            client.load_extension(f'cogs.{extension}')
            print(f'cogs.{filename} reloaded!')
    else:
        await ctx.send('You need to be a server owner to use this command!')


# ! Load all Cogs file
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# ! Run / Required Token to run
client.run(TOKEN)
