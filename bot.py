import discord
from discord.ext import commands, tasks
from discord import Spotify

import time
import datetime
from datetime import datetime

import pytz
from pytz import timezone

import random
import json
from itertools import cycle

# ! Load data/bot_token.json file
with open('data/client_token.json') as token:
    token = json.load(token)

# * Import data/hug.json file
with open('data/hug.json') as hug:
    hug = json.load(hug)

# * Import data/izone.json file
with open('data/izone.json') as izone:
    izone = json.load(izone)

# * Import data/malee.json file
with open('data/malee.json') as malee:
    malee = json.load(malee)

# * Import data/client_playing.json file
with open('data/client_playing.json') as client_playing:
    client_playing = json.load(client_playing)

# * Intents Settings
intents = discord.Intents.all()

# * Bot's Infomations
TOKEN = token['token']
client = commands.Bot(command_prefix='.', intents=intents,
                      case_insensitive=True)
status = cycle(client_playing)

# * Remove Commands
client.remove_command('help')

# * Author's Informations
author_icon = 'https://i.ibb.co/tMbrntz/jang-wonyoung-nationality-cover2.jpg'

# * Server's Infomations
GUILD_ID = 545170933254717450
CHANNEL_ID = 562590723875143680


# * When bot is online
@client.event
async def on_ready():
    change_status.start()
    print("Bot is online!")


# * Change status of client
@tasks.loop(seconds=180)
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
        color=0x90ee90)
    embed_channel.set_author(
        name="น้องหยอง", icon_url=author_icon)
    embed_channel.set_thumbnail(url=member.avatar_url)
    embed_channel.set_footer(
        text=member.name + " เข้ามาในร้านโกโก้ตอน " + new_omj_timezone_time.strftime("%d/%m/%Y, %H:%M"))

    embed_dm = discord.Embed(
        title="อันยองจ้า!",
        description=(f"นี่คือร้านโกโก้ของน้องซันเองจ้าาา\n"
                     f"ถ้าอยากให้น้องหยองช่วยอะไรก็พิมพ์ .help ได้เลยนร้าาาาา"),
        color=0xd9598c)
    embed_dm.set_author(
        name="น้องหยอง",
        icon_url=author_icon)
    embed_dm.set_footer(text="น้องได้เข้ามาในร้านโกโก้ตอน " +
                        new_omj_timezone_time.strftime("%d/%m/%Y, %H:%M"))

    embed_dm_image = discord.Embed()
    embed_dm_image.set_image(
        url='https://thumbs.gfycat.com/FarflungScaredDartfrog-size_restricted.gif')

    # This is important!,
    # do not !!forget!! this!,
    # Set This before send message.
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
        color=0xff0033)
    embed.set_author(
        name="น้องหยอง",
        icon_url=author_icon)
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_footer(text=member.name + " ออกจากเซิฟไปตอน " +
                     new_omr_timezone_time.strftime("%d/%m/%Y, %H:%M"))

    # This is important!,
    # do not !!forget!! this!,
    # Set This before send message.
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
    text = message.content.lower().startswith

    # ? Check is sender = client?
    if sender == client.user:
        return

    # ? When users mention the client.
    if client.user.mentioned_in(message):
        await message.channel.send(f"น้อง {sender.display_name} เรียกน้องหยองหรอคะ?\n"
                                   + "สามารถเรียกน้องหยองได้โดยพิมพ์ .help ในช่องแชทเลย")

    # ? When users type "ควย"
    if text('ควย'):
        await message.channel.send("เป็นเหี้ยอะไรหล่ะ")

    # ? If user type "เหี้ย"
    if text("เหี้ย"):
        await message.channel.send(f"เหี้ย")

    # ? If user type "sundick"
    if text('sundick'):
        rd = random.randint(1, 3)

        if rd < 3:
            counting = int()
            crit_rd = random.randint(1, 4)

            await sender.edit(mute=True, deafen=True)

            if crit_rd == 1:
                timer = int(12)
                pass
            else:
                timer = int(6)
                pass

            if timer == 6:
                await message.channel.send(f"น้อง {sender.display_name} โดนปิดไมค์ไป `{timer}` วินาที")
            else:
                await message.channel.send(f":crossed_swords: `ติดคริติคอล` **200%**\n"
                                           + f"น้อง {sender.display_name} โดนปิดไมค์ไป `{timer}` วินาที")

            for countdown in range(timer):
                counting += countdown
                time.sleep(1)

                while counting >= timer:
                    await sender.edit(mute=False, deafen=False)
                    break

        elif rd == 3:
            await message.channel.send(f"น้อง {sender.mention} โชคดีที่ไม่โดนปิดไมค์ไปนะ แต่ครั้งหน้าก็ระวังไว้ด้วยละกันหล่ะ")

    await client.process_commands(message)


