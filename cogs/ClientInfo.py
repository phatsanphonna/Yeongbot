import discord
from discord.ext import commands
from datetime import datetime, timedelta
from pytz import timezone

CRIT_RATE = 33
CRIT2X_RATE = 35

AUTHOR_ICON = 'https://i.ibb.co/tMbrntz/jang-wonyoung-nationality-cover2.jpg'

tz_bangkok = timedelta(hours=7)  # Bangkok's Timezone (GMT +7)
on_ready_time = datetime.now() + tz_bangkok

class ClientInfo(commands.Cog):
    def __init__(self, client):
        client = self.client

    # * When users uses command (.help)
    @commands.command()
    async def help(self, ctx, arg=None):
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
    @commands.command()
    async def info(self, ctx):
        total_restart_time = (datetime.now()+tz_bangkok) - on_ready_time

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
