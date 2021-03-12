import discord
from discord.ext import commands
from discord import Spotify
from datetime import datetime, timedelta

import random
import json

tz_bangkok = timedelta(hours=7)  # Bangkok's Timezone (GMT +7)

class Fun(commands.Cog):
    def __init__(self, client):
        client = self.client

    # * When users use command (.guessnumber)
    @commands.command()
    async def guessnumber(self, ctx):
        random_number = random.randint(1, 20)
        tries = 5

        await ctx.send('Guessing Number from 1 to 10')

        while tries != 0:
            num = await client.wait_for(
                'message',
                check=lambda message: message.author is ctx.author
            )
            if int(num.content) > random_number:
                tries -= 1
                if tries == 0:
                    await ctx.send('นายไม่มีสิทธิเดาแล้ว เสียใจด้วย')
                    break
                else:
                    await ctx.send(f'ตัวเลขที่แกเดามาอ่ะ มันสูงไปนะ, แกยังสามารถเดาได้อีก `{tries}` ครั้ง')
                    continue

            elif int(num.content) < random_number:
                tries -= 1
                if tries == 0:
                    await ctx.send('นายไม่มีสิทธิเดาแล้ว เสียใจด้วย')
                    break
                else:
                    await ctx.send(f'ตัวเลขที่แกเดามาอ่ะ มันต่ำไปนะ, แกยังสามารถเดาได้อีก `{tries}` ครั้ง')
                    continue

            elif int(num.content) is random_number:
                await ctx.send('ดีมาก! แกเดาตัวเลขถูกแล้ว!')
                break

        if tries == 0:
            await ctx.send(f'ตัวเลขคือ {random_number}')

    # * When users use command (.roll)
    @commands.command()
    async def roll(self, ctx, num1: int = None, num2: int = None):
        if num1 is None:
            randnum = random.randint(1, 10)
            await ctx.send(f':roller_coaster: {ctx.author.name} สุ่มได้ {randnum} แต้ม (1-10)')

        elif num1 is not None and num2 is None:
            randnum = random.randint(1, num1)
            await ctx.send(f':roller_coaster: {ctx.author.name} สุ่มได้ {randnum} แต้ม (1-{num1})')

        elif num1 is not None and num2 is not None:
            randnum = random.randint(num1, num2)
            await ctx.send(f':roller_coaster: {ctx.author.name} สุ่มได้ {randnum} แต้ม ({num1}-{num2})')

    # * When users uses command (.ping)
    @commands.command()
    async def ping(self, ctx):
        message = await ctx.send('*Pinging...*')

        await message.edit(
            content=f":ping_pong: {round(client.latency * 1000)}ms"
        )

    # * When users uses command (.hello)
    @commands.command(aliases=['hi'])
    async def hello(self, ctx):
        with open('assets/hello_msg.json', encoding='utf-8') as f:
            hello_msg = json.load(f)

        await ctx.send(f"> {random.choice(hello_msg)} {ctx.author.mention}")

    # * When users uses command (.spotify / .listening)
    @commands.command(aliases=['listening'])
    async def spotify(self, ctx, user: discord.Member = None):
        # ? If users did not put <username> argument,
        # ? user will be sender (ctx.author)
        if user == None:
            user = ctx.author
            pass

        if user.activities:
            for activity in user.activities:
                if isinstance(activity, Spotify):
                    raw_current_length = activity.end - datetime.now()
                    current_length = activity.duration - raw_current_length
                    created_at = activity.created_at + tz_bangkok

                    spotify_icon = 'https://i.pinimg.com/originals/83/3c/f5/833cf5fe43f8c92c1fcb85a68b29e585.png'

                    """
                    divmod use for situation 'datetime.timedelta' has no attribute 'strftime'
                    calculate or convert time like from seconds to minutes
                    """
                    m1, s1 = divmod(int(activity.duration.seconds), 60)
                    m2, s2 = divmod(int(current_length.seconds), 60)

                    # ? if second(s1) is odd number (0-9)
                    if s1 < 10:
                        song_length = f'{m1}:0{s1}'
                        pass
                    else:
                        song_length = f'{m1}:{s1}'
                        pass

                    # ? if second(s2) is odd number (0-9)
                    if s2 < 10:
                        current_length = f'{m2}:0{s2}'
                        pass
                    else:
                        current_length = f'{m2}:{s2}'
                        pass

                    embed = discord.Embed(
                        title=f"น้อง {user.display_name} กำลังฟังเพลงอะไรอยู่กันนะ? :thinking:",
                        description=":musical_note: **น้อง `{}` กำลังฟัง {}**".format(
                            user.display_name,
                            f"[{activity.title}](https://open.spotify.com/track/{activity.track_id})"
                        ),
                        color=activity.color
                    )
                    embed.set_author(name="Spotfiy", icon_url=spotify_icon)
                    embed.set_thumbnail(url=activity.album_cover_url)
                    embed.add_field(name="ชื่อเพลง", value=activity.title)
                    embed.add_field(name="ศิลปิน", value=activity.artist)
                    embed.add_field(
                        name="อัลบั้ม", value=activity.album, inline=False
                    )
                    embed.add_field(
                        name="ระยะเวลา", value=f"{current_length}/{song_length}",
                        inline=True
                    )
                    embed.set_footer(
                        icon_url=user.avatar_url,
                        text=(
                            "{} เริ่มฟังเพลงตอน {} น.".format(
                                user.name,
                                created_at.strftime("%H:%M")
                            )
                        )
                    )

                    await ctx.send(embed=embed)
        else:
            await ctx.send(f'ดูเหมือนว่า {user.name} จะไม่ได้ทำอะไรอยู่นะ')

    # * When users use command (.send)
    @commands.command()
    async def send(self, ctx, arg1=None):
        # ? if arg1 is None (.send)
        if arg1 == None:
            embed = discord.Embed(title="คำสั่งหมวด send <arg>")
            embed.add_field(name="hug", value="ต้องการกอดหรอ?")
            embed.add_field(name="izone", value="IZ*ONE น้องหยองชอบมักๆ")
            embed.add_field(name="nude", value="ต้องการรูปสินะ... 555555")
            embed.add_field(name="quote", value="อยากได้คำคมหรอ?")
            embed.add_field(name="malee", value="แตกหนึ่ง! สวยพี่สวย!")

            await ctx.send(embed=embed)

        # ? If arg1 != None (.send <arg>)
        else:
            embed = discord.Embed()

            # ? If arg1 is hug (.send hug)
            if arg1 == 'hug':
                # * Import assets/hug.json file
                with open('assets/hug.json') as f:
                    hug = json.load(f)

                hug_rd = random.choice(hug)

                embed.set_image(url=hug_rd)

            # ? If arg is izone (.send izone)
            elif arg1 == 'izone':
                # * Import assets/izone.json file
                with open('assets/izone.json') as f:
                    izone = json.load(f)

                izone_rd = random.choice(izone)

                embed.set_image(url=izone_rd)

            # ? If arg is nude (.send nude)
            elif arg1 == 'nude':
                embed.set_image(
                    url='https://i.makeagif.com/media/2-10-2021/g_z7xe.gif')

            # ? If arg is malee (.send malee)
            elif arg1 == 'malee':
                # * Import assets/malee.json file
                with open('assets/malee.json') as f:
                    malee = json.load(f)

                malee_rd = random.choice(malee)

                embed.set_image(url=malee_rd)

            # ? If arg is quote (.send quote)
            elif arg1 == 'quote':
                # * Import assets/quote.json file
                with open('assets/quote.json', encoding='utf-8') as f:
                    quote = json.load(f)

                quote_rd = random.choice(quote)

                await ctx.send(f'> *{quote_rd}*')
                return

            # ? If arg is video (.send video)
            elif arg1 == 'video':
                # * Import assets/video.json file
                with open('assets/video.json') as f:
                    video = json.load(f)

                video_rd = random.choice(video)

                await ctx.send(video_rd)
                return

            # ? If arg is None of the above
            # ! Example (.send quoter)
            else:
                await ctx.send("พิมพ์ผิดป้ะเนี่ย! พิมพ์ให้ถูกหน่อยดิวะ")
                return

            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fun(client))
