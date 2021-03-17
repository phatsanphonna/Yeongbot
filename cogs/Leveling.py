import discord
from discord.ext import commands

from pymongo import MongoClient
import dns
import os

cluster_password = os.environ['mongo_password']
cluster = MongoClient(
    f'mongodb+srv://ssuniie:<{cluster_password}>@discordbot.w8ujg.mongodb.net/discordbot?retryWrites=true&w=majority'
)

leveling = cluster['discord']['leveling']


class Leveling(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        stats = leveling.find_one({"id": message.author.id})
        if not message.author.bot:
            if stats is None:
                newuser = {"id": message.author.id, "exp": 0}
                leveling.insert_one(newuser)
            else:
                exp = stats["exp"] + 5
                leveling.update_one({"id": message.author.id}, {
                                    "$set": {"exp": exp}})
                level = 0

                while True:
                    if exp < ((50*(level**2))+(50*(level-1))):
                        break
                    level += 1

                exp -= (50*(level**2))+(50*(level-1))

                if exp == 0:
                    await message.channel.send(f'well done {message.author.mention}, You level up to level {level}')

    @commands.command()
    async def rank(self, ctx):
        stats = leveling.find_one({"id": ctx.author.id})

        if stats is None:
            await ctx.send('You dont have any rank right now')
        else:
            exp = stats['exp']
            level = 0
            rank = 0

            while True:
                if exp < ((50*(level**2))+(50*(level-1))):
                    break
                level += 1

            exp -= (50*(level**2))+(50*(level-1))
            boxes = int((exp/(200*((1/2) * level)))*20)
            rankings = leveling.find().sort('exp', -1)

            for i in rankings:
                rank += 1
                if stats['id'] == i['id']:
                    break

            embed = discord.Embed(
                title=f"{ctx.author.name}'s level stats"
            )
            embed.add_field(name='Name', value=ctx.author.mention, inline=True)
            embed.add_field(
                name='EXP', value=f'{exp}/{int(200*(1/2)*level)}', inline=True)
            embed.add_field(
                name='Rank', value=f'{rank}/{ctx.guild.member_count}', inline=True)
            embed.add_field(
                name='Progrsss Bar (Level)', value=boxes *
                ":blue_square:" + (20-boxes) * ":white_large_square:", inline=True)
            await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Leveling(client))
