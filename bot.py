import discord
from discord.ext import commands, tasks
from discord import Spotify

import time
import datetime
from datetime import datetime, timedelta
from itertools import cycle

import pytz
from pytz import timezone

import random
import json
import asyncio
import requests
import os

'''
# ! Load secret/client_secret.json file
with open('secret/client_secret.json') as f:
    client_secret = json.load(f)

# ! Load secret/server_secret.json file
with open('secret/server_secret.json') as f:
    server_secret = json.load(f)

# ! Load secret/line_secret.json file
with open('secret/line_secret.json') as f:
    line_secret = json.load(f)
'''

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
status = cycle(client_playing)
CRIT_RATE = 33
CRIT2X_RATE = 35
CRIT_MULTIPLY_RATE1, CRIT_MULTIPLY_RATE2 = 1, 2

# * lINE Bot Notifications
linebot_url = 'https://notify-api.line.me/api/notify'
linebot_token = os.environ['line_token']
linebot_headers = {
    'content-type': 'application/x-www-form-urlencoded',
    'Authorization': 'Bearer '+linebot_token
}

# * Remove Commands
client.remove_command('help')

# * Author's Informations
AUTHOR_ICON = 'https://i.ibb.co/tMbrntz/jang-wonyoung-nationality-cover2.jpg'

# * Server's Infomations
GUILD_ID = os.environ['GUILD_ID']
CHANNEL_ID = os.environ['CHANNEL_ID']

on_ready_time = datetime.now()
tz_bangkok = timedelta(hours=7)  # Bangkok's Timezone (GMT +7)


# * When bot is online
@client.event
async def on_ready():
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
async def change_status():
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name=next(status)))


# * When users joined the server.
@client.event
async def on_member_join(member):
    guild = client.get_guild(GUILD_ID)
    channel = guild.get_channel(CHANNEL_ID)
    role = discord.utils.get(member.guild.roles, name="Citizen")

    # * datetime Infomations
    current_omj_timezone_time = datetime.now()
    new_omj_timezone_time = current_omj_timezone_time.astimezone(
        timezone('Asia/Bangkok'))

    embed_channel = discord.Embed(
        title="ยินดีต้อนรับ!",
        description=f"อันยองน้อง {member.mention}\n เข้ามาที่ร้านโกโก้ของน้องซันนร้าาา",
        color=0x90ee90
    )
    embed_channel.set_author(
        name="น้องหยอง", icon_url=AUTHOR_ICON
    )
    embed_channel.set_thumbnail(url=member.avatar_url)
    embed_channel.set_footer(
        text=member.name + " เข้ามาในร้านโกโก้ตอน " +
        new_omj_timezone_time.strftime("%d/%m/%Y, %H:%M")
    )

    embed_dm = discord.Embed(
        title="อันยองจ้า!",
        description=(
            f"นี่คือร้านโกโก้ของน้องซันเองจ้าาา\n\
            ถ้าอยากให้น้องหยองช่วยอะไรก็พิมพ์ .help ได้เลยนร้าาาาา"
        ),
        color=0xd9598c
    )
    embed_dm.set_author(
        name="น้องหยอง",
        icon_url=AUTHOR_ICON
    )
    embed_dm.set_footer(
        text="น้องได้เข้ามาในร้านโกโก้ตอน " +
        new_omj_timezone_time.strftime("%d/%m/%Y, %H:%M")
    )

    embed_dm_image = discord.Embed()
    embed_dm_image.set_image(
        url='https://thumbs.gfycat.com/FarflungScaredDartfrog-size_restricted.gif')

    # ! This is important!,
    # ! do not !!forget!! this!,
    # ! Set This before send message.
    await client.wait_until_ready()

    await member.add_roles(role)
    await channel.send(embed=embed_channel)
    await member.send(embed=embed_dm)
    await member.send(embed=embed_dm_image)


