import discord
from discord.ext import commands

import pymongo
import os

MONGO_PASWORD = os.environ['mongo_password']
cluster = pymongo.MongoClient(
    f'mongodb+srv://ssuniie:{MONGO_PASWORD}@discord-bot.qwo3e.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
)
db = cluster.Yeongbot.users

class Currency(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def stats(self, ctx, member):
        id = db.find_one(db[str(ctx.author.id)])
        if str(ctx.author.id) not in db.users:
            data = {
                str(ctx.author.id): {
                    'relations': 100
                }
            }
            db.insert_one(data)
            await ctx.send('database added sucessfully!')
        else:
            await ctx.send(db[str(ctx.author.id)]['relations'])


def setup(client):
    client.add_cog(Currency(client))
