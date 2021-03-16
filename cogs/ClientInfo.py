import discord
from discord.ext import commands
from datetime import datetime, timedelta
from pytz import timezone

AUTHOR_ICON = 'https://i.ibb.co/tMbrntz/jang-wonyoung-nationality-cover2.jpg'

tz_bangkok = timedelta(hours=7)  # Bangkok's Timezone (GMT +7)


class ClientInfo(commands.Cog):
    def __init__(self, client):
        self.client = client

    # * When users uses command (.help)
    @commands.group(invoke_without_command=True)
    async def help(self, ctx):
        embed = discord.Embed(title="คำสั่งทั้งหมด ขึ้นต้นด้วย .",
                              color=0xd9598c)
        embed.set_author(name="น้องหยอง",
                         icon_url=AUTHOR_ICON)
        embed.add_field(name="help",
                        value="แสดงหน้าต่างนี้ไง", inline=True)  # ? (.help)
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

    @help.group()
    async def mute(self, ctx):
        await ctx.send('คำสั่งคือ .mute จะเป็นการปิดไมค์ทั้งห้อง')

    @help.group()
    async def unmute(self, ctx):
        await ctx.send(
            'คำสั่งคือ `.unmute` จะเป็นการเปิดไมค์ทั้งห้อง\n'
            + 'คำสั่ง `.unmute me` จะเป็นการเปิดไมค์ของตัวเอง (ในกรณีโดน Server Mute อยู่)'
        )

    @help.group()
    async def roll(self, ctx):
        await ctx.send('สุ่มตัวเลขจาก 1-10 (หรือกำหนดเอง)')

    @help.group()
    async def guessnumber(self, ctx):
        await ctx.send('เดาตัวเลข')

    @help.group()
    async def magicball(self, ctx):
        await ctx.send('ลูกแก้ววิเศษจงบอกข้าเถิด ใครงามเลิศในปัตตานี...')

    # * When users use command (.clock)
    @commands.command(aliases=['time'])
    async def clock(self, ctx):
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


def setup(client):
    client.add_cog(ClientInfo(client))