# * When users left the server.
@client.event
async def on_member_remove(member):
    # * guild and channel Infomations
    guild = client.get_guild(GUILD_ID)
    channel = guild.get_channel(CHANNEL_ID)

    # * datetime Infomations
    current_omr_timezone_time = datetime.now()
    new_omr_timezone_time = current_omr_timezone_time.astimezone(
        timezone('Asia/Bangkok'))

    embed = discord.Embed(
        title="ลาก่อน...",
        description=f"{member.mention} ออกไปจากร้านโกโก้ของน้องซันแล้ว :crying_cat_face:",
        color=0xff0033
    )
    embed.set_author(
        name="น้องหยอง",
        icon_url=AUTHOR_ICON)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=member.name + " ออกจากเซิฟไปตอน " +
                     new_omr_timezone_time.strftime("%d/%m/%Y, %H:%M"))

    # ! This is important!,
    # ! do not !!forget!! this!,
    # ! Set This before send message.
    await client.wait_until_ready()

    await channel.send(embed=embed)


# * When client joined the server.
@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('เย้!! น้องหยองเข้ามาเป็นผู้ช่วยของเซิฟคุณแล้ว')
        break


# * When users send message (or something).
@client.event
async def on_message(message):
    sender = message.author

    # ? Check is sender = client?
    if sender == client.user:
        return

    # ? When users mention the client.
    if client.user.mentioned_in(message):
        await message.channel.send(
            f"น้อง {sender.display_name} เรียกน้องหยองหรอคะ?\n"
            + "สามารถเรียกน้องหยองได้โดยพิมพ์ .help ในช่องแชทเลย"
        )

    # ? When users mention the guild owner.
    if message.guild:
        if sender.guild.owner.mentioned_in(message):
            if sender.bot:
                return
            else:
                msg = f'{sender.name} has mention you on {message.guild.name}, {message.channel.name}'
                r = requests.post(linebot_url, headers=linebot_headers,
                                  data={'message': msg})
                print('LINE Pinging:', r.text)
                return

    # ? When users type "ควย"
    kuy = ['kuy', 'ควย']
    for kuy in kuy:
        if kuy in message.content.lower():
            await message.channel.send("เป็นเหี้ยอะไรหล่ะ")
            return

    # ? If user type "เหี้ย"
    here = ['เชี่ย', 'เหี้ย', 'here']
    for here in here:
        if here in message.content.lower():
            if sender.bot:
                return
            else:
                here_msg = [
                    'มีปัญหาหรอสัส!',
                    'เป็นควยไรหล่ะ',
                    'อยากมีปัญหาหรอวะ'
                ]
                rd = random.choice(here_msg)

                await message.channel.send(f'{rd}')
                return

    # ? If user type "เงียบ"
    if 'เงียบ' in message.content.lower():
        await message.channel.send(
            f"ก็กูอยากเงียบอ่ะ มีปัญหาหรอวะ แน่จริง 1-1 หลังเซเว่นปิดดิ {sender.mention}"
        )
        return

    # ? If user type "sundick"
    sundick = ['sundick', 'ซันดิ้ก', 'mute me senpai']
    for sundick in sundick:
        if sundick in message.content.lower():
            f'''
                # ! = ALGORITHM EXPLAINED =
                This is a random that user will get mute
                # ? if mute_rate is below {CRIT_RATE} will get muted but:
                        if user get crit_rate below {CRIT2X_RATE}
                            will get critical mute(critical range: 1.0-2.0),
                        else is user got 5 second mute
                    else is 'You are free!'
            '''

            mute_rate = random.randint(1, 100)

            # ! If user random a number that hit mute rate
            if mute_rate <= CRIT_RATE:
                counting = int()
                crit_rate = int(random.randint(1, 100))

                # ? If user random a number that hit critical rate
                if crit_rate <= CRIT2X_RATE:
                    crit_multiply = float('{:.2f}'.format(
                        random.uniform(CRIT_MULTIPLY_RATE1,
                                       CRIT_MULTIPLY_RATE2)
                    ))
                    timer = int(5*crit_multiply)
                    await message.channel.send(
                        f":crossed_swords: `ติดคริติคอล` **{int(100*(crit_multiply-1.00))}%**\n"
                        + f"น้อง {sender.display_name} โดนปิดไมค์ไป `{timer}` วินาที"
                    )
                    pass
                else:
                    timer = int(5)
                    await message.channel.send(
                        f"น้อง {sender.display_name} โดนปิดไมค์ไป `{timer}` วินาที"
                    )
                    pass

                await sender.edit(mute=True, deafen=True)

                for _ in range(timer):
                    counting += 1
                    await asyncio.sleep(1)

                    while counting >= timer:
                        await sender.edit(mute=False, deafen=False)
                        break

            else:
                await message.channel.send(
                    f"น้อง {sender.display_name} โชคดีที่ไม่โดนปิดไมค์ไปนะ "
                    + "แต่ครั้งหน้าก็ระวังไว้ด้วยละกันหล่ะ"
                )
            return
    sleep = ['ง่วง', 'อยากนอน']
    for sleep in sleep:
        if sleep in message.content.lower():
            await message.channel.send('ไปนอนสิ')

            msg = await client.wait_for(
                'message',
                check=lambda channel: message.channel == message.channel
            )

            yes = ['ได้', 'โอเค', 'ด้าย', 'yes']
            for yes in yes:
                if yes in msg.content.lower():
                    await message.channel.send('Good Job!')
                    break

            no = ['ไม่', 'no']
            for no in no:
                if no in msg.content.lower():
                    await message.channel.send('ทำไมไม่ไปนอนหล่ะ บอกให้ไปนอนไง!')
                    break

    await client.process_commands(message)

