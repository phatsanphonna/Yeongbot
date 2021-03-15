import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import json
import os

# * Import assets/client_playing.json file
with open('assets/client_playing.json') as f:
    client_playing = json.load(f)

tz_bangkok = timedelta(hours=7)  # Bangkok's Timezone (GMT +7)
on_ready_time = datetime.now()

GUILD_ID = int(os.environ['GUILD_ID'])
CHANNEL_ID = int(os.environ['CHANNEL_ID'])

CRIT_RATE = 33
CRIT2X_RATE = 35


class Client(commands.Cog):
    def __init__(self, client):
        self.client = client

    # * When client is online!
    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.client.get_guild(GUILD_ID)
        channel = guild.get_channel(CHANNEL_ID)

        print('Client is online!')
        print(on_ready_time.strftime("%d/%m/%Y, %H:%M:%S"))

        embed = discord.Embed(
            title='Yeongbot Restart :tools:',
            description=(':warning: Yeong Bot rebooted at\n:clock1: `{}`'.format(
                on_ready_time.strftime("%d/%m/%Y, %H:%M:%S"))
            ),
            color=0xff0033
        )
        await self.client.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name='.help'
            )
        )
        await channel.send(embed=embed)

    # * When client joined the server.
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        for channel in guild.text_channels:
            if channel.permissions_for(guild.me).send_messages:
                await channel.send('เย้!! น้องหยองเข้ามาเป็นผู้ช่วยของเซิฟคุณแล้ว')
            break

    # * When users uses command (.info)
    @commands.command()
    async def info(self, ctx):
        total_restart_time = datetime.now() - on_ready_time

        m, s = divmod(int(total_restart_time.seconds), 60)
        h, m = divmod(m, 60)

        if total_restart_time.days > 0:
            d = total_restart_time.days
        else:
            d = 0

        embed = discord.Embed(
            title='รายละเอียดของบอท',
            color=0xFCF694
        )
        embed.add_field(
            name='Last Restart',
            value=f'Date: `{on_ready_time.strftime("%d/%m/%Y / %d %B %Y")}`\n\
            Time: `{on_ready_time.strftime("%H:%M:%S")} GMT +7`\n\
            > `{int(d)} Days, {int(h)} Hours, {int(m)} Minutes, {int(s)} Seconds`',
            inline=False
        )
        embed.add_field(
            name='Bot Critical Rate',
            value=f'Critical Rate: `{CRIT_RATE}`%\n\
            Critical Multiplier Rate: `{CRIT2X_RATE}`%'
        )
        embed.add_field(
            name='Ping Time',
            value=f'`{round(self.client.latency * 1000)}` ms')

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Client(client))
