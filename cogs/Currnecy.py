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

        print(users)


def setup(client):
    client.add_cog(Currency(client))