# * When users uses command (.help)


@client.command()
async def help(ctx, arg=None):
    if arg == None:
        embed = discord.Embed(title="คำสั่งทั้งหมด ขึ้นต้นด้วย .",
                              color=0xd9598c)
        embed.set_author(name="น้องหยอง",
                         icon_url=AUTHOR_ICON)
        embed.add_field(name="help",
                        value=f"แสดงหน้าต่างนี้ไง", inline=True)  # ? (.help)
        embed.add_field(name="whois <member>",
                        value="แสดงข้อมูลเกี่ยวกับคนในเซิฟเวอร์", inline=True)  # ? (.whois)
        embed.add_field(name="spotify / listening <member>",
                        value="แสดงเพลงที่ member \nกำลังเล่นอยู่บน Spotify", inline=True)  # ? (.spotify / .listening)
        embed.add_field(name="call",
                        value="เรียกคนที่ต้องการเรียกหา", inline=True)  # ? (.call)
        embed.add_field(name="clock / time",
                        value="แสดงวันที่และเวลาในปัจจุบัน", inline=True)  # ? (.clock / .time)
        embed.add_field(name="ping",
                        value="ทดสอบการตอบกลับ", inline=True)  # ? (.ping)
        embed.add_field(name="info",
                        value="แสดงรายละเอียดเกี่ยวกับบอท", inline=True)  # ? (.info)
        embed.add_field(name="hello / hi",
                        value="สวัสดีไงเพื่อนรัก", inline=True)  # ? (.hello / .hi)
        embed.add_field(name="send",
                        value="ขอให้บอทส่งอะไรสักอย่าง", inline=True)  # ? (.send <arg>)
        embed.add_field(name="totalusers",
                        value="ดูจำนวนสมาชิกทั้งหมดในเซิฟ", inline=True)  # ? (.totalusers)
        embed.add_field(name="mute / unmute",
                        value="ปิด/เปิดไมค์ทุกคนในห้องแชท (ยกเว้นบอท)", inline=True)  # ? (.mute / .unmute)
        embed.add_field(name="roll",
                        value="สุ่มตัวเลข", inline=True)  # ? (.roll)
        embed.add_field(name="color / colour",
                        value="เปลี่ยนสีของชื่อตัวเอง", inline=True)  # ? (.color / .colour)

        await ctx.send(embed=embed)

    elif arg == 'mute':
        await ctx.send('คำสั่งคือ .mute จะเป็นการปิดไมค์ทั้งห้อง')

    elif arg == 'unmute':
        await ctx.send(
            'คำสั่งคือ `.unmute` จะเป็นการเปิดไมค์ทั้งห้อง\n'
            + 'คำสั่ง `.unmute me` จะเป็นการเปิดไมค์ของตัวเอง (ในกรณีโดน Server Mute อยู่)')


