import discord
from discord.ext import commands
from discord import Spotify

import time

import datetime
from datetime import datetime

import pytz
from pytz import timezone

import random
import logging
import json

# * Open bot_token.json file
with open('data/bot_token.json') as token:
    token = json.load(token)

# * Intents Settings
intents = discord.Intents.all()

# * Bot's Infomations
TOKEN = token['token']
client = commands.Bot(command_prefix='.', intents=intents,
                      case_insensitive=True)

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
    await client.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(
            type=discord.ActivityType.listening,
            name="D-D-DANCE"))
    print("Bot is online!")


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

    # This is important!, do not !!forget!! this!, Set This before send message.
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

    # This is important!, do not !!forget!! this!, Set This before send message.
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
    if text("sundick"):
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
                    value="ขอให้บอทส่งรูป", inline=True)  # ? (.send <arg>)

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
        call_rd = random.randint(1, 5)

        for call in range(call_rd):
            await user.send(f"**{ctx.author.mention}** เรียกคุณที่ {ctx.guild.name}, {ctx.channel.mention} ค่ะ โปรดมาตอบกลับด้วย")

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
    await ctx.send(f"> สวัสดีจ้า {ctx.author.mention}")


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


# TODO: Fill hug and izone image until finish
# * When users use command (.send)
@client.command()
async def send(ctx, arg=None):

    if arg == None:
        embed_arg_none = discord.Embed(title="คำสั่งหมวด send <arg>")
        embed_arg_none.add_field(name="hug", value="ต้องการกอดหรอ?")
        embed_arg_none.add_field(name="izone", value="IZ*ONE น้องหยองชอบมักๆ")
        embed_arg_none.add_field(name="nude", value="ต้องการรูปสินะ... 555555")
        embed_arg_none.add_field(name="quote", value="อยากได้คำคมหรอ?")

        await ctx.send(embed=embed_arg_none)

    # ? If arg is hug (.send hug)
    if arg == 'hug':
        hug_rd = random.randint(1, 13)
        embed_hug = discord.Embed()

        if hug_rd == 1:
            embed_hug.set_image(
                url='https://media1.tenor.com/images/9dec8539c8609196df55de188472ae37/tenor.gif')
        elif hug_rd == 2:
            embed_hug.set_image(
                url='https://i.pinimg.com/originals/6b/03/8c/6b038c71d327aca16de4bc198fb710f2.jpg')
        elif hug_rd == 3:
            embed_hug.set_image(
                url='https://i.redd.it/5824h8uby8841.jpg')
        elif hug_rd == 4:
            embed_hug.set_image(
                url='https://thumbs.gfycat.com/InfatuatedFastBluet-max-1mb.gif')
        elif hug_rd == 5:
            embed_hug.set_image(
                url='https://thumbs.gfycat.com/ScentedNearHectorsdolphin-max-1mb.gif')
        elif hug_rd == 6:
            embed_hug.set_image(
                url='https://media.giphy.com/media/vRJXuIhTWenUYWgFZT/giphy.gif')
        elif hug_rd == 7:
            embed_hug.set_image(
                url='https://pa1.narvii.com/6960/803810a086327d11b9850e1c5347732c33c07a98r1-600-480_hq.gif')
        elif hug_rd == 8:
            embed_hug.set_image(
                url='https://media1.tenor.com/images/ae425776aac226f98ae367faf40b1d0d/tenor.gif')
        elif hug_rd == 9:
            embed_hug.set_image(
                url='https://media1.tenor.com/images/3d4ea9a8343b7f8c62b54804ceeee820/tenor.gif')
        elif hug_rd == 10:
            embed_hug.set_image(
                url='https://media1.tenor.com/images/91df71d695fcefc1d90f4203d67661c1/tenor.gif')
        elif hug_rd == 11:
            embed_hug.set_image(
                url='https://i.pinimg.com/originals/a3/7c/a5/a37ca562d83a50b1467f9875ed8322b9.gif')
        elif hug_rd == 12:
            embed_hug.set_image(
                url='https://c.tenor.com/qhYX_uLj2NAAAAAC/izone-minju.gif')
        elif hug_rd == 13:
            embed_hug.set_image(
                url='https://pa1.narvii.com/6934/1027222f54d69e3c642c06bc8714b3c8e3224949r1-320-215_hq.gif')

        await ctx.send(embed=embed_hug)

    # ? If arg is izone (.send izone)
    if arg == 'izone':
        izone_rd = random.randint(1, 6)
        embed_izone = discord.Embed()

        if izone_rd == 1:
            embed_izone.set_image(
                url='https://media1.tenor.com/images/86a3809e3dfa0e0b17ecba1d776f3f21/tenor.gif')
        elif izone_rd == 2:
            embed_izone.set_image(
                url='https://media1.tenor.com/images/421a1c6c0d05f0f4c515cc9a44c98ff9/tenor.gif')
        elif izone_rd == 3:
            embed_izone.set_image(
                url='https://media1.giphy.com/media/enQCEjBvRxT6UsIlYW/giphy.gif')
        elif izone_rd == 4:
            embed_izone.set_image(
                url='https://thumbs.gfycat.com/BronzeGleamingLark-size_restricted.gif')
        elif izone_rd == 5:
            embed_izone.set_image(
                url='https://media0.giphy.com/media/vvUTAPfZACsaIkdjW3/giphy.gif')
        elif izone_rd == 6:
            embed_izone.set_image(
                url='https://i.pinimg.com/originals/42/1a/1c/421a1c6c0d05f0f4c515cc9a44c98ff9.gif')
        elif izone_rd == 7:
            embed_izone.set_image(
                url='https://thumbs.gfycat.com/BraveFabulousGrasshopper-max-1mb.gif')
        elif izone_rd == 8:
            embed_izone.set_image(
                url='https://i.pinimg.com/originals/37/1c/d0/371cd06385698091345cea743a958c1a.gif')
        elif izone_rd == 9:
            embed_izone.set_image(
                url='https://data.whicdn.com/images/332011626/original.gif')
        elif izone_rd == 10:
            embed_izone.set_image(
                url='https://thumbs.gfycat.com/FearlessGiantChinchilla-size_restricted.gif')

        await ctx.send(embed=embed_izone)

    # ? If arg is nudes (.send nude)
    if arg == 'nude':
        nude_rd = random.randint(1, 2)

        if nude_rd == 1:
            for send_nude_rd in range(random.randint(1, 5)):
                await ctx.send(f'{ctx.author.mention} ไอนี้มันเป็นคนแย่ มันขอรูปเปลือยในที่สาธารณะ')
        elif nude_rd == 2:
            embed_nude_rd_2 = discord.Embed()
            embed_nude_rd_2.set_image(
                url='https://i.makeagif.com/media/2-10-2021/g_z7xe.gif')

            await ctx.send(embed=embed_nude_rd_2)


    # ? If arg is quote (.send quote)
    if arg == 'quote':
        #//// * Open data.json file
        #////with open('data.json') as data:
            #////data = json.load(data)

        quote_rd = random.randint(1, 5)

        #////for quote in data['data']:
            #////print(quote['1'])
        
        if quote_rd == 1:
            await ctx.send('> คำคมนี้มันจะบาดตาบาดใจสักแค่ไหนกันเชียว')
        elif quote_rd == 1:
            await ctx.send('> เห็นแดดตาหยี')


# ! Run / Required Token to run
client.run(TOKEN)
