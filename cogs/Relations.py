import discord
from discord.ext import commands

import pymongo
import os

MONGO_PASWORD = os.environ['mongo_password']
cluster = pymongo.MongoClient(
    f'mongodb+srv://ssuniie:{MONGO_PASWORD}@discord-bot.qwo3e.mongodb.net/myFirstDatabase?retryWrites=true&w=majority'
)
db = cluster.Yeongbot.users

class Relations(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def stats(self, ctx):
        user_id = db.find_one({'id': ctx.author.id})

        if user_id is None:
            data = {
                'id': ctx.author.id,
                'relations': 100
            }
            db.insert_one(data)
            await ctx.send('database added sucessfully!')
        else:
            await ctx.send(user_id['relations'])


def setup(client):
    client.add_cog(Relations(client))