# * When users uses command (.info)
@client.command()
async def info(ctx):
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
        value=f'`{round(client.latency * 1000)}` ms')

    await ctx.send(embed=embed)


# * When users uses command (.whois)
@client.command()
async def whois(ctx, member: discord.Member):
    embed = discord.Embed(
        title=f"น้อง {member.name}",
        color=0xd9598c
    )
    embed.set_author(name="น้องหยอง", icon_url=AUTHOR_ICON)
    embed.add_field(name="ชื่อ", value=member.name, inline=True)
    embed.add_field(
        name="ชื่อที่แสดง",
        value=member.display_name, inline=True
    )
    embed.add_field(
        name="วันที่สมัครไอดี",
        value='{}'.format(
            member.created_at.strftime("%d/%m/%Y")),
        inline=False
    )
    embed.add_field(
        name="วันที่เข้ามาในร้าน",
        value='{}'.format(
            member.joined_at.strftime("%d/%m/%Y")),
        inline=False
    )
    embed.add_field(name="ไอดี", value=member.id, inline=False)
    embed.set_footer(
        icon_url=ctx.author.avatar_url,
        text="ขอดูประวัติโดย {}".format(ctx.author.name)
    )
    embed.timestamp = datetime.utcnow()
    embed.set_thumbnail(url=member.avatar_url)

    await ctx.send(embed=embed)


# * When users uses command (.spotify / .listening)
@client.command(aliases=['listening'])
async def spotify(ctx, user: discord.Member = None):
    # ? If users did not put <username> argument,
    # ? user will be sender (ctx.author)
    if user == None:
        user = ctx.author
        pass

    if user.activities:
        for activity in user.activities:
            if isinstance(activity, Spotify):
                raw_current_length = activity.end \
                    - (datetime.now() - tz_bangkok)
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


# * When user use command (.call)
# TODO: User can multiple call in one command
@client.command()
async def call(ctx, user: discord.Member = None):
    if user == None:  # ? user = None (.call)
        await ctx.send("ถ้าต้องการเรียกใครมาตอบให้พิม .call <username> นะคะ")

    elif ctx.author != user:  # ? user != sender
        call_msg = [
            f"**{ctx.author.mention}** เรียกคุณที่ `{ctx.guild.name}`, "
            + f"{ctx.channel.mention} ค่ะ โปรดมาตอบกลับด้วย",
            f"ฮัลโหล... อยู่รึปล่าว, มีคนเรียกแกอ่ะ ลองมาดูที่ {ctx.channel.mention} ดูดิ"
        ]
        call_rd = random.choice(call_msg)

        await user.send(call_msg)

    else:  # ? user = sender
        embed = discord.Embed()
        embed.set_image(
            url='https://media1.tenor.com/images/75eb5955851b1daebd1af193e2d76019/tenor.gif?itemid=12319210'
        )

        await ctx.send(f"คุณไม่สามารถเรียกตัวเองได้นะคะ")
        await ctx.send(embed=embed)


# * When users uses command (.ping)
@client.command()
async def ping(ctx):
    message = await ctx.send('*Pinging...*')

    await message.edit(
        content=f":ping_pong: {round(client.latency * 1000)}ms"
    )


# * When users uses command (.hello)
@client.command(aliases=['hi'])
async def hello(ctx):
    with open('assets/hello_msg.json', encoding='utf-8') as f:
        hello_msg = json.load(f)

    await ctx.send(f"> {random.choice(hello_msg)} {ctx.author.mention}")


# * When users use command (.clock)
@client.command(aliases=['time'])
async def clock(ctx):
    # * datetime Infomations
    clock_current_timezone_time = datetime.now()
    new_clock_timezone_time = clock_current_timezone_time.astimezone(
        timezone('Asia/Bangkok'))

    embed = discord.Embed(
        title="ตอนนี้เป็นเวลา",
        description=":calendar_spiral: {}\n:alarm_clock: {}".format(
            new_clock_timezone_time.strftime("%d/%m/%Y"),
            new_clock_timezone_time.strftime("%H:%M:%S")),
        color=0xff7326)

    await ctx.send(embed=embed)


