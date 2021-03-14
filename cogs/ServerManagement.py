import discord
from discord.ext import commands
import asyncio
import os

PASSWORD = os.environ['admin_password']

class ServerManagement(commands.Cog):
    def __init__(self, client):
        self.client = client

    # * When users use command (.clear)
    @commands.command()
    async def clear(self, ctx, number: int = None):
        if ctx.author is ctx.guild.owner:
            if number is None:
                number = 25+3

                await ctx.send('Are you sure to delete 25 messages? (Y/N)')

                msg = await self.client.wait_for(
                    'message',
                    check=lambda message: message.content.lower(
                    ) == 'y' and ctx.channel == message.channel
                )
                await ctx.channel.purge(limit=number)
            else:
                number += 3

                await ctx.send(f'Are you sure to delete {number-3} message? (Y/N)')

                msg = await self.client.wait_for(
                    'message',
                    check=lambda message: message.content.lower(
                    ) == 'y' and message.channel == ctx.channel
                )
                await ctx.channel.purge(limit=number)
        else:
            await ctx.send('You need to be a server owner to use this command!')

    # * When users use command (.role)
    @commands.command(aliases=['colour'])
    async def color(self, ctx, *, color=None):
        if color is None:
            embed = discord.Embed(
                title='Colors',
                description=(
                    # Pink
                    '[pink](https://www.color-hex.com/color/d9598c "#D9598c")\n'
                    # Light Pink
                    + '[light pink](https://www.color-hex.com/color/f1d2e7 "#F1D2E7")\n'
                    # Orange
                    + '[orange](https://www.color-hex.com/color/f3aa51 "#F3AA51")\n'
                    # Yellow
                    + '[yellow](https://www.color-hex.com/color/fcf695 "#FCF695")\n'
                    # Blue
                    + '[blue](https://www.color-hex.com/color/567ace "#567ACE")\n'
                    # Light Blue
                    + '[light blue](https://www.color-hex.com/color/b7d3e9 "#B7D3E9")\n'
                    # Purple
                    + '[purple](https://www.color-hex.com/color/bbb0dc "#BBB0DC")\n'
                    # Red
                    + '[red](https://www.color-hex.com/color/d9726b "#D9726B")\n'
                    # Peach
                    + '[peach](https://www.color-hex.com/color/f1c3aa "#F1C3AA")\n'
                    # Mint
                    + '[mint](https://www.color-hex.com/color/cee5d5 "#CEE5D5")\n'
                    # White
                    + '[white](https://www.color-hex.com/color/ffffff "#FFFFFF")\n'
                    # Blue Mint
                    + '[blue mint](https://www.color-hex.com/color/a7e0e1 "#A7E0E1")\n'
                    # Black
                    + '[black](https://www.color-hex.com/color/010101 "#010101")\n'
                ),
                color=0xd9598c
            )

            await ctx.send(embed=embed)

        else:
            user = ctx.author
            role = discord.utils.get(user.guild.roles, name=color)

            if role in user.roles:
                await user.remove_roles(role)
                await ctx.send(
                    f'น้องหยองได้เอาสี {role.name} ออกให้แล้วนะคะ :smiling_face_with_3_hearts:'
                )
                await asyncio.sleep(2)
                await ctx.channel.purge(limit=2)

            else:
                await user.add_roles(role)
                await ctx.send(
                    f'น้องหยองได้เพิ่มสี {role.name} ให้แล้วนะคะ :smiling_face_with_3_hearts:'
                )
                await asyncio.sleep(2)
                await ctx.channel.purge(limit=2)
    
    # * When users use command (.mute)
    @commands.command()
    async def mute(self, ctx):
        channel = ctx.author.voice.channel

        for user in channel.members:
            if user.bot:
                await user.edit(mute=False)
            else:
                await user.edit(mute=True)

        await ctx.send(f'{ctx.author.name} ได้ทำการปิดไมค์ทุกคนในห้องแล้ว')


    # * When users use command (.unmute)
    @commands.command()
    async def unmute(self, ctx, onoff=None):
        channel = ctx.author.voice.channel
        
        if onoff is None:
            for member in channel.members:
                await member.edit(mute=False)
            await ctx.send(f'{ctx.author.name} ได้ทำการเปิดไมค์ทุกคนในห้องแล้ว')

        elif onoff == 'me':
            await ctx.author.edit(mute=False)

    # * When users use command (.totalusers)
    @commands.command()
    async def totalusers(self, ctx):
        guild = self.client.get_guild(ctx.author.guild.id)

        total = len(guild.members)
        bot_total = 0
        user_total = 0

        for user in guild.members:
            if user.bot:
                bot_total += 1
            else:
                user_total += 1

        embed = discord.Embed(
            title=f'{guild.name} Total Members',
            color=0x90ee90
        )
        embed.add_field(name='Total', value=f'`{total}`')
        embed.add_field(name='Users :bearded_person:', value=f'`{user_total}`')
        embed.add_field(name='Bots :robot:', value=f'`{bot_total}`')

        await ctx.send(embed=embed)
    
    # * When users use command (.connect <password>)
    # ! [need server owner to use this command]
    @commands.command(aliases=['join'])
    async def connect(self, ctx, password_input=None):
        message = ctx.message
        password = PASSWORD

        if ctx.author is not ctx.author.guild.owner:
            return
        else:
            if password_input is password:
                channel = ctx.author.voice.channel
                await channel.connect()
                await message.delete_message()
            else:
                print(f'{ctx.author.name} type wrong password (.connect)')
                await ctx.author.delete_message(message)


def setup(client):
    client.add_cog(ServerManagement(client))