# * When users uses command (.help)
@client.command()
async def help(ctx):
    embed = discord.Embed(title="คำสั่งทั้งหมด ขึ้นต้นด้วย .",
                          color=0xd9598c)
    embed.set_author(name="น้องหยอง",
                     icon_url=author_icon)
    embed.add_field(name="help",
                    value=f"แสดงหน้าต่างนี้ไง", inline=True)  # ? (.help)
    embed.add_field(name="userinfo / user <member>",
                    value="แสดงข้อมูลเกี่ยวกับคนในเซิฟเวอร์", inline=True)  # ? (.userinfo / .user)
    embed.add_field(name="spotify / listening <member>",
                    value="แสดงเพลงที่ member \nกำลังเล่นอยู่บน Spotify", inline=True)  # ? (.spotify / .listening)
    embed.add_field(name="call",
                    value="เรียกคนที่ต้องการเรียกหา", inline=True)  # ? (.call)
    embed.add_field(name="clock / time",
                    value="แสดงวันที่และเวลาในปัจจุบัน", inline=True)  # ? (.clock / .time)
    embed.add_field(name="botinfo",
                    value="แสดงรายละเอียดของบอท", inline=True)  # ? (.botinfo)
    embed.add_field(name="ping",
                    value="ทดสอบการตอบกลับ", inline=True)  # ? (.ping)
    embed.add_field(name="hello / hi",
                    value="สวัสดีไงเพื่อนรัก", inline=True)  # ? (.hello / .hi)
    embed.add_field(name="send",
                    value="ขอให้บอทส่งอะไรสักอย่าง", inline=True)  # ? (.send <arg>)

    await ctx.author.send(embed=embed)


# * When users uses command (.userinfo / .user)
@client.command(aliases=['user'])
async def userinfo(ctx, member: discord.Member):

    embed = discord.Embed(title=f"น้อง {member.name}",
                          color=0xd9598c)
    embed.set_author(name="น้องหยอง",
                     icon_url=author_icon)
    embed.add_field(name="ชื่อ", value=member.name, inline=True)
    embed.add_field(name="ชื่อที่แสดง",
                    value=member.display_name, inline=True)
    embed.add_field(name="วันที่เข้ามาในร้าน",
                    value='{}'.format(
                         member.joined_at.strftime("%d/%m/%Y")),
                    inline=False)
    embed.add_field(name="ไอดี", value=member.id, inline=False)
    embed.set_thumbnail(url=member.avatar_url)

    await ctx.send(embed=embed)


# * When users uses command (.spotify / .lsitening)
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
                created_at_new_timezone_time = activity.created_at.astimezone(
                    timezone('Asia/Bangkok'))

                m1, s1 = divmod(int(activity.duration.seconds), 60)

                # ? if second is odd number (0-9)
                if s1 < 10:
                    song_length = f'{m1}:0{s1}'
                    pass
                else:
                    song_length = f'{m1}:{s1}'
                    pass

                ''' # ! Not used but will use soon, If possible!
                m2, s2 = divmod(int(activity.duration.seconds), 60)
                if s1 < 10:
                    current_length = f'{m1}:0{s1}'
                    pass
                else:
                    current_length = f'{m1}:{s1}'
                    pass
                '''

                embed = discord.Embed(
                    title=f"น้อง {user.display_name} กำลังฟังเพลงอะไรอยู่กันนะ? :thinking:",
                    description=":musical_note: **น้อง `{}` กำลังฟัง {}**".format(
                        user.display_name,
                        f"[{activity.title}](https://open.spotify.com/track/{activity.track_id})"),
                    color=activity.color)
                embed.set_thumbnail(url=activity.album_cover_url)
                embed.add_field(name="ชื่อเพลง", value=activity.title)
                embed.add_field(name="ศิลปิน", value=activity.artist)
                embed.add_field(
                    name="อัลบั้ม", value=activity.album, inline=False)
                embed.add_field(name="ระยะเวลา",
                                value=f"{song_length}", inline=True)
                # ////embed.add_field(name="ระยะเวลา",
                # ////value=f"{current_length}/{song_length}", inline=True)
                embed.set_author(name="น้องหยอง",
                                 icon_url=author_icon)
                embed.set_footer(
                    text=("{} เริ่มฟังตอน {} UTC".format(user.name, created_at_new_timezone_time.strftime("%H:%M"))))

                await ctx.send(embed=embed)


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

    else:  # user = sender
        embed = discord.Embed()
        embed.set_image(
            url='https://media1.tenor.com/images/75eb5955851b1daebd1af193e2d76019/tenor.gif?itemid=12319210')

        await ctx.send(f"คุณไม่สามารถเรียกตัวเองได้นะคะ")
        await ctx.send(embed=embed)


