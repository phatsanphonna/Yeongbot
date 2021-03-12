import discord
from discord.ext import commands, tasks

import json

# * Import assets/client_playing.json file
with open('assets/client_playing.json') as f:
    client_playing = json.load(f)


class Client(commands.Cog):
    def __init__(self, client, status, on_ready_time, GUILD_ID, CHANNEL_ID):
        self.client = client
        self.status = status
        self.on_ready_time = on_ready_time
        self.GUILD_ID = GUILD_ID
        self.CHANNEL_ID = CHANNEL_ID

    # * When client is online!
    @commands.Cog.listener()
    async def on_ready(self):
        guild = client.get_guild(GUILD_ID)
        channel = guild.get_channel(CHANNEL_ID)

        change_status.start()
        print('Client is online!')
        print(on_ready_time.strftime("%d/%m/%Y, %H:%M:%S"))

        embed = discord.Embed(
            title='Yeongbot Restart :tools:',
            description=(':warning: Yeong Bot rebooted at\n:clock1: `{}`'.format(
                on_ready_time.strftime("%d/%m/%Y, %H:%M:%S"))
            ),
            color=0xff0033
        )
        await channel.send(embed=embed)

    # * Change status of client
    @tasks.loop(seconds=180, reconnect=True)
    async def change_status(self):
        await client.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name=next(status)))

    # * When client joined the server.
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send('เย้!! น้องหยองเข้ามาเป็นผู้ช่วยของเซิฟคุณแล้ว')
            break


def setup(client):
    client.add_cog(Client(client))
