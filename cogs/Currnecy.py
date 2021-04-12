import discord
from discord.ext import commands

import json


class Currency(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def money(self, ctx):
        with open('users.json') as f:
            users = json.load(f)

        for user in users:
            if ctx.author.id in user['user_id']:
                print(users['user_id'])
            else:
                new_id = {
                    'id': ctx.author.id,
                    'money': 1
                }
                
                print(new_id)

        print(users)


def setup(client):
    client.add_cog(Currency(client))