# * When users uses command (.ping)
@client.command()
async def ping(ctx):
    await ctx.send(f":ping_pong: {round(client.latency * 1000)}ms")


# * When users uses command (.hello)
@client.command(aliases=['hi'])
async def hello(ctx):
    hello_msg = [
        f'สวัสดีจ้า {ctx.author.mention}',
        f'สวัสดี, {ctx.author.mention}',
        f'Hello {ctx.author.mention}',
        f'Hello, World',
        f'你好！{ctx.author.mention}'
    ]
    await ctx.send(f"> {random.choice(hello_msg)}")


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


# * When users use command (.botinfo)
@client.command()
async def botinfo(ctx):
    creator_url = 'https://cdn.discordapp.com/avatars/254515724804947969/e22d5539f86680742088a7996f44c9ea.webp?size=1024'

    embed = discord.Embed(
        title="รายละเอียดของน้องหยอง",
        color=0xd9598c)
    embed.set_author(name="น้องหยอง",
                     icon_url=author_icon)
    embed.add_field(name="คนสร้างน้องหยอง", value="Sun#6284", inline=False)
    embed.add_field(name="สร้างไว้ทำอะไร ?",
                    value="ก็กูอยากสร้างอ่ะมีปัญหาอะไรไหม", inline=False)
    embed.set_image(
        url='https://thumbs.gfycat.com/PitifulSkinnyEuropeanpolecat-size_restricted.gif')
    embed.set_thumbnail(url=creator_url)

    await ctx.send(embed=embed)


# * When users use command (.send)
@client.command()
async def send(ctx, arg=None):

    if arg == None:
        embed_arg_none = discord.Embed(title="คำสั่งหมวด send <arg>")
        embed_arg_none.add_field(name="hug", value="ต้องการกอดหรอ?")
        embed_arg_none.add_field(name="izone", value="IZ*ONE น้องหยองชอบมักๆ")
        embed_arg_none.add_field(name="nude", value="ต้องการรูปสินะ... 555555")
        embed_arg_none.add_field(name="quote", value="อยากได้คำคมหรอ?")
        embed_arg_none.add_field(name="malee", value="แตกหนึ่ง! สวยพี่สวย!")

        await ctx.send(embed=embed_arg_none)

    else:
        embed = discord.Embed()

        # ? If arg is hug (.send hug)
        if arg == 'hug':
            hug_rd = random.choice(hug)
            embed.set_image(url=hug_rd)

        # ? If arg is izone (.send izone)
        if arg == 'izone':
            izone_rd = random.choice(izone)
            embed.set_image(url=izone_rd)

        # ? If arg is nudes (.send nude)
        if arg == 'nude':
            embed.set_image(
                url='https://i.makeagif.com/media/2-10-2021/g_z7xe.gif')

        if arg == 'malee':
            malee_rd = random.choice(malee)
            embed.set_image(
                url=malee_rd)

        # ? If arg is quote (.send quote)
        if arg == 'quote':
            quote = [
                "เห็นแดดแล้วตาหยี",
                "คำคมบาดใจ"
            ]
            quote_rd = random.choice(quote)

            await ctx.send(f'> ***{quote_rd}***')
            return

        await ctx.send(embed=embed)


# ! Run / Required Token to run
client.run(TOKEN)
