import discord
from discord.ext import commands

from datetime import datetime
from pytz import timezone
import random
import os

GUILD_ID = int(os.environ['GUILD_ID'])
CHANNEL_ID = int(os.environ['CHANNEL_ID'])
AUTHOR_ICON = 'https://i.ibb.co/tMbrntz/jang-wonyoung-nationality-cover2.jpg'


class Members(commands.Cog):
    def __init__(self, client):
        self.client = client

    # * When users joined the server.
    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.client.get_guild(GUILD_ID)
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

        await self.client.wait_until_ready()

        await member.add_roles(role)
        await channel.send(embed=embed_channel)
        await member.send(embed=embed_dm)
        await member.send(embed=embed_dm_image)

    # * When users left the server.
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        # * guild and channel Infomations
        guild = self.client.get_guild(GUILD_ID)
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

        await self.client.wait_until_ready()

        await channel.send(embed=embed)

    # * When users uses command (.whois)
    @commands.command()
    async def whois(self, ctx, member: discord.Member):
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

    # * When user use command (.call)
    # TODO: User can multiple call in one command
    @commands.command()
    async def call(self, ctx, user: discord.Member = None):
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


def setup(client):
    client.add_cog(Members(client))