# * When users use command (.send)
@client.command()
async def send(ctx, arg1=None):
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


# * When users use command (.list)
@client.command()
async def totalusers(ctx):
    guild = client.get_guild(ctx.author.guild.id)

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
# ! [need "ว่าที่โปรแกรมเมอร์" role]
@client.command(aliases=['join'])
async def connect(ctx, password_input=None):
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


# * When users use command (.mute)
@client.command()
async def mute(ctx):
    channel = ctx.author.voice.channel

    for user in channel.members:
        if user.bot:
            await user.edit(mute=False)
        else:
            await user.edit(mute=True)

    await ctx.send(f'{ctx.author.name} ได้ทำการปิดไมค์ทุกคนในห้องแล้ว')


# * When users use command (.unmute)
@client.command()
async def unmute(ctx, onoff=None):
    channel = ctx.author.voice.channel
    if onoff is None:
        for member in channel.members:
            await member.edit(mute=False)
        await ctx.send(f'{ctx.author.name} ได้ทำการเปิดไมค์ทุกคนในห้องแล้ว')

    elif onoff == 'me':
        await ctx.author.edit(mute=False)


# * When users use command (.roll)
@client.command()
async def roll(ctx, num1: int = None, num2: int = None):
    if num1 is None:
        randnum = random.randint(1, 10)
        await ctx.send(f':roller_coaster: {ctx.author.name} สุ่มได้ {randnum} แต้ม (1-10)')

    elif num1 is not None and num2 is None:
        randnum = random.randint(1, num1)
        await ctx.send(f':roller_coaster: {ctx.author.name} สุ่มได้ {randnum} แต้ม (1-{num1})')

    elif num1 is not None and num2 is not None:
        randnum = random.randint(num1, num2)
        await ctx.send(f':roller_coaster: {ctx.author.name} สุ่มได้ {randnum} แต้ม ({num1}-{num2})')


# * When users use command (.role)
@client.command(aliases=['colour'])
async def color(ctx, *, color=None):
    if color is None:
        embed = discord.Embed(
            title='Colors',
            description=(
                '[pink](https://www.color-hex.com/color/d9598c "#D9598c")\n'  # Pink
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


# * When users use command (.clear)
@client.command()
async def clear(ctx, number: int = None):
    if ctx.author is ctx.guild.owner:
        if number is None:
            number = 25+3

            await ctx.send('Are you sure to delete 25 messages? (Y/N)')

            msg = await client.wait_for(
                'message',
                check=lambda message: message.content.lower() == 'y' and ctx.channel == message.channel
                )
            await ctx.channel.purge(limit=number)
        else:
            number += 3

            await ctx.send(f'Are you sure to delete {number-3} message? (Y/N)')

            msg = await client.wait_for(
                'message',
                check=lambda message: message.content.lower(
                ) == 'y' and message.channel == ctx.channel
            )
            await ctx.channel.purge(limit=number)
    else:
        await ctx.send('You need to be a server owner to use this command!')


# * When users use command (.play)
@client.command()
async def play(ctx, args=None):
    if args is None:
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
                    await ctx.send(f'ตัวเลขที่นายเดามาหน่ะ มันสูงไปนะ, นายยังสามารถเดาได้อีก `{tries}` ครั้ง')
                    continue

            elif int(num.content) < random_number:
                tries -= 1
                if tries == 0:
                    await ctx.send('นายไม่มีสิทธิเดาแล้ว เสียใจด้วย')
                    break
                else:
                    await ctx.send(f'ตัวเลขที่นายเดามาหน่ะ มันต่ำไปนะ, นายยังสามารถเดาได้อีก `{tries}` ครั้ง')
                    continue

            elif int(num.content) is random_number:
                await ctx.send('ดีมาก! นายเดาตัวเลขถูกแล้ว!')
                break

        if tries == 0:
            await ctx.send(f'ตัวเลขคือ {random_number}')


# ! Run / Required Token to run
client.run(TOKEN)
